import os.path
from fooof import FOOOFGroup,FOOOF
from scipy.stats import norm
import numpy as np
from fooof.utils import trim_spectrum, interpolate_spectrum
from fooof.plts.spectra import plot_spectra
import matplotlib.pyplot as plt
import datetime
from fooof.bands import Bands
from fooof.objs.utils import average_fg
from scipy.stats import linregress
def reconstruct_signal(data, label, sfreq, method="remove_aperiodic", phase_invariance=2,freq_range=None):
	"""
	Reconstruct signals by extracting periodic and aperiodic components from time series data.

	Args:
		data (numpy.ndarray): Time series data of shape (n_epoch, n_channels, n_times).
		label (numpy.ndarray): Labels of shape (n_epoch,).
		sfreq (float): Sampling frequency of the signal.
		method (str): Reconstruction method. Options:
			"remove_aperiodic": Reconstruct time signal and remove aperiodic components.
			"get_periodic": Reconstruct time signal and extract periodic components.
			"get_aperiodic": Reconstruct time signal and extract aperiodic components.
		phase_invariance (int): Phase invariance option:
			0: Use original phase.
			2: Use zero phase.
		freq_range (list, optional): Frequency range for reconstruction.

	Returns:
		tuple: A tuple containing:
			- numpy.ndarray: Reconstructed data of shape (n_epoch, n_channels, n_times).
			- numpy.ndarray: New labels of shape (n_epoch,).
	"""
	reconstruct_data = []
	new_label = []
	for i_data, i_label in zip(data, label):
	    psd_temp = BuildPSDPeriod(i_data,sfreq)
	    i_reconstruct_data = psd_temp.get_reconstructed_signal(freq_range=freq_range, para_=False,
	                        method=method, phase_invariance=phase_invariance)
	    if not np.isnan(i_reconstruct_data).any() and not np.isinf(i_reconstruct_data).any():
	        reconstruct_data.append(i_reconstruct_data)
	        new_label.append(i_label)
	reconstruct_data = np.squeeze(np.array(reconstruct_data))
	new_label = np.squeeze(np.array(new_label))
	return reconstruct_data,new_label

