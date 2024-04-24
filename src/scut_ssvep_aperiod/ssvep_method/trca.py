import sys
import numpy as np
from numpy import linalg as LA
from scipy.io import loadmat, savemat
from scipy import signal as SIG
from scut_ssvep_aperiod.ssvep_method.ssvep_methd_base import SSVEPMethodBase
import time
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from mne.filter import filter_data
class TRCA(SSVEPMethodBase):
    def __init__(self, sfreq, ws, fres_list,filter_=None):
        super(TRCA, self).__init__(sfreq, ws, fres_list)
        ##trca没有谐波的概念

    def train(self,train_data,train_label):
        """
        :param train_data:  shape (n_trials, n_channels, n_times)
        :param train_label: shape (n_trials,)
        :param fres_list:   list len(n_event)
        :return:
        """
        #准备数据
        if filter_ is not None:
            train_data = filter_data(train_data, self.sfreq, filter_[0], filter_[1])
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
        self.weight = W
        self.temp_X = temp_X
        return W,temp_X

    def classifier(self,test_data):
        if filter_ is not None:
            test_data = filter_data(test_data, self.sfreq, filter_[0], filter_[1])
        n_test_trials = np.shape(test_data)[0]
        coefficients = np.zeros([self.n_event])
        result = np.zeros([n_test_trials], np.int32)
        for test_idx in range(n_test_trials):
            test_trial = test_data[test_idx,:, :]
            for i, w in enumerate(self.weight):
                w = w[None, :]
                test_i = np.dot(w, test_trial)
                temp_i = np.dot(w, self.temp_X[i, :, :])
                coefficients[i], _ = pearsonr(test_i[0], temp_i[0])
            label = np.max(np.where(coefficients == np.max(coefficients)))
            result[test_idx] = label
        return result
if __name__ == "__main__":
    from scut_ssvep_aperiod.load_dataset.dataset_lee import LoadDataLeeOne
    from scut_ssvep_aperiod.utils.common_function import cal_acc
    data_path = r"D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\session1\s1\sess01_subj01_EEG_SSVEP.mat"
    datasetone = LoadDataLeeOne(data_path)
    train_data, train_label, test_data, test_label = datasetone.get_data(pro_ica = False, filter_para = [3,40], resample=4)
    print(train_data.shape, train_label.shape,test_data.shape, test_label.shape)
    ssvep_method = TRCA(datasetone.sample_rate_test, datasetone.window_time,datasetone.freqs)
    ssvep_method.train(train_data,train_label)
    predict_label = ssvep_method.classifier(test_data)
    print(predict_label,test_label)
    acc = cal_acc(test_label, predict_label)
    print(acc)
