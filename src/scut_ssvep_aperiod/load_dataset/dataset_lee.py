import os
import numpy as np
import scipy.io as sio
from mne.io import RawArray
from mne import create_info
from mne.filter import filter_data
from scut_ssvep_aperiod.load_dataset.dataset_base import LoadDataBase
from scut_ssvep_aperiod.fooof_parameter.decode_rebuild import reconstruct_signal


class LoadDataLeeOne(LoadDataBase):
	def __init__(self, data_path, info_path=r"D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\info_ssvep_lee_dataset.mat"):
		"""
		Initializes the LoadDataLeeOne instance.

		Args:
			data_path (str): Path to the data.
			info_path (str): Path to the info file (.mat).
		"""
		super(LoadDataLeeOne, self).__init__(data_path=data_path)
		self.window_time = 4 - 0.14
		self.info_path = info_path
		self._get_info()

	def _get_info(self):
		"""Gets the info from the info file."""
		info_data = sio.loadmat(self.info_path)['info']
		self.sample_rate = info_data['fs'][0][0][0][0]
		self.ch_names = [item[0] for item in info_data['chan'][0][0][0]]
		# Delete non 10-20 standard channels
		delect_channel = ['FTT9h', 'TTP7h', 'TPP9h', 'FTT10h', 'TPP8h', 'TPP10h']
		indices_to_remove = [self.ch_names.index(i_channel) for i_channel in delect_channel]
		for index in sorted(indices_to_remove, reverse=True):
			del self.ch_names[index]
		self.ch_types = (len(self.ch_names)) * ['eeg']
		self.freqs = [60.0 / 5.0, 60.0 / 7.0, 60.0 / 9.0, 60.0 / 11.0]
		self.info = create_info(self.ch_names, ch_types=self.ch_types, sfreq=self.sample_rate)
		self.info.set_montage("standard_1020")

	def _load_data_from_npz(self, path):
		"""
		Loads the data from a npz file (preprocess).

		Args:
			path (str): Path to the npz file.

		Attributes:
			data_test (numpy.ndarray): Test data.
			label_test (numpy.ndarray): Test labels.
			n_epoch_test (int): Number of test epochs.
			n_channel_test (int): Number of test channels.
			sample_rate_test (int): Sample rate for test data.
			data_train (numpy.ndarray): Training data.
			label_train (numpy.ndarray): Training labels.
			n_epoch_train (int): Number of training epochs.
			n_channel_train (int): Number of training channels.
			sample_rate_train (int): Sample rate for training data.
		"""
		loaded_data = np.load(path)
		self.data_test = loaded_data['data_test']
		self.label_test = loaded_data['label_test']
		self.n_epoch_test = int(loaded_data['n_epoch_test'])
		self.n_channel_test = int(loaded_data['n_channel_test'])
		self.sample_rate_test = int(loaded_data['sample_rate_test'])
		self.data_train = loaded_data['data_train']
		self.label_train = loaded_data['label_train']
		self.n_epoch_train = int(loaded_data['n_epoch_train'])
		self.n_channel_train = int(loaded_data['n_channel_train'])
		self.sample_rate_train = int(loaded_data['sample_rate_train'])

	def _load_data_from_structure(self, file_data, pro_ica=True, filter_para=None, resample=None,
	                              picks=['P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10']):
		"""
		Reads data from the structure in .mat file.

		Args:
			file_data (dict): Data loaded from .mat file.
			pro_ica (bool): Whether to perform ICA in preprocessing.
			filter_para (None or list): Filter parameters, default is None (no filters).
										 [low_freq, high_freq].
			resample (None or int): Factor for resampling, default is None (no resample).
			picks (list): Channels to select, default is ['P7','P3','Pz','P4','P8','PO9','O1','Oz','O2','PO10'].

		Returns:
			split_data (numpy.ndarray): Data split into shape (n_epochs, n_channels, n_samples).
			label (numpy.ndarray): Labels of the data.
			n_epoch (int): Number of epochs.
			n_channel (int): Number of channels.
			sample_rate (float): Sampling rate after resampling.
		"""
		sig_len = int(self.window_time * self.sample_rate)
		x = file_data['x'][0][0].T
		x = np.delete(x, [45, 46, 48, 50, 51, 53], axis=0)
		t = file_data['t'][0][0][0]
		label = np.squeeze(file_data['y_dec'][0][0]) - 1
		n_epoch = t.shape[0]
		n_channel = min(x.shape[0], len(picks))
		combine_raw = RawArray(x, self.info)
		combine_raw = self.preprocess(combine_raw, pro_ica, filter_para)
		x = combine_raw.get_data(picks=picks)
		# 分割数据
		split_data = np.zeros((n_epoch, n_channel, sig_len))
		for t_idx, start_t in enumerate(t):
			start_t = start_t + 0.14 * self.sample_rate
			end_t = np.floor(start_t + sig_len)
			split_data[t_idx, :, :] = x[:, int(start_t):int(end_t)]
		if resample is not None:
			split_data = split_data[:, :, ::resample]
			# split_data = signal.decimate(split_data, resample, axis =2)
			sample_rate = self.sample_rate / resample
		return split_data, label, n_epoch, n_channel, sample_rate

	def _load_resting_state_data_from_structure(self, file_data, pro_ica=True, filter_para=None, resample=None,
	                                            picks=None):
		"""
		Reads resting state data from the structure in .mat file.

		Args:
			file_data (dict): Data loaded from .mat file.
			pro_ica (bool): Whether to perform ICA in preprocessing.
			filter_para (None or list): Filter parameters, default is None (no filters).
										 [low_freq, high_freq].
			resample (None or int): Factor for resampling, default is None (no resample).
			picks (list): Channels to select, default is ['P7','P3','Pz','P4','P8','PO9','O1','Oz','O2','PO10'].

		Returns:
			pre_rest_data (numpy.ndarray): Pre-resting state data.
			post_rest_data (numpy.ndarray): Post-resting state data.
		"""
		sig_len = int(self.window_time * self.sample_rate)
		pre_rest_data = file_data['pre_rest'][0][0].T
		post_rest_data = file_data['post_rest'][0][0].T
		pre_rest_data = np.delete(pre_rest_data, [45, 46, 48, 50, 51, 53], axis=0)
		post_rest_data = np.delete(post_rest_data, [45, 46, 48, 50, 51, 53], axis=0)
		pre_raw = RawArray(pre_rest_data, self.info)
		post_raw = RawArray(post_rest_data, self.info)
		pre_raw = self.preprocess(pre_raw, pro_ica, filter_para)
		post_raw = self.preprocess(post_raw, pro_ica, filter_para)
		pre_rest_data = pre_raw.get_data(picks=picks)
		post_rest_data = post_raw.get_data(picks=picks)
		if resample is not None:
			pre_rest_data = pre_rest_data[:, ::resample]
			post_rest_data = post_rest_data[:, ::resample]
		return pre_rest_data, post_rest_data

	def _load_data_from_mat(self, pro_ica=True, filter_para=None, resample=None,
	                        picks=['P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10']):
		"""
		Loads dataset from .mat file.

		Args:
		    pro_ica (bool): Whether to perform ICA in preprocessing.
		    filter_para (None or list): Filter parameters, default is None (no filters).
		                                 [low_freq, high_freq].
		    resample (None or int): Factor for resampling, default is None (no resample).
		    picks (list): Channels to select, default is ['P7','P3','Pz','P4','P8','PO9','O1','Oz','O2','PO10'].

		Returns:
		    None: Loads data into instance variables.
		"""
		file_data_test = sio.loadmat(self.data_path)['EEG_SSVEP_test']
		file_data_train = sio.loadmat(self.data_path)['EEG_SSVEP_train']
		self.data_test, self.label_test, self.n_epoch_test, self.n_channel_test, self.sample_rate_test = self._load_data_from_structure(
			file_data_test,
			pro_ica=pro_ica, filter_para=filter_para, resample=resample, picks=picks)
		self.data_train, self.label_train, self.n_epoch_train, self.n_channel_train, self.sample_rate_train = self._load_data_from_structure(
			file_data_train,
			pro_ica=pro_ica, filter_para=filter_para, resample=resample, picks=picks)

	def _load_resting_state_data_from_mat(self, pro_ica=True, filter_para=None, resample=None, picks=None):
		"""
		Load resting state dataset from a MAT file.

		Args:
			pro_ica (bool): If True, performs Independent Component Analysis (ICA) during preprocessing.
			filter_para (list or None): Frequency filter parameters, specified as [low_freq, high_freq].
										 Default is None (no filters).
			resample (int or None): Resampling factor. If None, no resampling is performed.
			picks (list): Channels to select. Default is
						  ['P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10'].

		Returns:
			tuple: Preprocessed training and testing data for the resting state.
		"""
		file_data_test = sio.loadmat(self.data_path)['EEG_SSVEP_test']
		file_data_train = sio.loadmat(self.data_path)['EEG_SSVEP_train']
		pre_data_test, post_data_test = self._load_resting_state_data_from_structure(file_data_test,
		                                                                             pro_ica=pro_ica,
		                                                                             filter_para=filter_para,
		                                                                             resample=resample, picks=picks)
		pre_data_train, post_data_train = (
			self._load_resting_state_data_from_structure(file_data_train,
			                                             pro_ica=pro_ica, filter_para=filter_para, resample=resample,
			                                             picks=picks))
		return pre_data_train, post_data_train, pre_data_test, post_data_test

	def get_data(self, pro_ica=True, filter_para=None, resample=None, reconstruct_=False,
	             reconstruct_type=0, freq_range=None,
	             picks=['P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10']):
		"""
		Retrieve and preprocess EEG data.

		Args:
			pro_ica (bool): If True, performs Independent Component Analysis (ICA) during preprocessing.
			filter_para (list or None): Frequency filter parameters, specified as [low_freq, high_freq].
										 Default is None (no filters).
			resample (int or None): Resampling factor. If None, no resampling is performed.
			reconstruct_ (str or None): Reconstruction method. Options include:
										 "remove_aperiodic", "get_periodic", "get_aperiodic".
										 Default is None (no reconstruction).
			reconstruct_type (int): Type of reconstruction phase invariance. Default is 0.
			freq_range (None or list): Frequency range for filtering. Default is None (no filtering).
			picks (list): Channels to select. Default is
						  ['P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10'].

		Returns:
			tuple: Preprocessed training and testing data along with their labels.
		"""
		self.event_dict = {"12 Hz": 1, "8.57 Hz": 2, "6.67 Hz": 3, "5.45Hz": 4}
		name_base = os.path.basename(self.data_path).replace('EEG_SSVEP.mat', '')
		path_root = os.path.dirname(self.data_path)
		save_path_name = (name_base + f"pro_ica_{pro_ica}_filter_{filter_para}_resample_{resample}_reconstruct_"
		                              f"{reconstruct_}_reconstruct_type{reconstruct_type}_freq_range{freq_range}.npz")
		save_path = os.path.join(path_root, save_path_name)
		if not os.path.exists(save_path):
			save_name_before_reconstruct = (name_base + f"pro_ica_{pro_ica}_filter_{filter_para}_resample_"
			                                            f"{resample}_reconstruct_{False}_reconstruct_type{None}_freq_range{None}.npz")
			save_path_before_reconstruct = os.path.join(path_root, save_name_before_reconstruct)
			if reconstruct_ and os.path.exists(save_path_before_reconstruct):
				self._load_data_from_npz(save_path_before_reconstruct)
			else:
				self._load_data_from_mat(pro_ica, filter_para, resample, picks)
			if reconstruct_:
				self.data_test, self.label_test = reconstruct_signal(self.data_test, self.label_test,
				                                                     self.sample_rate_test, method=reconstruct_,
				                                                     phase_invariance=reconstruct_type)

				self.data_train, self.label_train = reconstruct_signal(self.data_train, self.label_train,
				                                                       self.sample_rate_train, method=reconstruct_,
				                                                       phase_invariance=reconstruct_type)
			np.savez(save_path, data_test=self.data_test, label_test=self.label_test, n_epoch_test=self.n_epoch_test,
			         n_channel_test=self.n_channel_test, sample_rate_test=self.sample_rate_test,
			         data_train=self.data_train, label_train=self.label_train, n_epoch_train=self.n_epoch_train,
			         n_channel_train=self.n_channel_train, sample_rate_train=self.sample_rate_train)
		else:
			self._load_data_from_npz(save_path)
		return self.data_train, self.label_train, self.data_test, self.label_test

	def get_data_resting_state(self, pro_ica=True, filter_para=None, resample=None, picks=None):
		"""
		Get resting state data after preprocessing.

		Args:
			pro_ica (bool): If True, performs Independent Component Analysis (ICA) during preprocessing.
			filter_para (list or None): Frequency filter parameters, specified as [low_freq, high_freq].
										 Default is None (no filters).
			resample (int or None): Resampling factor. If None, no resampling is performed.
			picks (list): Channels to select. Default is
						  ['P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10'].

		Returns:
			tuple: Preprocessed training and testing data for the resting state.
		"""
		pre_data_train, post_data_train, pre_data_test, post_data_test = self._load_resting_state_data_from_mat(pro_ica,
		                                                                                                        filter_para,
		                                                                                                        resample,
		                                                                                                        picks)
		return pre_data_train, post_data_train, pre_data_test, post_data_test


if __name__ == "__main__":
	ssvep_data_lee = LoadDataLeeOne(
		data_path=r"D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\session1\s1\sess01_subj01_EEG_SSVEP.mat")
	pre_data_train, post_data_train, pre_data_test, post_data_test = ssvep_data_lee.get_data_resting_state(pro_ica=True,filter_para=[1, 40], resample=4)
	print(pre_data_train.shape, post_data_train.shape)
