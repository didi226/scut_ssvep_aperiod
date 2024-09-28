import numpy as np
import math
from scipy import signal
from sklearn.cross_decomposition import CCA
from scut_ssvep_aperiod.ssvep_method.ssvep_methd_base import CCABase
from scut_ssvep_aperiod.utils.common_function import cal_acc


class FBCCA(CCABase):
	def __init__(self, sfreq, ws, fres_list, n_harmonics, Nc=9, Nm=5,
				 passband=[6, 14, 22, 30, 38],
	             stopband=[4, 10, 16, 24, 32],
	             high_cut_pass=40, high_cut_stop=50):
		"""
		Initializes the FBCCA class for frequency band Canonical Correlation Analysis (FBCCA).
		Different filter banks need to be designed for different datasets

		Args:
			sfreq (float): Sampling frequency.
			ws (int): Window size.
			fres_list (list): List of frequency results.
			n_harmonics (int): Number of harmonics.
			Nc (int): Number of channels (default: 9).
			Nm (int): Number of frequency bands (default: 5).
			passband (list): List of passband frequencies (default: [6, 14, 22, 30, 38]).
			stopband (list): List of stopband frequencies (default: [4, 10, 16, 24, 32]).
			high_cut_pass (float): High cut pass frequency (default: 40).
			high_cut_stop (float): High cut stop frequency (default: 50).
		"""
		super(FBCCA, self).__init__(sfreq, ws, fres_list, n_harmonics)
		self.Nc = Nc
		self.Nm = Nm
		self.Nf = len(fres_list)
		self.pass_band = passband
		self.stop_band = stopband
		self.high_cut_pass = high_cut_pass
		self.high_cut_stop = high_cut_stop

	def filter_bank(self, eeg):
		"""
		Applies a filter bank to the EEG data.

		Args:
			eeg (ndarray): Input EEG data with shape (n_epoch, n_channels, n_times).

		Returns:
			ndarray: Filtered data with shape (n_epoch, Nm, n_channels, n_times).
		"""
		result = np.zeros((eeg.shape[0], self.Nm, eeg.shape[-2], self.T))
		nyq = self.sfreq / 2

		# high_cut_pass, high_cut_stop = 40, 50
		gpass, gstop, rp = 3, 40, 0.5

		for i in range(self.Nm):
			wp = np.array([self.pass_band[i] / nyq, self.high_cut_pass / nyq])
			ws = np.array([self.stop_band[i] / nyq, self.high_cut_stop / nyq])
			[n, wn] = signal.cheb1ord(wp, ws, gpass, gstop)
			[b, a] = signal.cheby1(n, rp, wn, 'bandpass')
			data = signal.filtfilt(b, a, eeg, padlen=3 * (max(len(b), len(a)) - 1)).copy()
			result[:, i, :, :] = data
		return result

	def classify(self, test_data):
		"""
		Classifies the test data using FBCCA.

		Args:
			test_data (ndarray): Input test data with shape (n_epochs, n_channels, n_times).

		Returns:
			ndarray: An array of predicted class labels for each segment.
		"""
		reference_signals = self.get_reference_signal()
		test_data = self.filter_bank(test_data)
		predicted_class = []
		self.result_ex = []
		num_segments = test_data.shape[0]
		fb_weight = [math.pow(i, -1.25) + 0.25 for i in range(1, self.Nm + 1)]
		for segment in range(num_segments):
			result = np.zeros(self.Nf)
			for fb_i in range(self.Nm):
				x = test_data[segment, fb_i]
				y = reference_signals
				w = fb_weight[fb_i]
				result += (w * (self.find_correlation(1, x, y) ** 2))
			self.result_ex.append(result)
			predicted_class.append(np.argmax(result))
		predicted_class = np.array(predicted_class)
		self.result_ex = np.array(self.result_ex)
		return predicted_class


	def calculate_ex(self):
		"""
		Returns the results of the classification experiments.

		Returns:
			ndarray: The results of the classification experiments.
		"""
		return self.result_ex


if __name__ == "__main__":
	from scut_ssvep_aperiod.load_dataset.dataset_lee import LoadDataLeeOne
	data_path = r"D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\session1\s1\sess01_subj01_EEG_SSVEP.mat"
	datasetone = LoadDataLeeOne(data_path)
	train_data, train_label, test_data, test_label = datasetone.get_data(pro_ica=False, filter_para=[3, 40], resample=4)
	print(train_data.shape, train_label.shape, test_data.shape, test_label.shape)
	ssvep_method = FBCCA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs, 3)
	predict_label = ssvep_method.classify(test_data)
	print(predict_label, test_label)
	acc = cal_acc(test_label, predict_label)
	print(acc)
