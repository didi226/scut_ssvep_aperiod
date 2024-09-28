from scut_ssvep_aperiod.utils.common_function import ica_iclabel
from scipy import signal
class LoadDataBase:
	"""
	Base class for loading and preprocessing SSVEP data.

	Args:
	    data_path (str): Path to the dataset file.

	Attributes:
	    data_path (str): Path to the dataset file.
	    window_time (float): The time window for data processing, default is 4 - 0.14 seconds.
	"""
	def __init__(self, data_path):
		"""
		Initializes the LoadDataBase instance with a specified data path.

		Args:
			data_path (str): The path to the data file.
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
		Preprocesses the raw EEG data by applying filtering and ICA for artifact removal.

		Args:
			raw (mne.io.BaseRaw): Raw EEG data in MNE format.
			ica_ (bool, optional): Whether to apply ICA for removing noise artifacts. Defaults to True.
								   - True: Apply ICA to remove artifacts (e.g., muscle, eye blink, heartbeat).
								   - False: Do not apply ICA.
			filter_para (list or None, optional): Frequency filter parameters. Defaults to None (no filtering applied).
												  - [low_fre, high_fre]: Apply band-pass filtering between low_fre and high_fre.

		Returns:
			mne.io.BaseRaw: The preprocessed raw EEG data after optional filtering and ICA.
		"""
		if filter_para is not None:
			raw = raw.copy().filter(filter_para[0], filter_para[1])
		if ica_:
			raw = ica_iclabel(raw, n_components=None, remove_label={'muscle artifact': 0.9, 'eye blink': 0.9, 'heart beat': 0.9})
		return raw

	def get_data(self, ica_=True, filter_para=None):
		"""
		Abstract method for loading and retrieving data.

		Args:
			ica_ (bool, optional): Whether to apply ICA in data preprocessing. Defaults to True.
			filter_para (list or None, optional): Frequency filter parameters. Defaults to None (no filtering applied).

		Raises:
			NotImplementedError: To be implemented in subclasses that handle specific data formats.
		"""
		pass



if __name__ == "__main__":
	LoadDataBase("D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\session1\s1\sess01_subj01_EEG_SSVEP.mat")
