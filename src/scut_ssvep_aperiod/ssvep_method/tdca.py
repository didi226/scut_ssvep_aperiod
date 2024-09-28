
# Original Designer:Ethan Pan
# Mod Designer: Di Chen
# Time:2024/09/25
import numpy as np
from scipy.linalg import qr
from scipy.stats import pearsonr
from sklearn.base import BaseEstimator, TransformerMixin, ClassifierMixin
from scut_ssvep_aperiod.ssvep_method.ssvep_methd_base import CCABase
from scipy import signal
from scipy.linalg import eigh
from scipy.linalg import solve
from scut_ssvep_aperiod.utils.common_function import cal_acc


def isPD(B):
    """
    Checks if the input matrix is positive-definite using Cholesky decomposition.

    This function determines whether the matrix B is positive-definite by attempting
    to perform a Cholesky decomposition. If the decomposition succeeds, the matrix
    is positive-definite; otherwise, it is not.

    Args:
        B (ndarray): Any matrix, shape (N, N).

    Returns:
        bool: True if B is positive-definite, False otherwise.
    """

    try:
        _ = np.linalg.cholesky(B)
        return True
    except np.linalg.LinAlgError:
        return False


def nearestPD(A):
    """
    Finds the nearest positive-definite matrix to the input.

    Args:
        A (ndarray): Any square matrix, shape (N, N).

    Returns:
        ndarray: Positive-definite matrix closest to A.

    References:
        N.J. Higham, "Computing a nearest symmetric positive semidefinite matrix" (1988):
        https://doi.org/10.1016/0024-3795(88)90223-6
    """

    B = (A + A.T) / 2
    _, s, V = np.linalg.svd(B)

    H = np.dot(V.T, np.dot(np.diag(s), V))

    A2 = (B + H) / 2

    A3 = (A2 + A2.T) / 2

    if isPD(A3):
        return A3

    print("Replace current matrix with the nearest positive-definite matrix.")

    spacing = np.spacing(np.linalg.norm(A))
    # The above is different from [1]. It appears that MATLAB's `chol` Cholesky
    # decomposition will accept matrixes with exactly 0-eigenvalue, whereas
    # Numpy's will not. So where [1] uses `eps(mineig)` (where `eps` is Matlab
    # for `numpy.spacing`), we use the above definition. CAVEAT: our `spacing`
    # will be much larger than [1]'s `eps(mineig)`, since `mineig` is usually on
    # the order of 1e-16, and `eps(1e-16)` is on the order of 1e-34, whereas
    # `spacing` will, for Gaussian random matrixes of small dimension, be on
    # othe order of 1e-16. In practice, both ways converge, as the unit test
    # below suggests.
    eye = np.eye(A.shape[0])
    k = 1
    while not isPD(A3):
        mineig = np.min(np.real(np.linalg.eigvals(A3)))
        A3 += eye * (-mineig * k ** 2 + spacing)
        k += 1

    return A3


def robust_pattern(W, Cx, Cs):
    """
    Transforms spatial filters to spatial patterns based on the method described in the literature.

    This function constructs spatial patterns from spatial filters, which illustrates how to combine
    information from different EEG channels to extract signals of interest. For neurophysiological
    interpretation or visualization of weights, it is essential to derive activation patterns from
    the obtained spatial filters.

    Args:
        W (ndarray): Spatial filters, shape (n_channels, n_filters).
        Cx (ndarray): Covariance matrix of EEG data, shape (n_channels, n_channels).
        Cs (ndarray): Covariance matrix of source data, shape (n_channels, n_channels).

    Returns:
        ndarray: Spatial patterns, shape (n_channels, n_patterns), where each column represents a
        spatial pattern.

    References:
        Haufe, Stefan, et al. "On the interpretation of weight vectors of linear models in multivariate
        neuroimaging." Neuroimage 87 (2014): 96-110.

    Notes:
        Use `linalg.solve` instead of `inv` to enhance numerical stability.
        For more details, see:
        - https://github.com/robintibor/fbcsp/blob/master/fbcsp/signalproc.py
        - https://ww2.mathworks.cn/help/matlab/ref/mldivide.html
    """
    A = solve(Cs.T, np.dot(Cx, W).T).T
    return A


