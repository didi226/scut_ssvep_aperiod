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
		:param data_path:  str       path of data
		:param info_path:  str       path of info file(.mat)
		"""
		super(LoadDataLeeOne, self).__init__(data_path=data_path)
		self.window_time = 4 - 0.14
		self.info_path = info_path
		self._get_info()
	def _get_info(self):
		"""
		get info from info file
		:return:
		"""
		info_data = sio.loadmat(self.info_path)['info']
		self.sample_rate = info_data ['fs'][0][0][0][0]
		self.ch_names = [item[0] for item in info_data ['chan'][0][0][0]]
		# Delete non 10-20 standard channels
		delect_channel =['FTT9h', 'TTP7h', 'TPP9h', 'FTT10h', 'TPP8h', 'TPP10h']
		indices_to_remove = [self.ch_names.index(i_channel) for i_channel in delect_channel]
		for index in sorted(indices_to_remove, reverse = True):
			del self.ch_names[index]
		self.ch_types = (len(self.ch_names)) * ['eeg']
		self.freqs = [60.0/5.0, 60.0/7.0, 60.0/9.0, 60.0/11.0]
		self.info = create_info(self.ch_names, ch_types = self.ch_types, sfreq = self.sample_rate)
		self.info.set_montage("standard_1020")
	def _load_data_from_npz(self, path):
		"""
		Load the data from a npz file (preprosess)
		:param path:              str            path to the npz file
		:return:
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

	def _load_data_from_structure(self, file_data, pro_ica = True, filter_para = None, resample = None,
	                              picks = ['P7','P3','Pz','P4','P8','PO9','O1','Oz','O2','PO10']):
		"""
		read data from the structure in .mat
		:param file_data:
		:param pro_ica:                bool            whether to do ica in propresess
	    :param filter_para:            None/list       Default None  no filters
	                                                   [low_freq, high_freq]
		:param resample:               None/int        Default None no resample
		                                               int the factor of resampling
		:param reconstruct_:          None/str         Default None  no reconstruct
	                                                   "remove_aperiodic" ---- reconstruct time signals and remove_aperiodic
	                                                   "get_periodic" ---- reconstruct time signals and get_periodic
	                                                   "get_aperiodic" ---- reconstruct time signals and get_aperiodic
		:param picks:                list              channels to select
		                                               Default ['P7','P3','Pz','P4','P8','PO9','O1','Oz','O2','PO10']
		:return:
		split_data                   numpy array       shape (n_epochs,n_channels,n_samples)
	    label                        numpy array       shape (n_epochs,)
		n_epoch                      int               the number of epochs
		n_channel                    int               the number of channels
		sample_rate                  float             the sampling rate after resampling
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
		x = combine_raw.get_data(picks = picks)
		# 分割数据
		split_data = np.zeros((n_epoch, n_channel, sig_len))
		for t_idx, start_t in enumerate(t):
			start_t = start_t + 0.14*self.sample_rate
			end_t = np.floor(start_t + sig_len)
			split_data[t_idx, :, :] = x[:, int(start_t):int(end_t)]
		if resample is not None:
			split_data = split_data[:,:, ::resample]
			# split_data = signal.decimate(split_data, resample, axis =2)
			sample_rate = self.sample_rate / resample
		return split_data, label, n_epoch, n_channel, sample_rate


	def _load_data_from_mat (self, pro_ica=True, filter_para=None, resample=None, picks=['P7','P3','Pz','P4','P8','PO9','O1','Oz','O2','PO10']):
		"""
		Load dataset from mat file
		:param pro_ica:                bool            whether to do ica in propresess
		:param filter_para:            None/list       Default None  no filters
	                                                   [low_freq, high_freq]
		:param resample:               None/int        Default None no resample
		                                               int the factor of resampling
		:param reconstruct_:           None/str         Default None  no reconstruct
	                                                   "remove_aperiodic" ---- reconstruct time signals and remove_aperiodic
	                                                   "get_periodic" ---- reconstruct time signals and get_periodic
	                                                   "get_aperiodic" ---- reconstruct time signals and get_aperiodic
		:param picks:                  list             channels to select
		                                                Default ['P7','P3','Pz','P4','P8','PO9','O1','Oz','O2','PO10']
		:return:
		"""
		file_data_test = sio.loadmat(self.data_path)['EEG_SSVEP_test']
		file_data_train = sio.loadmat(self.data_path)['EEG_SSVEP_train']
		self.data_test, self.label_test, self.n_epoch_test, self.n_channel_test, self.sample_rate_test = self._load_data_from_structure(file_data_test,
		        pro_ica = pro_ica, filter_para = filter_para, resample = resample, picks = picks)
		self.data_train, self.label_train, self.n_epoch_train, self.n_channel_train, self.sample_rate_train = self._load_data_from_structure(file_data_train,
				pro_ica = pro_ica, filter_para = filter_para, resample = resample, picks = picks)

	def get_data(self, pro_ica=True, filter_para=None, resample=None, reconstruct_=False,
	             reconstruct_type=0, freq_range=None, picks=['P7','P3','Pz','P4','P8','PO9','O1','Oz','O2','PO10']):
		"""
		get data after preprosess
		:param pro_ica:                bool            whether to do ica in propresess
		:param filter_para:            None/list       Default None  no filters
	                                                   [low_freq, high_freq]
		:param resample:               None/int        Default None no resample
		                                               int the factor of resampling
		:param reconstruct_:           None/str         Default None  no reconstruct
	                                                   "remove_aperiodic" ---- reconstruct time signals and remove_aperiodic
	                                                   "get_periodic" ---- reconstruct time signals and get_periodic
	                                                   "get_aperiodic" ---- reconstruct time signals and get_aperiodic
		:param picks:                  list             channels to select
		                                                Default ['P7','P3','Pz','P4','P8','PO9','O1','Oz','O2','PO10']
		:return:
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
			if  reconstruct_ and os.path.exists(save_path_before_reconstruct):
				self._load_data_from_npz(save_path_before_reconstruct)
			else:
				self._load_data_from_mat(pro_ica, filter_para, resample, picks)
			if reconstruct_:
				self.data_test, self.label_test = reconstruct_signal(self.data_test, self.label_test,
				                self.sample_rate_test, method = reconstruct_, phase_invariance = reconstruct_type)

				self.data_train, self.label_train = reconstruct_signal(self.data_train, self.label_train,
				                self.sample_rate_train, method = reconstruct_, phase_invariance = reconstruct_type)
			np.savez(save_path, data_test = self.data_test, label_test = self.label_test,  n_epoch_test = self.n_epoch_test,
			         n_channel_test = self.n_channel_test, sample_rate_test = self.sample_rate_test,
			         data_train = self.data_train, label_train = self.label_train, n_epoch_train = self.n_epoch_train,
			         n_channel_train = self.n_channel_train, sample_rate_train = self.sample_rate_train)
		else:
			self._load_data_from_npz(save_path)
		return self.data_train, self.label_train, self.data_test, self.label_test

if __name__ == "__main__":
	ssvep_data_lee = LoadDataLeeOne(data_path = r"D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\session1\s1\sess01_subj01_EEG_SSVEP.mat")
	x, y = ssvep_data_lee.get_data(pro_ica=True, resample=4)
	print(x.shape,y.shape)
