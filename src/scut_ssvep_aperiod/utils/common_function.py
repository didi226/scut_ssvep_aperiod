from mne_icalabel.iclabel import iclabel_label_components
from typing import Union, Optional, Dict, List, Tuple, Callable
from mne.preprocessing import ICA
import os
def ica_iclabel(raw, n_components = None,remove_label = {'muscle artifact':0.9 ,'eye blink':0.9, 'heart beat':0.9}):
    """
    去眼电 自动识别眼电通道去眼电
    :param raw:           mne raw 结构
    :return:
           reconst_raw:   去眼电后的raw结构
    """

    ica = ICA( n_components = n_components,
        max_iter="auto",
        method="infomax",
        random_state = 97,
        fit_params=dict(extended=True),
    )
    ica.fit(raw)
    labels_pred_proba = iclabel_label_components(raw, ica)
    label_list =['brain', 'muscle artifact', 'eye blink', 'heart beat', 'line noise', 'channel noise', 'other']
    exclude_components = []
    for n_components in range(labels_pred_proba.shape[0]):
        for i, i_label in enumerate(label_list):
            if i_label in remove_label.items():
                if labels_pred_proba[n_components, i] >= remove_label[i_label]:
                    exclude_components.append(n_components)
                    continue
    ica.apply(raw, exclude = exclude_components)
    return raw

def get_filelist(dir, str= ".mat"):
    """
    获取文件夹内后缀str的文件序列并且排序
    :param      dir        str      文件夹地址
    :param      str        str      后缀
    :return:    filelist   list
    """
    filelist = []
    files=os.listdir(dir)
    for i_file in files :  # 遍历整个文件夹
        path = os.path.join(dir, i_file)
        if os.path.isfile(path):  # 判断是否为一个文件，排除文件夹
            if os.path.splitext(path)[1] == str:
                filelist.append(i_file)
    return filelist


def cal_acc(Y_true: List[int], Y_pred: List[int]) -> float:
    """
    Calculate accuracy

    Parameters
    ----------
    Y_true : List[int]
        True labels
    Y_pred : List[int]
        Predicted labels

    Returns
    -------
    acc : float
        Accuracy
    """
    if len(Y_true) != len(Y_pred):
        raise ValueError('Lengths of true labels and predicted labels should be same')
    true_detect = [1 for i in range(len(Y_true)) if int(Y_true[i])==int(Y_pred[i])]
    true_detect_count = sum(true_detect)
    acc = true_detect_count/len(Y_true)
    return acc


# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 10:16:21 2019

@author: ALU
"""
import warnings
import scipy.signal
import numpy as np


def filterbank(eeg, fs, idx_fb):
    if idx_fb == None:
        warnings.warn('stats:filterbank:MissingInput ' \
                      + 'Missing filter index. Default value (idx_fb = 0) will be used.')
        idx_fb = 0
    elif (idx_fb < 0 or 9 < idx_fb):
        raise ValueError('stats:filterbank:InvalidInput ' \
                         + 'The number of sub-bands must be 0 <= idx_fb <= 9.')

    if (len(eeg.shape) == 2):
        num_chans = eeg.shape[0]
        num_trials = 1
    else:
        num_chans, _, num_trials = eeg.shape

    # Nyquist Frequency = Fs/2N
    Nq = fs / 2

    passband = [6, 14, 22, 30, 38, 46, 54, 62, 70, 78]
    stopband = [4, 10, 16, 24, 32, 40, 48, 56, 64, 72]
    Wp = [passband[idx_fb] / Nq, 90 / Nq]
    Ws = [stopband[idx_fb] / Nq, 100 / Nq]
    [N, Wn] = scipy.signal.cheb1ord(Wp, Ws, 3, 40)  # band pass filter StopBand=[Ws(1)~Ws(2)] PassBand=[Wp(1)~Wp(2)]
    [B, A] = scipy.signal.cheby1(N, 0.5, Wn, 'bandpass')  # Wn passband edge frequency

    y = np.zeros(eeg.shape)
    if (num_trials == 1):
        for ch_i in range(num_chans):
            # apply filter, zero phass filtering by applying a linear filter twice, once forward and once backwards.
            # to match matlab result we need to change padding length
            y[ch_i, :] = scipy.signal.filtfilt(B, A, eeg[ch_i, :], padtype='odd', padlen=3 * (max(len(B), len(A)) - 1))

    else:
        for trial_i in range(num_trials):
            for ch_i in range(num_chans):
                y[ch_i, :, trial_i] = scipy.signal.filtfilt(B, A, eeg[ch_i, :, trial_i], padtype='odd',
                                                            padlen=3 * (max(len(B), len(A)) - 1))

    return y


if __name__ == '__main__':
    from scipy.io import loadmat

    D = loadmat("sample.mat")
    eeg = D['eeg']
    eeg = eeg[:, :, (33):(33 + 125), :]
    eeg = eeg[:, :, :, 0]  # first bank
    eeg = eeg[0, :, :]  # first target

    y1 = filterbank(eeg, 250, 0)
    y2 = filterbank(eeg, 250, 9)

    y1_from_matlab = loadmat("y1_from_matlab.mat")['y1']
    y2_from_matlab = loadmat("y2_from_matlab.mat")['y2']

    dif1 = y1 - y1_from_matlab
    dif2 = y2 - y2_from_matlab

    print("Difference between matlab and python = ", np.sum(dif1))
    print("Difference between matlab and python = ", np.sum(dif2))