def xiang_dsp_kernel(X, y):
    """
    DSP: Discriminative Spatial Patterns, only for two classes.

    This function solves spatial filters with DSP by finding a projection matrix
    that maximizes the between-class scatter matrix and minimizes the within-class
    scatter matrix. Currently, it supports only two types of data.

    Args:
        X (ndarray): EEG train data (n_trials, n_channels, n_samples) with mean removed.
        y (ndarray): Labels of EEG data (n_trials,).

    Returns:
        tuple:
            W (ndarray): Spatial filters (n_channels, n_filters).
            D (ndarray): Eigenvalues in descending order.
            M (ndarray): Mean value of all classes and trials (n_channel, n_samples).
            A (ndarray): Spatial patterns (n_channels, n_filters).

    Raises:
        ValueError: If the number of components exceeds the number of channels.

    References:
        Liao, Xiang, et al. "Combining spatial filters for the classification of single-trial EEG in a finger movement task."
        IEEE Transactions on Biomedical Engineering 54.5 (2007): 821-831.
    """
    X, y = np.copy(X), np.copy(y)
    labels = np.unique(y)
    X = np.reshape(X, (-1, *X.shape[-2:]))
    X = X - np.mean(X, axis=-1, keepdims=True)
    # the number of each label
    n_labels = np.array([np.sum(y == label) for label in labels])
    # average template of all trials
    M = np.mean(X, axis=0)
    # class conditional template
    Ms, Ss = zip(
        *[
            (
                np.mean(X[y == label], axis=0),
                np.sum(
                    np.matmul(X[y == label], np.swapaxes(X[y == label], -1, -2)), axis=0  # Equation (2)
                ),
            )
            for label in labels
        ]
    )
    Ms, Ss = np.stack(Ms), np.stack(Ss)
    # within-class scatter matrix
    Sw = np.sum(
        Ss - n_labels[:, np.newaxis, np.newaxis] * np.matmul(Ms, np.swapaxes(Ms, -1, -2)),
        axis=0,
    )
    Ms = Ms - M
    # between-class scatter matrix
    Sb = np.sum(
        n_labels[:, np.newaxis, np.newaxis] * np.matmul(Ms, np.swapaxes(Ms, -1, -2)),  # Equation (3)
        axis=0,
    )

    D, W = eigh(nearestPD(Sb), nearestPD(Sw))
    ix = np.argsort(D)[::-1]  # in descending order
    D, W = D[ix], W[:, ix]
    A = robust_pattern(W, Sb, W.T @ Sb @ W)

    return W, D, M, A


def xiang_dsp_feature(W, M, X, n_components):
    """
    Return DSP features as described in the paper.

    Args:
        W (ndarray): Spatial filters (n_channels, n_filters).
        M (ndarray): Common template for all classes (n_channel, n_samples).
        X (ndarray): EEG test data (n_trials, n_channels, n_samples).
        n_components (int, optional): Length of the spatial filters; first k components to use (default is 1).

    Returns:
        ndarray: Features (n_trials, n_components, n_samples).

    Raises:
        ValueError: If n_components is greater than the number of channels.

    References:
        Liao, Xiang, et al. "Combining spatial filters for the classification of single-trial EEG in a finger movement task."
        IEEE Transactions on Biomedical Engineering 54.5 (2007): 821-831.
    """
    W, M, X = np.copy(W), np.copy(M), np.copy(X)
    max_components = W.shape[1]
    if n_components > max_components:
        raise ValueError("n_components should less than the number of channels")
    X = np.reshape(X, (-1, *X.shape[-2:]))
    X = X - np.mean(X, axis=-1, keepdims=True)
    features = np.matmul(W[:, :n_components].T, X - M)
    return features


