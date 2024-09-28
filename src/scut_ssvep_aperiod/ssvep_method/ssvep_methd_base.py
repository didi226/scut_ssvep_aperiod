import numpy as np
from sklearn.cross_decomposition import CCA
class SSVEPMethodBase():
	"""Base class for SSVEP methods.

	Attributes:
		sfreq (float): Sampling frequency of the data.
		ws (float): Window size in seconds.
		T (int): Number of samples per window.
		fres_list (list): List of frequencies for stimulation.
		n_event (int): Number of events (stimuli).
	"""
	def __init__(self,sfreq,ws,fres_list,):
		"""Initializes the SSVEPMethodBase class.

		Args:
			sfreq (float): Sampling frequency.
			ws (float): Window size in seconds.
			fres_list (list): List of frequencies for stimulation.
		"""
		self.sfreq = sfreq
		self.ws = ws
		self.T = int(self.sfreq * self.ws)
		self.fres_list = fres_list
		self.n_event = len(self.fres_list)


class CCABase(SSVEPMethodBase):
	"""Class for Canonical Correlation Analysis (CCA) methods.

	Inherits from SSVEPMethodBase and adds harmonic analysis capabilities.

	Attributes:
		n_harmonics (int): Number of harmonics to consider for reference signals.
	"""
	def __init__(self, sfreq,ws,fres_list,n_harmonics):
		"""Initializes the CCABase class.

		Args:
			sfreq (float): Sampling frequency.
			ws (float): Window size in seconds.
			fres_list (list): List of frequencies for stimulation.
			n_harmonics (int): Number of harmonics for analysis.
		"""
		super(CCABase, self).__init__(sfreq,ws,fres_list)
		self.n_harmonics = n_harmonics

	def get_reference_signal(self):
		"""Generates reference signals for each frequency and harmonic.

		Returns:
			np.ndarray: An array of reference signals shaped as (n_events, n_harmonics * 2, T).
		"""
		reference_signals = []
		t = np.arange(0, (self.T / self.sfreq), step = 1.0 / self.sfreq)
		for f in self.fres_list:
			reference_f = []
			for h in range(1, self.n_harmonics + 1):
				reference_f.append(np.sin(2 * np.pi * h * f * t)[0:self.T])
				reference_f.append(np.cos(2 * np.pi * h * f * t)[0:self.T])
			reference_signals.append(reference_f)
		reference_signals = np.asarray(reference_signals)
		return reference_signals

	def find_correlation(self, n_components, X, Y):
		"""Finds the maximum correlation between data and reference signals.

		Args:
			n_components (int): Number of components for CCA.
			X (np.ndarray): Data matrix (trials x features).
			Y (np.ndarray): Reference signals (frequencies x time).

		Returns:
			np.ndarray: Maximum correlation values for each frequency.
		"""
		cca = CCA(n_components)
		corr = np.zeros(n_components)
		num_freq = Y.shape[0]
		result = np.zeros(num_freq)
		for freq_idx in range(0, num_freq):
			matched_X = X
			cca.fit(matched_X.T, Y[freq_idx].T)
			x_a, y_b = cca.transform(matched_X.T, Y[freq_idx].T)
			for i in range(n_components):
				corr[i] = np.corrcoef(x_a[:, i], y_b[:, i])[0, 1]
			result[freq_idx] = np.max(corr)
		return result
