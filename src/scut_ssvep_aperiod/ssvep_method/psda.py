
from scut_ssvep_aperiod.ssvep_method.ssvep_methd_base import SSVEPMethodBase
from scut_ssvep_aperiod.fooof_parameter.decode_rebuild import BuildPSDPeriod
from scipy.stats import linregress
import numpy as np
import math
class PSDA(SSVEPMethodBase):
	"""
	Class for Power Spectral Density Analysis (PSDA) of SSVEP data.

	Args:
		sfreq (float): Sampling frequency of the data.
		ws (float): Window size for analysis.
		fres_list (list): List of frequencies of interest.
		n_harmonics (int): Number of harmonics to consider.
		psd_type (str): Type of PSD calculation (default is "Ordinary").
		psd_channel (str): Channel type for PSD calculation (default is "ave").
		psda_type (str): Type of PSDA method to use (default is "direct_compare").
		freq_range (tuple, optional): Frequency range for analysis.
		figure_ (bool): Whether to generate figures (default is False).
		save_path_base (list): Base path for saving figures (default is ["__", "__"]).
	"""
	def __init__(self, sfreq, ws, fres_list, n_harmonics, psd_type = "Ordinary",
	             psd_channel = "ave", psda_type = "direct_compare",
				 freq_range=None,figure_=False,save_path_base=["__","__"]):
		super(PSDA, self).__init__(sfreq, ws, fres_list)
		self.n_harmonics = n_harmonics
		self.psd_type = psd_type
		self.psd_channel = psd_channel
		self.psda_type = psda_type
		self.deltaf = 1/ws
		self.freq_range = freq_range
		self.figure_ = figure_
		self.save_path_base = save_path_base
	def classify(self, data):
		"""
		Classifies the input data using PSDA.

		Args:
			data (numpy.ndarray): Input data for classification.

		Returns:
			tuple: Predicted labels, errors, and R-squared values for each trial.
		"""
		n_trials = data.shape[0]
		pred_label = np.zeros((n_trials))
		error = np.zeros((n_trials))
		r_squa = np.zeros((n_trials))
		for i, i_data in enumerate(data):
			PSD_temp = BuildPSDPeriod(i_data, self.sfreq)
			spectrum, freqs = PSD_temp.data_to_fft(psd_type = self.psd_type)
			psd_classify = PSDA_SSVEP(spectrum, freqs, self.fres_list, psd_channel=self.psd_channel, harmonic=self.n_harmonics,
			                          sfreq=self.sfreq, n_times=self.ws*self.sfreq, deltaf=self.deltaf,freq_range=self.freq_range,
			                          figure_ = self.figure_,save_path_base=[self.save_path_base,f'{i}.svg'])
			pred_label[i], error[i], r_squa[i] = psd_classify.psda_classify(psda_type = self.psda_type)
		return pred_label,error,r_squa
	def slope_estimation(self,data):
		"""
		Estimates the slope of the PSD for each trial.

		Args:
			data (numpy.ndarray): Input data for slope estimation.

		Returns:
			tuple: Errors and R-squared values for each trial.
		"""
		n_trials = data.shape[0]
		pred_label = np.zeros((n_trials))
		error = np.zeros((n_trials))
		r_squa = np.zeros((n_trials))
		for i, i_data in enumerate(data):
			PSD_temp = BuildPSDPeriod(i_data, self.sfreq)
			spectrum, freqs = PSD_temp.data_to_fft(psd_type=self.psd_type)
			error[i], r_squa[i] = PSD_temp.slope_estimate(spectrum, freqs,self.freq_range)
		return error,r_squa
	def calculate_snr(self,data):
		"""
		Calculates the signal-to-noise ratio (SNR) for each trial.

	   Args:
		   data (numpy.ndarray): Input data for SNR calculation.

	   Returns:
		   numpy.ndarray: SNR values for each frequency for all trials.
	   """
		n_trials = data.shape[0]
		pred_label = np.zeros((n_trials))
		psd_ex = np.zeros((n_trials,self.n_event))
		for i, i_data in enumerate(data):
			PSD_temp = BuildPSDPeriod(i_data, self.sfreq)
			spectrum, freqs = PSD_temp.data_to_fft(psd_type = self.psd_type)
			psd_classify = PSDA_SSVEP(spectrum, freqs, self.fres_list, psd_channel=self.psd_channel, harmonic=self.n_harmonics,
			                          sfreq=self.sfreq, n_times=self.ws*self.sfreq, deltaf=self.deltaf,freq_range=self.freq_range,
			                          figure_ = self.figure_,save_path_base=[self.save_path_base,f'{i}.svg'])
			psd_ex[i], _,_ = psd_classify.psda_ex(psda_type = self.psda_type)
		return psd_ex
