from sklearn.decomposition import FastICA
import numpy as np

from scut_ssvep_aperiod.ssvep_method.ssvep_methd_base import CCABase

class CCACommon(CCABase):
	def __init__(self, sfreq, ws, fres_list, n_harmonics):
		"""
		Initializes the CCACommon class.

		Args:
			sfreq (float): Sampling frequency.
			ws (int): Window size.
			fres_list (list): List of frequency results.
			n_harmonics (int): Number of harmonics.
		"""
		super(CCACommon, self).__init__(sfreq, ws, fres_list, n_harmonics)

	def _cca_ex(self,  test_data, ica_ = False):
		"""
		Performs Canonical Correlation Analysis (CCA) on the provided test data.

		Args:
			test_data (ndarray): Input data with shape (n_channels, n_times).
			ica_ (bool): Flag indicating whether to apply Independent Component Analysis (ICA).

		Returns:
			ndarray: The correlation results obtained from the CCA.
		"""
		if ica_:
			ica = FastICA(n_components = 6)
			test_data_0 = ica.fit_transform(test_data.T)  # S是独立成分.T
			test_data_1 = ica.mixing_.T
			test_data = test_data_0.dot(test_data_1).T

		reference_signals = self.get_reference_signal()
		result = self.find_correlation(1, test_data, reference_signals)
		return result

	def _cca_classify(self, test_data, ica_ = False):
		"""
		Classifies the test data using CCA.

		Args:
			test_data (ndarray):  shape(n_channels,n_times)
			ica_ (bool): Whether to apply ICA.

		Returns:
			int: The index of the class with the highest correlation.
		"""
		result = self._cca_ex(test_data, ica_)
		return np.argmax(result)
	def classify(self, test_data, ica_ = False):
		"""
		Classifies the provided test data using Canonical Correlation Analysis (CCA).

		Args:
			test_data (ndarray): Input data with shape (n_channels, n_times).
			ica_ (bool): Flag indicating whether to apply ICA.

		Returns:
			int: The index of the class with the highest correlation result.
		"""
		label = np.zeros((test_data.shape[0]))
		for i, i_data in enumerate(test_data):
			label[i] = self._cca_classify(i_data, ica_)
		return label
	def calculate_ex(self,test_data,ica_ = False):
		"""
		Calculates the CCA results for each sample in the test data.

		Args:
			test_data (ndarray):  shape(n_epochs,n_channels,n_times)
			ica_ (bool): Whether to apply ICA.

		Returns:
			ndarray: An array of CCA results for each sample.
		"""
		ex = np.zeros((test_data.shape[0],self.n_event ))
		for i, i_data in enumerate(test_data):
			ex[i,:] = self._cca_ex(i_data, ica_)
		return ex