class BuildPSDPeriod:
	def __init__(self,data,sfreq,save_path_base=["__","__"]):
		"""
		Initialize the power spectral density (PSD) construction class.

		Args:
			data (numpy.ndarray): Multi-channel time-domain data of shape (n_channel, n_times).
			sfreq (int): Sampling frequency.
			save_path_base (list): Base name for save path.
		"""
		self.n_channel, self.n_times = data.shape
		self.sfreq = sfreq
		self.data = data
		self.save_path_base = save_path_base
	@staticmethod
	def slope_estimate(spectrum, freqs, freq_range=None):
		"""
		Estimate the slope and R² value of a given spectrum.

		Args:
			spectrum (numpy.ndarray): Spectrum data.
			freqs (numpy.ndarray): Corresponding frequency points.
			freq_range (list, optional): Frequency range for estimation.

		Returns:
			tuple: A tuple containing:
				- float: Standard error.
				- float: R² value.
		"""
		if freq_range is None:
			idx_ = np.where(freqs>=0)
		else:
			idx_ = np.where((freq_range[0] <= freqs) & (freqs <= freq_range[1]))
		freqs = np.log10(freqs[idx_])
		spectrum = np.mean(spectrum[:, idx_], axis=0)
		slope, intercept, r_value, p_value, stderr = linregress(freqs, spectrum)
		error = stderr  # 标准误差
		r_qua = r_value ** 2  # 判定系数
		return error, r_qua

	@staticmethod
	def get_periodic_value(gaussian_values,fg,n_channel,freqs,spectrum_frequencies,freq_range=None):
		"""
		Get the values of periodic signals.

		Args:
		    gaussian_values (numpy.ndarray): Empty matrix for storing results, shape (n_channel, n_freqs).
		    fg (FOOOF): FOOOF fitting class.
		    n_channel (int): Number of channels.
		    freqs (numpy.ndarray): Corresponding frequency points, shape (n_freqs).
		    spectrum_frequencies (numpy.ndarray): FFT spectrum, shape (n_channel, n_freqs).
		    freq_range (list, optional): Frequency range for FOOOF fitting.

		Returns:
		    numpy.ndarray: Updated periodic signal values.
		"""
		aps1 = fg.get_params('gaussian_params')
		gaussian_list = aps1[:, 3]
		for i_channel in range(n_channel):
			i_channel_dx = np.where(gaussian_list == i_channel)[0]
			for idx in i_channel_dx:
				gaussian_values[i_channel, :] = aps1[idx, 1] * norm.pdf(freqs, aps1[idx, 0],
				                                                        aps1[idx, 2]) + gaussian_values[i_channel, :]
		if freq_range is not None:
			gaussian_values = np.power(10, gaussian_values)
		else:
			idx_out_range = np.where((freq_range[0] > freqs) | (freqs > freq_range[1]))[0]
			gaussian_values[:,idx_out_range]=spectrum_frequencies[:,idx_out_range]
		return gaussian_values

	@staticmethod
	def remove_aperiodic_value(gaussian_values,fg,n_channel,freqs,spectrum_frequencies,freq_range=None):
		"""
		Get the values after removing aperiodic signals.

		Args:
			gaussian_values (numpy.ndarray): Matrix for storing results, shape (n_channel, n_freqs).
			fg (FOOOF): FOOOF fitting class.
			n_channel (int): Number of channels.
			freqs (numpy.ndarray): Corresponding frequency points, shape (n_freqs).
			spectrum_frequencies (numpy.ndarray): FFT spectrum, shape (n_channel, n_freqs).
			freq_range (list, optional): Frequency range for FOOOF fitting.

		Returns:
			numpy.ndarray: Updated values after removing aperiodic signals.
			float: Standard error.
			float: R² value.
		"""
		offset_ex_list = fg.get_params('aperiodic_params')
		error = fg.group_results[0].error
		r_squared = fg.group_results[0].r_squared
		for i_channel in range(n_channel):
			if freq_range is None:
				for idx in np.where(freqs > 0)[0]:
					aperiodic_value = np.power(10, offset_ex_list[i_channel, 0] -
					                    offset_ex_list[i_channel, 1] * np.log10(freqs[idx]))
					gaussian_values[i_channel, idx] = spectrum_frequencies[i_channel, idx] - aperiodic_value
			else:
				for idx in np.where((freq_range[0] <= freqs) & (freqs <= freq_range[1]))[0]:
					aperiodic_value = np.power(10, offset_ex_list[i_channel, 0] -
					                           offset_ex_list[i_channel, 1] * np.log10(freqs[idx]))
					gaussian_values[i_channel, idx] = spectrum_frequencies[i_channel, idx] - aperiodic_value
		return gaussian_values,error,r_squared

	@staticmethod
	def get_aperiodic_value(gaussian_values,fg,n_channel,freqs,spectrum_frequencies,freq_range=None):
		"""
		Get the values of aperiodic signals.

		Args:
			gaussian_values (numpy.ndarray): Empty matrix for storing results, shape (n_channel, n_freqs).
			fg (FOOOF): FOOOF fitting class.
			n_channel (int): Number of channels.
			freqs (numpy.ndarray): Corresponding frequency points, shape (n_freqs).
			spectrum_frequencies (numpy.ndarray): FFT spectrum, shape (n_channel, n_freqs).
			freq_range (list, optional): Frequency range for FOOOF fitting.

		Returns:
			numpy.ndarray: Updated aperiodic signal values.
		"""
		offset_ex_list = fg.get_params('aperiodic_params')
		gaussian_values = spectrum_frequencies
		for i_channel in range(n_channel):
			if freq_range is None:
				for idx in np.where(freqs > 0)[0]:
					aperiodic_value = np.power(10, offset_ex_list[i_channel, 0] - offset_ex_list[i_channel, 1] * np.log10(
						freqs[idx]))
					gaussian_values[i_channel, idx] = aperiodic_value
			else:
				for idx in np.where((freq_range[0] <= freqs) & (freqs <= freq_range[1]))[0]:
					aperiodic_value = np.power(10, offset_ex_list[i_channel, 0] - offset_ex_list[i_channel, 1] * np.log10(
						freqs[idx]))
					gaussian_values[i_channel, idx] = aperiodic_value
		return gaussian_values


	def get_period_psd(self, spectrum_frequencies, freqs, freq_range=None, method="remove_aperiodic", figure_=False):
		"""
		:param spectrum_frequencies:       narray     Ordinary PSD  shape   (n_channel,n_freqs)
		:param freqs:                      narray     Frequency points corresponding to ordinary PSD   shape   (n_freqs)
		:param freq_range:                 None/list  The default None is determined by foof fitting to the frequency range list, for example [2,50]
		:param method:                     str        "remove_aperiodic"  Remove aperiodic signals
			                                          "get_periodic"      Obtaining periodic signals
			                                          "get_aperiodic"     Obtaining non periodic signals
		:param figure_:                    bool        True: plot fooof fit for psd
		                                               False: don not plot
		:return:
		gaussian_values                   narray       shape   (n_channel,n_freqs) A new PSD matrix corresponding to the method
		"""
		n_channel,_ = spectrum_frequencies.shape
		fg = FOOOFGroup(peak_width_limits=(0.05,12),verbose=False)
		greater_idx = np.where(freqs >= 0)[0]
		greater_fres = freqs[greater_idx]
		greater_spectrum_frequencies = spectrum_frequencies[:, greater_idx]
		fg.fit(greater_fres, greater_spectrum_frequencies, freq_range = freq_range)
		if figure_:
			# current_time = datetime.datetime.now()
			# formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
			# file_name = f"output_{formatted_time}.png"
			# bands = Bands({'a': [0, 50]})
			# afm = average_fg(fg, bands, avg_method='mean')
			# afm.plot(save_fig=True, file_name=os.path.join("save_figure",file_name))
			#plot_spectra(fm.freqs, [np.squeeze(greater_spectrum_frequencies,
			import matplotlib
			matplotlib.use('TkAgg')
			fm = FOOOF(peak_width_limits=(0.05,12),verbose=False)
			fm.fit(greater_fres, np.squeeze(greater_spectrum_frequencies), freq_range = freq_range)
			plot_spectra(fm.freqs, [fm.power_spectrum,fm.get_model('aperiodic') + fm.get_model('peak'),fm.get_model('aperiodic')],
			             linestyle=['-', 'dashed','--'], colors = ['black','red','blue'],log_freqs=True, log_powers = True)
			if not os.path.exists(self.save_path_base[0]):
				os.mkdir(self.save_path_base[0])
			plt.savefig(os.path.join(self.save_path_base[0],self.save_path_base[1]))

		error = 0
		r_squared = 0
		gaussian_values = np.zeros_like(spectrum_frequencies)
		if method == "get_periodic":
			gaussian_values = self.get_periodic_value(gaussian_values,fg,n_channel,freqs,spectrum_frequencies,freq_range)
		if method == "remove_aperiodic":
			gaussian_values,error,r_squared = self.remove_aperiodic_value(gaussian_values,fg,n_channel,freqs,spectrum_frequencies)
		if method == "get_aperiodic":
			gaussian_values = self.get_aperiodic_value(gaussian_values, fg, n_channel, freqs, spectrum_frequencies, freq_range)
		### 将变换后的PSD对应到负的部分
		for idx in np.where(freqs < 0)[0]:
			fre__ = -freqs[idx]
			try:
				gaussian_values[:, idx] = gaussian_values[:, np.where(freqs == fre__)[0][0]]
			except:
				print("used")
		return gaussian_values,error,r_squared

	@staticmethod
	def calculate_fft(data,sfreq):
		"""
		:param data:  narray   shape (n_channel, n_times) Multi-channel time-domain data
		:param sfreq: int      sfreq  sampling frequency
		:return:
		     spectrum_frequencies narray   shape (n_channel，n_freqs)   The amplitude matrix after FFT
             spectrum_phase       narray   shape (n_channel，n_freqs)   The phase matrix after FFT
             freqs                narray   shape (n_freqs)              Corresponding frequency point matrix
		"""
		n_channel, n_times = data.shape
		spectrum_frequencies = np.zeros((n_channel, n_times))
		spectrum_phase = np.zeros((n_channel, n_times))
		freqs = np.fft.fftfreq(n_times, 1/sfreq)
		for i_channel in range(n_channel):
			fft_result = np.fft.fft(data[i_channel, :], n = n_times)
			spectrum_frequencies[i_channel, :] = np.abs(fft_result)
			spectrum_phase[i_channel, :] = np.angle(fft_result)
		return spectrum_frequencies, spectrum_phase, freqs

	def data_to_fft(self, psd_type = "Ordinary", freq_range = None):
		"""
		:param psd_type:   str          Calculate the type of PSD:  "Ordinary"             Original PSD
			                                                        "get_periodic"         periodic signal PSD
			                                                        "remove_aperiodic"     remove aperiod signal PSD
			                                                        "get_aperiodic"        aperiod signal PSD
		:param freq_range: None/list    The default None is determined by foof fitting in the frequency range list, for example [2,50]
		:return:
		         gaussian_values  narray   shape (n_channel,n_fres)
		         freqs            narray   shape (n_fres)
		"""

		self.spectrum_frequencies,_, self.freqs = self.calculate_fft(self.data, self.sfreq)
		if psd_type == "Ordinary":
			return self.spectrum_frequencies**2/(self.sfreq * self.n_times),self.freqs
		else:
			gaussian_values,_,_ = self.get_period_psd(self.spectrum_frequencies**2/(self.sfreq * self.n_times),
			                                      self.freqs, freq_range = freq_range, method = psd_type)
			return gaussian_values, self.freqs

	def get_reconstructed_signal(self,freq_range = None, para_ = False, method = "get_periodic",
	                        phase_invariance = 1):
		"""
		Obtain the periodic components of the signal or remove the aperiodic components of the signal
		:param freq_range:        None/list    The default None is determined by foof fitting in the frequency range list, for example [2,50]
		:param para_:             bool         Discard parameters
		:param method:            str          "get_periodic"         periodic signal PSD
			                                   "remove_aperiodic"     remove aperiod signal PSD
			                                   "get_aperiodic"        aperiod signal PSD
		:return:
		-------
		References
		Donoghue T, Haller M, Peterson E J, et al. Parameterizing neural power spectra into periodic and aperiodic components[J]. Nature neuroscience, 2020, 23(12): 1655-1665.
		"""
		reconstructed_signal = np.zeros_like(self.data)
		spectrum_frequencies, spectrum_phase, freqs = self.calculate_fft(self.data,self.sfreq)
		gaussian_values,_,_ = self.get_period_psd(spectrum_frequencies**2/(self.sfreq * self.n_times),
		                                          freqs, freq_range = freq_range, method = method)
		if np.min(gaussian_values) < 0:
			gaussian_values = gaussian_values + np.abs(np.min(gaussian_values))
		if phase_invariance == 0:
			for i_channel in range(self.n_channel):
				reconstructed_signal[i_channel, :] = np.fft.ifft(np.sqrt(
					gaussian_values[i_channel, :]*(self.sfreq * self.n_times)) * np.exp(1j * spectrum_phase[i_channel, :]))
		# elif phase_invariance == 1:
		# 	for i_channel in range(self.n_channel):
		# 		reconstructed_signal[i_channel, :] = np.fft.ifft(np.sqrt(
		# 			np.abs(gaussian_values[i_channel, :]*(self.sfreq * self.n_times)) * np.exp(1j * spectrum_phase[i_channel, :])))
		elif phase_invariance == 2:
			for i_channel in range(self.n_channel):
				reconstructed_signal[i_channel, :] = np.fft.ifft(np.sqrt(
					gaussian_values[i_channel, :]*(self.sfreq * self.n_times) * np.exp(1j * 0)))
		# if para_:
		# 	peak_para = fg1.get_params('peak_params')
		# 	return reconstructed_signal, peak_para
		# else:
		return reconstructed_signal



