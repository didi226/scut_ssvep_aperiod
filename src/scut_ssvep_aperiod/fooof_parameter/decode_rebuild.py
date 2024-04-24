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
def reconstruct_signal(data, label, sfreq, method="remove_aperiodic", phase_invariance=2):
	"""
	:param data:                      numpy array       shape(n_epoch, n_channels, n_times)
	:param label:                     numpy array       shape(n_epoch,)
	:param sfreq:                     float             the sfreq of the signal
	:param method:                    str               method of reconstruction
	                                                    "remove_aperiodic" ---- reconstruct time signals and remove_aperiodic
	                                                    "get_periodic" ---- reconstruct time signals and get_periodic
	                                                    "get_aperiodic" ---- reconstruct time signals and get_aperiodic
	:param phase_invariance:          int                0 ---- with original phase
                                                         2 ---- with 0 phase

	:return:
	reconstruct_data                  numpy array       shape(n_epoch, n_channels, n_times)
	new_label                         numpy array       shape(n_epoch,)
	"""
	reconstruct_data = []
	new_label = []
	for i_data, i_label in zip(data, label):
	    psd_temp = BuildPSDPeriod(i_data,sfreq)
	    i_reconstruct_data = psd_temp.get_reconstructed_signal(freq_range = None, para_ = False,
	                        method = method, phase_invariance = phase_invariance)
	    if not np.isnan(i_reconstruct_data).any() and not np.isinf(i_reconstruct_data).any():
	        reconstruct_data.append(i_reconstruct_data)
	        new_label.append(i_label)
	reconstruct_data = np.squeeze(np.array(reconstruct_data))
	new_label = np.squeeze(np.array(new_label))
	return reconstruct_data,new_label

class BuildPSDPeriod:
	def __init__(self,data,sfreq,save_path_base=["__","__"]):
		"""
		Args:
			data:   narray     shape(n_channel, n_times)
			sfreq:  采样频率
		"""
		self.n_channel, self.n_times = data.shape
		self.sfreq = sfreq
		self.data = data
		self.save_path_base = save_path_base

	@staticmethod
	def get_periodic_value(gaussian_values,fg,n_channel,freqs):
		"""
		Args: 获取周期信号的值
			gaussian_values:  narray          一个空矩阵用来放结果 shape (n_channel,n_freqs)
			fg:               foof拟合类
			n_channel:        int             通道数量
			freqs:            narray          频率点矩阵      shape(n_freqs)
		Returns:              narray          返回周期信号对应的PSD矩阵 shape (n_channel,n_freqs)

		"""
		aps1 = fg.get_params('gaussian_params')
		gaussian_list = aps1[:, 3]
		for i_channel in range(n_channel):
			i_channel_dx = np.where(gaussian_list == i_channel)[0]
			for idx in i_channel_dx:
				gaussian_values[i_channel, :] = aps1[idx, 1] * norm.pdf(freqs, aps1[idx, 0],
				                                                        aps1[idx, 2]) + gaussian_values[i_channel, :]
		gaussian_values = np.power(10, gaussian_values)
		return gaussian_values

	@staticmethod
	def remove_aperiodic_value(gaussian_values,fg,n_channel,freqs,spectrum_frequencies):
		"""
		Args: 获取去除周期信号的值
			gaussian_values:  narray          一个空矩阵用来放结果 shape (n_channel,n_freqs)
			fg:               foof拟合类
			n_channel:        int             通道数量
			freqs:            narray          频率点矩阵      shape(n_freqs)
		Returns:              narray          返回去除周期信号对应的PSD矩阵 shape (n_channel,n_freqs)

		"""
		offset_ex_list = fg.get_params('aperiodic_params')
		error = fg.group_results[0].error
		r_squared = fg.group_results[0].r_squared
		for i_channel in range(n_channel):
			for idx in np.where(freqs > 0)[0]:
				aperiodic_value = np.power(10, offset_ex_list[i_channel, 0] -
				                    offset_ex_list[i_channel, 1] * np.log10(freqs[idx]))
				gaussian_values[i_channel, idx] = spectrum_frequencies[i_channel, idx] - aperiodic_value
		return gaussian_values,error,r_squared

	@staticmethod
	def get_aperiodic_value(gaussian_values,fg,n_channel,freqs):
		"""
		Args: 获取非周期信号的值
			gaussian_values:  narray          一个空矩阵用来放结果 shape (n_channel,n_freqs)
			fg:               foof拟合类
			n_channel:        int             通道数量
			freqs:            narray          频率点矩阵      shape(n_freqs)
		Returns:              narray          返回非周期信号对应的PSD矩阵 shape (n_channel,n_freqs)

		"""
		offset_ex_list = fg.get_params('aperiodic_params')
		for i_channel in range(n_channel):
			for idx in np.where(freqs > 0)[0]:
				aperiodic_value = np.power(10, offset_ex_list[i_channel, 0] - offset_ex_list[i_channel, 1] * np.log10(
					freqs[idx]))
				gaussian_values[i_channel, idx] = aperiodic_value
		return gaussian_values


	def get_period_psd(self, spectrum_frequencies, freqs, freq_range=None, method="remove_aperiodic", figure_=False):
		"""
		Args:
			spectrum_frequencies:    narray     普通的PSD  shape   (n_channel,n_freqs)
			freqs:                   narray     普通的PSD对应的频率点   shape   (n_freqs)
			freq_range:              None/list  默认None由foof拟合决定频率范围 list 例如 [2,50]
			method:                  str        "remove_aperiodic" 去除非周期信号
			                                    "get_periodic"     获取周期信号
			                                    "get_aperiodic"    获取非周期信号

		Returns: gaussian_values narray shape   (n_channel,n_freqs) 与method对应的新的PSD矩阵

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
			gaussian_values = self.get_periodic_value(gaussian_values,fg,n_channel,freqs)
		if method == "remove_aperiodic":
			gaussian_values,error,r_squared = self.remove_aperiodic_value(gaussian_values,fg,n_channel,freqs,spectrum_frequencies)
		if method == "get_aperiodic":
			gaussian_values = self.get_aperiodic_value(gaussian_values,fg,n_channel,freqs)
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
		Args:
			data:   narray   shape (n_channel, n_times) 多通道时域数据
			sfreq:  int      sfreq 采样频率

		Returns:
             spectrum_frequencies narray   shape (n_channel，n_freqs)   fft后的幅值矩阵
             spectrum_phase       narray   shape (n_channel，n_freqs)   相位矩阵
             freqs                narray   shape (n_freqs)              对应的频率点矩阵
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
		Args:
			psd_type:    str          计算PSD的类型  "Ordinary"           原始PSD
			                                       "get_periodic"       周期信号PSD
			                                       "remove_aperiodic"   去除非周期信号PSD
			                                       "get_aperiodic"      获取非周期信号PSD


			freq_range:  None/list  默认None由foof拟合决定频率范围 list 例如 [2,50]

		Returns: gaussian_values  narray   shape (n_channel,n_fres)
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
	                        phase_invariance = True):
		"""
		获取信号的周期成分或者说去掉信号的非周期成分
		Parameters
		----------
		data                      narray      shape（n_channel,n_times）
		sfreq                     int         信号的采样频率 默认250Hz
		Returns
		reconstructed_signal      narray      周期成分信号shape（n_channel,n_times）
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



