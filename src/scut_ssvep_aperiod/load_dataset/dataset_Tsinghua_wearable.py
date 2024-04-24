import os
import numpy as np
import scipy.io as sio
from mne.io import RawArray
from mne import create_info,EpochsArray
from mne.filter import filter_data
from scut_ssvep_aperiod.load_dataset.dataset_base import LoadDataBase
from scut_ssvep_aperiod.fooof_parameter.decode_rebuild import reconstruct_signal
from einops import rearrange

class LoadDataTHWOne(LoadDataBase):
	def __init__(self, data_path):
		"""
		:param data_path:  str       path of data
		:param info_path:  str       path of info file(.mat)
		"""
		super(LoadDataTHWOne, self).__init__(data_path=data_path)
		self.window_time = 2
		self._get_info()
	def _get_info(self):
		"""
		get info
		:return:
		"""
		self.sample_rate = 250
		self.ch_names = ['POz', 'PO3', 'PO4', 'PO5', 'PO6', 'Oz', 'O1', 'O2']
		self.ch_types = 8 * ['eeg']
		self.freqs = [9.25,11.25,13.25]
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




	def _load_data_from_mat(self, pro_ica=True, filter_para=None, resample=None, reconstruct_=False, picks=['POz', 'PO3', 'PO4', 'PO5', 'PO6', 'Oz', 'O1', 'O2']):
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
		                                                Default ['POz', 'PO3', 'PO4', 'PO5', 'PO6', 'Oz', 'O1', 'O2']
		:return:
		"""
		file_data_test = np.squeeze(sio.loadmat(self.data_path)['data'][:,int(0.64*self.sample_rate):int(2.64*self.sample_rate),0,5:,:3])
		file_data_train = np.squeeze(sio.loadmat(self.data_path)['data'][:,int(0.64*self.sample_rate):int(2.64*self.sample_rate),0,:5,:3])
		self.data_test = rearrange(file_data_test, 'n_channel n_times n_blocks n_target -> (n_blocks n_target) n_channel n_times')
		self.data_train = rearrange(file_data_train,'n_channel n_times n_blocks n_target -> (n_blocks n_target) n_channel n_times')
		self.sample_rate_train = 250
		self.sample_rate_test = 250
		if resample is not None:
			self.data_test = self.data_test[:,:,::resample]
			self.data_train = self.data_train[:,:,::resample]
			self.sample_rate_train = self.sample_rate_train/resample
			self.sample_rate_test = self.sample_rate_test/resample
		train_epochs = EpochsArray(self.data_train, self.info)
		test_epochs = EpochsArray(self.data_test, self.info)
		if reconstruct_:
			train_epochs = self.preprocess(train_epochs,pro_ica,None)
			test_epochs = self.preprocess(test_epochs, pro_ica, None)
		else:
			train_epochs = self.preprocess(train_epochs, pro_ica, filter_para)
			test_epochs = self.preprocess(test_epochs, pro_ica, filter_para)
		self.data_test = test_epochs.get_data()
		self.data_train = train_epochs.get_data()
		arrays = [np.arange(3) for _ in range(5)]
		label = np.concatenate(arrays)
		self.label_test = label
		self.label_train = label
		self.n_epoch_train = self.data_train.shape[0]
		self.n_channel_train = self.data_train.shape[1]
		self.n_epoch_test = self.data_test.shape[0]
		self.n_channel_test = self.data_test.shape[1]




	def get_data(self, pro_ica=True, filter_para=None, resample=None, reconstruct_=False,
	             reconstruct_type=0, picks=['P7','P3','Pz','P4','P8','PO9','O1','Oz','O2','PO10']):
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
		self.event_dict = {"9.25 Hz": 0, "11.25 Hz": 1, "13.25 Hz": 2}
		name_base = os.path.basename(self.data_path).replace('.mat', '')
		path_root = os.path.dirname(self.data_path)
		save_path_name = (name_base +
		                  f"pro_ica_{pro_ica}_filter_{filter_para}_resample_{resample}_reconstruct_{reconstruct_}_reconstruct_type{reconstruct_type}.npz")
		save_path = os.path.join(path_root, save_path_name)
		if not os.path.exists(save_path):
			save_name_before_reconstruct = (name_base + f"pro_ica_{pro_ica}_filter_{None}_resample_{resample}_reconstruct_{False}_reconstruct_type{None}.npz")
			save_path_before_reconstruct = os.path.join(path_root, save_name_before_reconstruct)
			if  reconstruct_ and os.path.exists(save_path_before_reconstruct):
				self._load_data_from_npz(save_path_before_reconstruct)
			else:
				self._load_data_from_mat(pro_ica, filter_para, resample, reconstruct_, picks)
			if reconstruct_:
				self.data_test, self.label_test = reconstruct_signal(self.data_test, self.label_test,
				                self.sample_rate_test, method = reconstruct_, phase_invariance = reconstruct_type)

				self.data_train, self.label_train = reconstruct_signal(self.data_train, self.label_train,
				                self.sample_rate_train, method = reconstruct_, phase_invariance = reconstruct_type)
				if filter_para is not None:
					self.data_test = filter_data(self.data_test, self.sample_rate_test, filter_para[0], filter_para[1])
					self.data_train = filter_data(self.data_train, self.sample_rate_train, filter_para[0], filter_para[1])
			np.savez(save_path, data_test = self.data_test, label_test = self.label_test,  n_epoch_test = self.n_epoch_test,
			         n_channel_test = self.n_channel_test, sample_rate_test = self.sample_rate_test,
			         data_train = self.data_train, label_train = self.label_train, n_epoch_train = self.n_epoch_train,
			         n_channel_train = self.n_channel_train, sample_rate_train = self.sample_rate_train)
		else:
			self._load_data_from_npz(save_path)
		return self.data_train, self.label_train, self.data_test, self.label_test

if __name__ == "__main__":
	ssvep_data_lee = LoadDataTHWOne(data_path = r"D:\data\ssvep_dataset\Tsinghua_dataset_ssvep_wearable\ssvep_data\S001\S001.mat")
	data_train, label_train, data_test, label_test = ssvep_data_lee.get_data(pro_ica=True,filter_para=[1,45], resample=None,reconstruct_=False, reconstruct_type=0)
	print(data_train.shape,label_train.shape,data_test.shape, label_test.shape)