def proj_ref(Yf):
    """
    Calculate the projection matrix from Sin-Cosine reference signals.

    Args:
        Yf (ndarray): Sin-Cosine reference signals (n_freq, 2 * num_harmonics, n_points).

    Returns:
        ndarray: Projection matrix.
    """
    Q, R = qr(Yf.T, mode="economic")
    # 计算投影矩阵P
    P = Q @ Q.T  # @ 表示矩阵乘法
    return P


def lagging_aug(X, n_samples, lagging_len, P, training):
    """
    Augment EEG signals with lagging.

    Args:
        X (ndarray): Input EEG signals (n_trials, n_channels, n_points).
        n_samples (int): Number of delayed sample points.
        lagging_len (int): Lagging length.
        P (ndarray): Projection matrix (n_points, n_points).
        training (bool): True for training, False for testing.

    Returns:
        ndarray: Augmented EEG signals (n_trials, (lagging_len + 1) * n_channels, n_samples).

    Raises:
        ValueError: If the length of X is not greater than lagging_len + n_samples.
    """
    # Reshape X to (n_trials, n_channels, n_points)
    X = X.reshape((-1, *X.shape[-2:]))
    n_trials, n_channels, n_points = X.shape

    if n_points < lagging_len + n_samples:
        raise ValueError("the length of X should be larger than l+n_samples.")
    aug_X = np.zeros((n_trials, (lagging_len + 1) * n_channels, n_samples))

    if training:
        for i in range(lagging_len + 1):
            aug_X[:, i * n_channels: (i + 1) * n_channels, :] = X[..., i: i + n_samples]
    else:
        for i in range(lagging_len + 1):
            aug_X[:, i * n_channels: (i + 1) * n_channels, : n_samples - i] = X[..., i:n_samples]

    aug_Xp = aug_X @ P
    aug_X = np.concatenate([aug_X, aug_Xp], axis=-1)
    return aug_X


def tdca_feature(X, templates, W, M, Ps, lagging_len, n_components, training=False):
    """
    Compute the TDCA feature.

    Args:
        X (ndarray): Input EEG signals (n_trials, n_channels, n_points).
        templates (ndarray): EEG template signals (n_freq, n_channels, n_points).
        W (ndarray): Spatial filters (n_channels, n_filters).
        M (ndarray): Common templates for all categories (n_channels, n_points).
        Ps (list): Projection matrices (n_freq, n_channels, n_points).
        lagging_len (int): Lagging length.
        n_components (int): Number of components.
        training (bool): True for training, False for testing.

    Returns:
        list: Correlation coefficients (n_freq,).
    """
    rhos = []
    for Xk, P in zip(templates, Ps):
        a = xiang_dsp_feature(W, M, lagging_aug(X, P.shape[0], lagging_len, P, training=training),
                              n_components=n_components)
        b = Xk[:n_components, :]
        a = np.reshape(a, (-1))
        b = np.reshape(b, (-1))
        rhos.append(pearsonr(a, b)[0])
    return rhos