class PSDA_SSVEP:
	"""
	Class for performing SSVEP-based PSD analysis.

	Args:
		data_psd (numpy.ndarray): Input PSD data.
		frequence (numpy.ndarray): Frequency array.
		fre_doi (list): Frequencies of interest for analysis.
		psd_channel (str): Channel type for PSD calculation (default is "ave").
		harmonic (int): Number of harmonics to consider (default is 4).
		sfreq (float): Sampling frequency (default is 250).
		n_times (int): Number of time points (default is 1000).
		deltaf (float): Frequency resolution (default is 0.25).
		freq_range (tuple, optional): Frequency range for analysis.
		figure_ (bool): Whether to generate figures (default is False).
		save_path_base (list): Base path for saving figures (default is ["__", "__"]).
	"""
	def __init__(self, data_psd, frequence, fre_doi, psd_channel="ave", harmonic=4,sfreq=250, n_times=1000,
	             deltaf=0.25, freq_range=None,figure_=False, save_path_base=["__","__"]):
		self.data_psd = data_psd
		self.frequence = frequence
		self.fre_doi = fre_doi
		self.psd_channel = psd_channel
		self.harmonic = harmonic
		self.n_channel, _ = data_psd.shape
		self.n_fre = len(fre_doi)
		self.sfreq = sfreq
		self.n_times = n_times
		self.deltaf = deltaf
		self.save_path_base = save_path_base
		self.freq_range = freq_range
		self.figure_ = figure_

	@staticmethod
	def estimate_psd_value(data_psd_i_channel, frequence, i_fre):
		"""
		Estimates the PSD value for a specific frequency.

		Args:
			data_psd_i_channel (numpy.ndarray): PSD values for a single channel.
			frequence (numpy.ndarray): Frequency array.
			i_fre (float): Frequency at which to estimate the PSD value.

		Returns:
			float: Estimated PSD value.
		"""
		index = np.where((frequence >= i_fre))[0][0]
		if index == 0:
			psd_value = data_psd_i_channel[0]
		elif index == len(frequence):
			psd_value = data_psd_i_channel[-1]
		else:
			x0, x2 = frequence[index - 1], frequence[index]
			y0, y2 = data_psd_i_channel[index - 1], data_psd_i_channel[index]
			psd_value = y0 + (y2 - y0) * (i_fre - x0) / (x2 - x0)
		return psd_value

	def calculate_snr(self, data_psd_channel, frequence, i_fre, deltaf):
		"""
		Calculates the signal-to-noise ratio (SNR) for a specific frequency.

		Args:
			data_psd_channel (numpy.ndarray): PSD values for a specific channel.
			frequence (numpy.ndarray): Frequency array.
			i_fre (float): Frequency at which to calculate SNR.
			deltaf (float): Frequency resolution.

		Returns:
			float: Calculated SNR value.
		"""
		y = self.estimate_psd_value(data_psd_channel, frequence, i_fre)
		denominator = [self.estimate_psd_value(data_psd_channel, frequence, i_fre + x * deltaf) for x in range(-5, 6)]
		snr = 20 * math.log10(10*y / (sum(denominator) - y))
		return snr

	def calculate_snr_hqy(self, data_psd_channel, frequence, i_fre, deltaf):
		"""
		Calculates the Signal-to-Noise Ratio (SNR) for a specific frequency.

		This method computes the SNR for a given frequency `i_fre` by finding the
		nearest frequency in the data and using neighboring frequencies as a noise
		baseline. If the power spectral density (PSD) has negative values, they are
		adjusted to avoid computation errors.

		Args:
			data_psd_channel (np.ndarray): Power spectral density values for a given channel.
			frequence (np.ndarray): Array of frequency values corresponding to `data_psd_channel`.
			i_fre (float): The frequency of interest for which SNR is calculated.
			deltaf (float): Frequency resolution or spacing used to estimate noise baseline.

		Returns:
			float: The calculated SNR in decibels (dB).

		Notes:
			- The method finds the frequency closest to `i_fre` and uses neighboring
			  frequencies (± deltaf) to estimate noise.
			- The SNR is computed in decibels using the formula:
				SNR = 20 * log10(8 * y / (sum(noise) - y))
			  where `y` is the PSD value at `i_fre`, and `noise` is the sum of PSD
			  values at neighboring frequencies.
		"""
		# idx = np.where((frequence >= i_fre-0.25) & (frequence <= i_fre+0.25))[0]
		# y = data_psd_channel[idx].max()
		# position = idx[np.argmax(data_psd_channel[idx])]

		min_value = np.min(data_psd_channel)
		if min_value <0:
			data_psd_channel = abs(min_value) + 0.000001 + data_psd_channel
		nearest_value = frequence[np.abs(frequence - i_fre).argmin()]
		position = np.where(frequence == nearest_value)[0]
		y = data_psd_channel[position]
		i_fre_new = frequence[position]
		denominator = [self.estimate_psd_value(data_psd_channel, frequence, i_fre_new + x * deltaf) for x in
		               range(-4, 5)]
		# denominator_2 = [self.estimate_psd_value(data_psd_channel, frequence, i_fre_new + x * deltaf) for x in
		#                range(-1, 2)]
		# denominator_2= sum(denominator_2)-y
		denominator_2 = 0
		snr = 20 * math.log10(8*y/ (sum(denominator) - y-denominator_2))
		return snr
	def psda_ex(self, psda_type= "direct_compare"):
		"""
	   Executes the PSDA analysis based on the specified method type.

	   Args:
		   psda_type (str): The type of PSDA method to use. Options include:
			   - "direct_compare": Direct comparison of PSD values.
			   - "snr": Signal-to-noise ratio analysis.
			   - "snr_hqy": SNR with high-quality estimates.
			   - "snr_hqy_ave_re": SNR with high-quality averaging, returning error and R-squared.
			   - "snr_hqy_ave_get": SNR high-quality averaging with different retrieval methods.

	   Returns:
		   numpy.ndarray: Computed PSD values.
		   float: Error metric (0 if not applicable).
		   float: R-squared value (0 if not applicable).
	   """
		error = 0
		r_squa = 0
		self.data_fft =np.sqrt(self.data_psd *(self.sfreq * self.n_times))
		if psda_type == "direct_compare":
			psd_values = self.psd_original()
		elif psda_type == "snr":
			psd_values = self.psd_snr()
		elif psda_type == "snr_hqy":
			psd_values = self.psd_snr_hqy()
		elif psda_type == "snr_hqy_ave_re":
			psd_values,error,r_squa = self.psd_snr_hqy_ave_re()
		elif psda_type == "snr_hqy_ave_get":
			psd_values = self.snr_hqy_ave_get()
		return psd_values,error,r_squa

	def psda_classify(self, psda_type= "direct_compare"):
		"""
		Classifies based on the PSD analysis result.

		Args:
			psda_type (str, optional): Type of PSD analysis to perform. Defaults to "direct_compare".

		Returns:
			label (int): Index of the maximum PSD value indicating the classification label.
			error (float): Error value from PSD analysis.
			r_squa (float): R-squared value from PSD analysis.
		"""
		psd_values,error,r_squa = self.psda_ex(psda_type = psda_type)
		label = np.argmax(psd_values)
		return label,error,r_squa

	def psd_original(self):
		"""
		Calculates the Power Spectral Density (PSD) values for each frequency of interest.

		If the psd_channel is not "ave", computes PSD for each channel and then averages. Otherwise, it averages across channels first.

		Returns:
			label (int): Index of the frequency with the highest PSD value.
		"""
		if self.psd_channel != "ave":
			psd_values = np.zeros((self.n_channel, self.n_fre))
			for i_channel in range(self.n_channel):
				data_psd_channel = self.data_fft[i_channel, :]
				for i, i_fre in enumerate(self.fre_doi):
					psd_values[i_channel, i] = sum(
						[self.estimate_psd_value(data_psd_channel, self.frequence, i_fre * x) for x in
						 range(1, self.harmonic + 1)])
			psd_values = np.mean(psd_values, axis=0)
		else:
			psd_values = np.zeros((self.n_fre))
			data_psd_channel = np.mean(self.data_fft, axis=0)
			for i, i_fre in enumerate(self.fre_doi):
				psd_values[i] = sum([self.estimate_psd_value(data_psd_channel, self.frequence, i_fre * x) for x in
				                     range(1, self.harmonic + 1)])
		label = np.argmax(psd_values)
		return label

	def psd_snr(self):
		"""
		Calculates the Signal-to-Noise Ratio (SNR) of the PSD for each frequency of interest.

		Returns:
			indicators_values (ndarray): SNR values across frequencies for each channel.
		"""
		deltaf = self.deltaf
		self.data_fft =abs(self.data_fft)
		if self.psd_channel != "ave":
			indicators_values = np.zeros((self.n_channel, self.n_fre))
			for i_channel in range(self.n_channel):
				data_psd_channel = self.data_fft[i_channel, :]
				print(i_channel)
				for i, i_fre in enumerate(self.fre_doi):
					indicators_values[i_channel, i] = sum([self.calculate_snr(data_psd_channel, self.frequence,
					                                                          i_fre * x, deltaf) for x in
					                                       range(1, self.harmonic + 1)])
			indicators_values = np.mean(indicators_values, axis=0)
			label = np.argmax(indicators_values)
		else:
			indicators_values = np.zeros((self.n_fre))
			data_psd_channel = np.mean(self.data_fft, axis=0)
			for i, i_fre in enumerate(self.fre_doi):
				indicators_values[i] = sum([self.calculate_snr(data_psd_channel, self.frequence,
				                                               i_fre * x, deltaf) for x in range(1, self.harmonic + 1)])
		return indicators_values

	def psd_snr_hqy(self):
		"""
		Calculates the SNR of the PSD using a harmonic approach for each frequency of interest.

		Returns:
			indicators_values (ndarray): Harmonic SNR values across frequencies for each channel.
		"""
		# deltaf = 0.25
		deltaf = self.deltaf
		if self.psd_channel != "ave":
			indicators_values = np.zeros((self.n_channel, self.n_fre))
			for i_channel in range(self.data_fft.shape[0]):
				data_psd_channel = self.data_fft[i_channel, :]
				print(i_channel)
				for i, i_fre in enumerate(self.fre_doi):
					indicators_values[i_channel, i] = sum([self.calculate_snr_hqy(data_psd_channel,
					                                                              self.frequence, i_fre * x, deltaf) for
					                                       x in range(1, self.harmonic + 1)])
			indicators_values = np.mean(indicators_values, axis=0)
			label = np.argmax(indicators_values)
		else:
			indicators_values = np.zeros((self.n_fre))
			data_psd_channel = np.mean(self.data_fft, axis=0)
			for i, i_fre in enumerate(self.fre_doi):
				indicators_values[i] = sum([self.calculate_snr_hqy(data_psd_channel,
				                                                   self.frequence, i_fre * x, deltaf) for x in
				                            range(1, self.harmonic + 1)])
			# label = np.argmax(indicators_values)
		return indicators_values



	def psd_snr_hqy_ave_re(self):
		"""
		Calculates the harmonic SNR using the averaged PSD after removing the aperiodic component.

	   Returns:
		   indicators_values (ndarray): Harmonic SNR values across frequencies.
		   error (float): Error value from PSD analysis.
		   r_squa (float): R-squared value from PSD analysis.
	   """
		deltaf = self.deltaf
		error = 0
		r_squa = 0
		indicators_values = np.zeros((self.n_fre))
		data_psd_channel = np.mean(self.data_fft, axis=0)
		data_build_psd_channel = BuildPSDPeriod(np.array([0, 1, 2, 3])[None, :], self.sfreq,save_path_base = self.save_path_base)
		data_psd_channel,error,r_squa = data_build_psd_channel.get_period_psd(data_psd_channel[None, :], self.frequence,
		                                    freq_range = self.freq_range, method = "remove_aperiodic", figure_ = self.figure_)
		data_psd_channel =  np.squeeze(data_psd_channel)
		del data_build_psd_channel
		for i, i_fre in enumerate(self.fre_doi):
			indicators_values[i] = sum([self.calculate_snr_hqy(data_psd_channel,
			                                self.frequence, i_fre * x, deltaf) for x in
			                            range(1, self.harmonic + 1)])
		return indicators_values, error,r_squa

	def snr_hqy_ave_get(self):
		"""
		Calculates the harmonic SNR using the averaged PSD with the aperiodic component.

		Returns:
			indicators_values (ndarray): Harmonic SNR values across frequencies.
		"""
		deltaf = self.deltaf
		indicators_values = np.zeros((self.n_fre))
		data_psd_channel = np.mean(self.data_fft, axis=0)
		data_build_psd_channel = BuildPSDPeriod(np.array([0, 1, 2, 3])[None, :], self.sfreq,self.save_path_base)
		data_psd_channel,_,_= data_build_psd_channel.get_period_psd(data_psd_channel[None, :], self.frequence, freq_range=self.freq_range,
		                                                         method = "get_aperiodic")
		data_psd_channel =  np.squeeze(data_psd_channel)
		del data_build_psd_channel
		for i, i_fre in enumerate(self.fre_doi):
			indicators_values[i] = sum([self.calculate_snr_hqy(data_psd_channel,
			                                self.frequence, i_fre * x, deltaf) for x in
			                            range(1, self.harmonic + 1)])
		return indicators_values
if __name__ == "__main__":
    from scut_ssvep_aperiod.load_dataset.dataset_lee import LoadDataLeeOne
    from scut_ssvep_aperiod.utils.common_function import cal_acc
    data_path = r"D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\session1\s1\sess01_subj01_EEG_SSVEP.mat"
    datasetone = LoadDataLeeOne(data_path)
    train_data, train_label, test_data, test_label = datasetone.get_data(pro_ica = True, filter_para = [3,40], resample=4)
    print(train_data.shape, train_label.shape,test_data.shape, test_label.shape)
    ssvep_method = PSDA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs, 3, psd_channel = "ave", psda_type = "snr_hqy_ave")
    predict_label = ssvep_method.classify(test_data)
    print(predict_label,test_label)
    acc = cal_acc(test_label, predict_label)
    print(acc)
