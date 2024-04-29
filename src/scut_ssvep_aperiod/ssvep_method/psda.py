
from scut_ssvep_aperiod.ssvep_method.ssvep_methd_base import SSVEPMethodBase
from scut_ssvep_aperiod.fooof_parameter.decode_rebuild import BuildPSDPeriod
from scipy.stats import linregress
import numpy as np
import math
class PSDA(SSVEPMethodBase):
	def __init__(self, sfreq, ws, fres_list, n_harmonics, psd_type = "Ordinary",
	             psd_channel = "ave", psda_type = "direct_compare",freq_range=None,figure_=False,save_path_base=["__","__"]):
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
		y = self.estimate_psd_value(data_psd_channel, frequence, i_fre)
		denominator = [self.estimate_psd_value(data_psd_channel, frequence, i_fre + x * deltaf) for x in range(-5, 6)]
		snr = 20 * math.log10(10*y / (sum(denominator) - y))
		return snr

	def calculate_snr_hqy(self, data_psd_channel, frequence, i_fre, deltaf):
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
		psd_values,error,r_squa = self.psda_ex(psda_type = psda_type)
		label = np.argmax(psd_values)
		return label,error,r_squa

	def psd_original(self):
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
