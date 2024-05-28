from scut_ssvep_aperiod.utils.common_function import ica_iclabel
from scipy import signal
class LoadDataBase:
	def __init__(self, data_path):
		"""
		:param data_path:      str      path of data
		"""
		self.data_path = data_path
		self.window_time = 4-0.14
		# self.sample_rate = None
		# self.split_data = []
		# self.label = []
		# self.n_epoch = None
		# self.n_channel = None


	@staticmethod
	def preprocess(raw, ica_=True, filter_para=None):
		"""
		:param raw:                inst  mne.io.BaseRaw      rawdata of mne
		:param ica_:               bool
		                           True  --- use ica remove niose
		                           False --- no use
		:param filter_para:        None/list
		                           Default None no filters
		                           list [low_fre, high_fre]
		:return:
		 raw :                     inst  mne.io.BaseRaw      rawdata after preprocess
		"""
		if filter_para is not None:
			raw = raw.copy().filter(filter_para[0], filter_para[1])
		if ica_:
			raw = ica_iclabel(raw, n_components=None, remove_label={'muscle artifact': 0.9, 'eye blink': 0.9, 'heart beat': 0.9})
		return raw

	def get_data(self, ica_=True, filter_para=None):
		pass



if __name__ == "__main__":
	LoadDataBase("D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\session1\s1\sess01_subj01_EEG_SSVEP.mat")
