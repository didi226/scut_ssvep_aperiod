import numpy as np
from sklearn.cross_decomposition import CCA
class SSVEPMethodBase():
	def __init__(self,sfreq,ws,fres_list,):
		self.sfreq = sfreq
		self.ws = ws
		self.T = int(self.sfreq * self.ws)
		self.fres_list = fres_list
		self.n_event = len(self.fres_list)


class CCABase(SSVEPMethodBase):
	def __init__(self, sfreq,ws,fres_list,n_harmonics):
		super(CCABase, self).__init__(sfreq,ws,fres_list)
		self.n_harmonics = n_harmonics

	def get_reference_signal(self):
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