class TDCA(CCABase):
    """
    Class for TDCA (Temporal Discriminative Component Analysis).

    Attributes:
        sfreq (float): Sampling frequency.
        ws (int): Window size.
        fres_list (list): Frequency list.
        n_harmonics (int): Number of harmonics.
        Nm (int): Number of channels.
        Nc (int): Number of components.
        lagging_len (int): Lagging length.
        passband (list): Passband frequencies.
        stopband (list): Stopband frequencies.
        highcut_pass (float): Highcut pass frequency.
        highcut_stop (float): Highcut stop frequency.
    """
    def __init__(self, sfreq, ws, fres_list, n_harmonics,Nc = 10,Nm=1,
                 passband = [6, 14, 22, 30, 38],
                 stopband = [4, 10, 16, 24, 32],
                 highcut_pass =40,highcut_stop=50,lagging_len=0):
        """
        Initialize TDCA.

        Args:
            sfreq (float): Sampling frequency.
            ws (int): Window size.
            fres_list (list): Frequency list.
            n_harmonics (int): Number of harmonics.
            Nc (int): Number of channels.
            Nm (int): Number of components.
            passband (list): Passband frequencies.
            stopband (list): Stopband frequencies.
            highcut_pass (float): Highcut pass frequency.
            highcut_stop (float): Highcut stop frequency.
            lagging_len (int): Lagging length.
        """
        super(TDCA, self).__init__(sfreq, ws, fres_list, n_harmonics)
        self.Nm = Nm
        self.Nc = Nc
        self.Nf = self.n_event
        self.lagging_len = lagging_len
        self.n_components = 3
        self.passband = passband
        self.stopband = stopband
        self.highcut_pass = highcut_pass
        self.highcut_stop = highcut_stop



    def filter_bank(self, X):
        """
        Apply filter bank to EEG signals.

        Args:
            X (ndarray): Input EEG signals (n_trials, n_channels, n_points).

        Returns:
            ndarray: Output EEG signals of filter banks (n_fb, n_trials, n_channels, n_points).
        """
        FB_X = np.zeros((self.Nm, X.shape[0], self.Nc, X.shape[-1]))
        nyq = self.sfreq / 2
        # passband = [6, 14, 22, 30, 38]
        # stopband = [4, 10, 16, 24, 32]
        # # passband = [6, 14, 22, 30, 38, 46, 54, 62, 70, 78]
        # # stopband = [4, 10, 16, 24, 32, 40, 48, 56, 64, 72]
        # highcut_pass, highcut_stop = 40, 50  #80 ,90

        gpass, gstop, Rp = 3, 40, 0.5
        for i in range(self.Nm):
            Wp = [self.passband[i] / nyq, self.highcut_pass / nyq]
            Ws = [self.stopband[i] / nyq, self.highcut_stop / nyq]
            [N, Wn] = signal.cheb1ord(Wp, Ws, gpass, gstop)
            [B, A] = signal.cheby1(N, Rp, Wn, 'bandpass')
            data = signal.filtfilt(B, A, X, padlen=3 * (max(len(B), len(A)) - 1)).copy()
            FB_X[i, :, :, :] = data
        if self.Nm == 1:
            FB_X = X [None,:]
        return FB_X
    # def filter_bank(self, X):
    #     '''
    #     Parameters
    #     ----------
    #     X: Input EEG signals (n_trials, n_channels, n_points)
    #     Returns: Output EEG signals of filter banks FB_X (n_fb, n_trials, n_channels, n_points)
    #     -------
    #     '''
    #     FB_X = np.zeros((self.Nm, X.shape[0], self.Nc, X.shape[-1]))
    #     nyq = self.sfreq / 2
    #     # passband = [10, 18, 26, 34, 38, 46]
    #     # stopband = [8, 16, 24,32,36,44]
    #     passband = [10,14, 18, 22,26, 30,34, 38, 42,46]
    #     stopband = [8, 12,16,20, 24, 28,32, 36,40, 44]
    #     highcut_pass, highcut_stop = 42,48
    #
    #     gpass, gstop, Rp = 3, 40, 0.5
    #     for i in range(self.Nm):
    #         Wp = [passband[i] / nyq, highcut_pass / nyq]
    #         Ws = [stopband[i] / nyq, highcut_stop / nyq]
    #         [N, Wn] = signal.cheb1ord(Wp, Ws, gpass, gstop)
    #         [B, A] = signal.cheby1(N, Rp, Wn, 'bandpass')
    #         data = signal.filtfilt(B, A, X, padlen=3 * (max(len(B), len(A)) - 1)).copy()
    #         FB_X[i, :, :, :] = data
    #
    #     return FB_X

    def train(self, X, y):
        """
        Train the TDCA model on input EEG signals and labels.

        Args:
            X (ndarray): Input EEG signals (n_trials, n_channels, n_points).
            y (ndarray): Input labels (n_trials,).

        Returns:
            self: TDCA object.
        """
        self.classes_ = np.unique(y)
        Yf = self.get_reference_signal()
        self.Ps = [proj_ref(Yf[i]) for i in range(len(self.classes_))]

        self.W, self.M, self.templates = [], [], []

        self.FB_X_Train = self.filter_bank(X)
        for fb_i in range(self.Nm):
            X = self.FB_X_Train[fb_i] - np.mean(self.FB_X_Train[fb_i], axis=-1,
                                                keepdims=True)  # For meeting the requirement of DSP Kernel
            aug_X_list, aug_Y_list = [], []
            for i, label in enumerate(self.classes_):
                aug_X_list.append(
                    lagging_aug(X[y == label], self.Ps[i].shape[0], self.lagging_len, self.Ps[i], training=True))
                aug_Y_list.append(y[y == label])

            aug_X = np.concatenate(aug_X_list, axis=0)
            aug_Y = np.concatenate(aug_Y_list, axis=0)

            W_fbi, _, M_fbi, _ = xiang_dsp_kernel(aug_X, aug_Y)
            self.W.append(W_fbi)
            self.M.append(M_fbi)

            self.templates.append(np.stack(
                [np.mean(
                    xiang_dsp_feature(W_fbi, M_fbi, aug_X[aug_Y == label], n_components=W_fbi.shape[1]), axis=0)
                    for label in self.classes_
                ]
            ))
        return self

    def transform(self, X, fb_i):
        """
        Transform input EEG signals into features.

        Args:
            X (ndarray): Input EEG signals (n_trials, n_channels, n_points).
            fb_i (int): Filter bank index.

        Returns:
            ndarray: Feature vectors (n_trials, n_freq).
        """
        X -= np.mean(X, axis=-1, keepdims=True)
        X = X.reshape((-1, *X.shape[-2:]))
        rhos = [
            tdca_feature(tmp, self.templates[fb_i], self.W[fb_i], self.M[fb_i], self.Ps, self.lagging_len,
                         n_components=self.n_components)
            for tmp in X
        ]
        rhos = np.stack(rhos)
        return rhos

    def classifier(self, X):
        """
        Classify input EEG signals.

        Args:
           X (ndarray): Input EEG signals (n_trials, n_channels, n_points).

        Returns:
           ndarray: Predicted labels (n_trials,).
        """

        if self.Nm == 1:
            sum_features = self.transform(X, 0)
        else:
            sum_features = np.zeros((self.Nm, X.shape[0], self.Nf))
            self.FB_X_Test = self.filter_bank(X)
            for fb_i in range(self.Nm):
                fb_weight = (fb_i + 1) ** (-1.25) + 0.25
                sum_features[fb_i] = fb_weight * self.transform(self.FB_X_Test[fb_i], fb_i)
            sum_features = np.sum(sum_features, axis=0)
        self.result_ex = sum_features
        pred_labels = self.classes_[np.argmax(sum_features, axis=-1)]
        return pred_labels

    def calculate_ex(self):
        """
        Calculate features from the last transformation.

        Returns:
            ndarray: Extracted features.
        """
        return self.result_ex
if __name__ == "__main__":
    from scut_ssvep_aperiod.load_dataset.dataset_lee import LoadDataLeeOne
    data_path = r"D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\session1\s1\sess01_subj01_EEG_SSVEP.mat"
    datasetone = LoadDataLeeOne(data_path)
    train_data, train_label, test_data, test_label = datasetone.get_data(pro_ica = None, filter_para = [1,40], resample=4)
    print(train_data.shape, train_label.shape,test_data.shape, test_label.shape)
    ssvep_method = TDCA(datasetone.sample_rate_test, datasetone.window_time,datasetone.freqs,3)
    ssvep_method.train(train_data,train_label)
    predict_label = ssvep_method.classifier(test_data)
    print(predict_label,test_label)
    acc = cal_acc(test_label, predict_label)
    print(acc)
