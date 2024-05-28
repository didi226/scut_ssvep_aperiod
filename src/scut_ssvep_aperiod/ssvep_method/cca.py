import os.path
import sys
import math
# sys.path.append('..')
from sklearn.decomposition import FastICA
import numpy as np

import pandas as pd
from scipy.signal import firwin, lfilter
from scut_ssvep_aperiod.utils.common_function import cal_acc
from scut_ssvep_aperiod.ssvep_method.ssvep_methd_base import CCABase

class CCACommon(CCABase):
	def __init__(self, sfreq, ws, fres_list, n_harmonics):
		"""

		:param Fs:
		:param ws:
		:param fres_list:
		:param n_harmonics:
		"""

		super(CCACommon, self).__init__(sfreq, ws, fres_list, n_harmonics)

	def cca_ex(self,  test_data, ica_ = False):
		if ica_:
			ica = FastICA(n_components = 6)
			test_data_0 = ica.fit_transform(test_data.T)  # S是独立成分.T
			test_data_1 = ica.mixing_.T
			test_data = test_data_0.dot(test_data_1).T

		reference_signals = self.get_reference_signal()
		result = self.find_correlation(1, test_data, reference_signals)
		return result

	def cca_classify(self, test_data, ica_ = False):
		result = self.cca_ex(test_data, ica_)
		return np.argmax(result)
	def classify(self, test_data, ica_ = False):
		label = np.zeros((test_data.shape[0]))
		for i, i_data in enumerate(test_data):
			label[i] = self.cca_classify(i_data, ica_)
		return label
	def calculate_ex(self,test_data,ica_=False):
		ex = np.zeros((test_data.shape[0],self.n_event ))
		for i, i_data in enumerate(test_data):
			ex[i,:] = self.cca_ex(i_data, ica_)
		return ex