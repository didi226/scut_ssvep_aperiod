import numpy as np
import scipy.io as sio
import pandas as pd
from mne.io import RawArray, read_raw_fif
from mne import create_info, find_events,Epochs,pick_types
from scut_ssvep_aperiod.utils.common_function import ica_iclabel
from scut_ssvep_aperiod.load_dataset.dataset_base import LoadDataBase
import random


class LoadDataKalungaOne(LoadDataBase):
	"""
	Class for loading and preprocessing SSVEP data from the KalungaOne dataset.

	Args:
		data_path (str): Path to the dataset file.

	Attributes:
		window_time (float): The time window for data processing (default is 5 seconds).
	"""
	def __init__(self, data_path):
		"""
		Initializes the LoadDataKalungaOne instance with a specified data path and sets the window time.

		Args:
			data_path (str): The path to the data file.
		"""
		super(LoadDataKalungaOne, self).__init__(data_path = data_path)
		self.window_time = 5


	def get_data(self, ica_ = True, filter_para = None, resample = None):
		"""
	   Loads and preprocesses the EEG data, extracts epochs, and returns the data and labels.

	   Args:
		   ica_ (bool, optional): Whether to apply ICA for noise removal. Defaults to True.
		   filter_para (list or None, optional): Frequency filter parameters. Defaults to None (no filtering applied).
		   resample (int or None, optional): Optionally resample the data. Defaults to None.

	   Returns:
		   np.ndarray: The preprocessed EEG data with shape (n_epochs, n_channels, n_times).
		   np.ndarray: Labels for the data indicating the event type (based on frequency).
	   """
		combine_raw = read_raw_fif(self.data_path, verbose = False, preload = True)
		combine_raw.info.set_montage("standard_1020")
		self.event_dict = {"13 Hz": 1, "17 Hz": 2, "21 Hz": 3}
		combine_raw = self.preprocess(combine_raw, ica_, filter_para)
		events = find_events(combine_raw, stim_channel = "STI 014")
		filtered_events = np.array([row for row in events if row[-1] != 4])
		epochs = Epochs(combine_raw, filtered_events, baseline = None, tmin = 0, tmax = 5-1/256, event_id = self.event_dict, reject = None)
		picks = pick_types(combine_raw.info, eeg = True, stim = False)
		self.split_data = epochs.get_data(picks = picks)

		self.info = combine_raw.info
		self.freqs = [13,17,21]

		self.sample_rate = combine_raw.info['sfreq']
		self.n_epoch = self.split_data.shape[0]
		self.n_channel = len(picks)
		self.label  = filtered_events[:, 2]-1
		return self.split_data, self.label

def get_data_path_list(form_path):
	"""
	Randomly marks two sessions per subject as effective in the input Excel file.

	Args:
	    form_path (str): Path to the Excel file containing subject and session information.

	Returns:
	    None. The modified Excel file is saved with an 'effectiveness' column indicating selected sessions.
	"""
	seednum = 42
	random.seed(seednum)
	np.random.seed(seednum)
	info_form = pd.read_excel(form_path)
	info_form['effectiveness'] = 0
	unique_subject_ids = info_form['subject_id'].unique()
	for subject_id in unique_subject_ids:
		subject_rows = info_form.loc[info_form['subject_id'] == subject_id]
		session_ids = subject_rows['session_id'].tolist()
		random_session_ids = random.sample(session_ids, 2)
		info_form.loc[(info_form['subject_id'] == subject_id) & (
			info_form['session_id'].isin(random_session_ids)), 'effectiveness'] = 1
	info_form.to_excel(form_path, index=False)

if __name__ == "__main__":
	ssvep_data_kalunga = LoadDataKalungaOne(data_path = r"D:\data\ssvep_dataset\MNE-ssvepexo-data\subject01\subject01_run1_raw.fif")
	x, y = ssvep_data_kalunga.get_data()
	print(x.shape, y.shape)
	# get_data_path_list("D:\data\ssvep_dataset\MNE-ssvepexo-data\ssvep_kang_sub_info.xlsx")


