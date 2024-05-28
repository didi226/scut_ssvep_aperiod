import sys
import numpy as np
from numpy import linalg as LA
from scipy.io import loadmat, savemat
from scipy import signal as SIG
from scut_ssvep_aperiod.ssvep_method.ssvep_methd_base import CCABase
import time
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from mne.filter import filter_data
from scipy import signal
class TRCA(CCABase):
    def __init__(self, sfreq, ws, fres_list,n_harmonics,filter_=None):
        super(TRCA, self).__init__(sfreq, ws, fres_list,n_harmonics)
        self.filter_=filter_
        ##trca没有谐波的概念
    def get_w(self,train_data):
        temp_data = [None] * self.n_event
        temp_X =[]
        for i, i_stimu in enumerate(self.fres_list):
            idx = np.where(train_label == i)
            temp_data[i] = train_data[idx[0],:,:]
            temp_data[i] = temp_data[i] - np.mean(temp_data[i], axis=2)[:, :, None]
            temp_X.append(np.mean(temp_data[i], axis = 0))
        temp_X = np.array(temp_X)
        _, n_channels, n_samples = temp_data[0].shape

        W = np.zeros([self.n_event, n_channels], np.float64)
        Q = np.zeros([n_channels, n_channels], np.float64)
        S = np.zeros_like(Q)
        for i_event in range(self.n_event):
            data = temp_data[i_event]
            n_trials = data.shape[0]
            UX = np.reshape(data, [n_channels, n_samples * n_trials], order='C')
            Q = np.matmul(UX, UX.T) / n_trials
            S = np.zeros_like(Q)
            for xi in range(n_trials):
                for xj in range(n_trials):
                    if xi != xj:
                        data_i = data[xi,:, :]
                        data_j = data[xj,:, : ]
                        S += np.matmul(data_i, data_j.T)
            S = S / (n_trials * (n_trials - 1))
            eigenvalues, eigenvectors = LA.eig(np.matmul(LA.inv(Q), S))
            w_index = np.max(np.where(eigenvalues == np.max(eigenvalues)))
            W[i_event, :] = eigenvectors[:, w_index].T
        return W, temp_X
        # self.weight = W
        # self.temp_X = temp_X

    def train(self,train_data,train_label):
        """
        :param train_data:  shape (n_trials, n_channels, n_times)
        :param train_label: shape (n_trials,)
        :param fres_list:   list len(n_event)
        :return:
        """
        #准备数据
        if self.filter_ is not None:
            train_data = filter_data(train_data, self.sfreq, self.filter_[0], self.filter_[1])
        train_data = self.filter_bank(train_data)
        self.n_filter = train_data.shape[0]
        ###初始化w temp_X
        w_all =[]
        temp_x_all=[]
        for i_train_data in  train_data:
            W,temp_X = self.get_w(i_train_data)
            w_all.append(W)
            temp_x_all.append(temp_X)
        w_all = np.array(w_all)
        temp_x_all =  np.array(temp_x_all)
        self.weight = w_all
        self.temp_x = temp_x_all
        return w_all,temp_x_all

    def filter_bank(self, X):
        '''
        Parameters
        ----------
        X: Input EEG signals (n_trials, n_channels, n_points)
        Returns: Output EEG signals of filter banks FB_X (n_fb, n_trials, n_channels, n_points)
        -------
        '''
        self.Nm = 10
        self.Nc = 10
        FB_X = np.zeros((self.Nm, X.shape[0], self.Nc, X.shape[-1]))
        nyq = self.sfreq / 2
        # passband = [14,40]
        # stopband = [4,18]
        passband =  [40]*10
        # stopband =  [3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39]
        stopband = [3, 7, 11, 15, 19,  23, 27, 31, 35, 39]
        self.w_band = np.zeros((10))
        for i in range(10):
            self.w_band[i] = (i+1)**(-1)+0.3


        highcut_pass, highcut_stop = 45, 50  #80 ,90

        gpass, gstop, Rp = 3, 40, 0.5
        for i in range(self.Nm):
            Wp = [passband[i] / nyq, highcut_pass / nyq]
            Ws = [stopband[i] / nyq, highcut_stop / nyq]
            [N, Wn] = signal.cheb1ord(Wp, Ws, gpass, gstop)
            [B, A] = signal.cheby1(N, Rp, Wn, 'bandpass')
            data = signal.filtfilt(B, A, X, padlen=3 * (max(len(B), len(A)) - 1)).copy()
            FB_X[i, :, :, :] = data

        return FB_X

    def classifier(self,test_data):
        if self.filter_ is not None:
            test_data = filter_data(test_data, self.sfreq, self.filter_[0], self.filter_[1])
        test_data = self.filter_bank(test_data)
        n_test_trials = np.shape(test_data)[1]
        coefficients = np.zeros([self.n_filter,self.n_event])
        result = np.zeros([n_test_trials], np.int32)
        for test_idx in range(n_test_trials):
            for i_filter,w_filter in enumerate(self.weight):
                test_trial = test_data[i_filter, test_idx, :, :]
                for i, w in enumerate(w_filter):
                    w = w[None, :]
                    test_i = np.dot(w, test_trial)
                    temp_i = np.dot(w, self.temp_x[i_filter,i, :, :])
                    coefficients[i_filter,i], _ = pearsonr(test_i[0], temp_i[0])
            coefficients = coefficients**2
            coefficients_mean =  np.squeeze(np.dot(coefficients.T,self.w_band[:,None]))
            label = np.max(np.where(coefficients_mean == np.max(coefficients_mean)))
            result[test_idx] = label


        return result
if __name__ == "__main__":
    from scut_ssvep_aperiod.load_dataset.dataset_lee import LoadDataLeeOne
    from scut_ssvep_aperiod.utils.common_function import cal_acc
    data_path = r"D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\session1\s1\sess01_subj01_EEG_SSVEP.mat"
    datasetone = LoadDataLeeOne(data_path)
    train_data, train_label, test_data, test_label = datasetone.get_data(pro_ica = False, filter_para = [3,40], resample=4)
    print(train_data.shape, train_label.shape,test_data.shape, test_label.shape)
    ssvep_method = TRCA(datasetone.sample_rate_test, datasetone.window_time,datasetone.freqs,3)
    ssvep_method.train(train_data,train_label)
    predict_label = ssvep_method.classifier(test_data)
    print(predict_label,test_label)
    acc = cal_acc(test_label, predict_label)
    print(acc)
