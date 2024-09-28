scut_ssvep_aperiod.ssvep_method.psda
====================================

.. py:module:: scut_ssvep_aperiod.ssvep_method.psda


Attributes
----------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_method.psda.data_path


Classes
-------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_method.psda.PSDA
   scut_ssvep_aperiod.ssvep_method.psda.PSDA_SSVEP


Module Contents
---------------

.. py:class:: PSDA(sfreq, ws, fres_list, n_harmonics, psd_type='Ordinary', psd_channel='ave', psda_type='direct_compare', freq_range=None, figure_=False, save_path_base=['__', '__'])

   Bases: :py:obj:`scut_ssvep_aperiod.ssvep_method.ssvep_methd_base.SSVEPMethodBase`


   
   Class for Power Spectral Density Analysis (PSDA) of SSVEP data.

   :param sfreq: Sampling frequency of the data.
   :type sfreq: float
   :param ws: Window size for analysis.
   :type ws: float
   :param fres_list: List of frequencies of interest.
   :type fres_list: list
   :param n_harmonics: Number of harmonics to consider.
   :type n_harmonics: int
   :param psd_type: Type of PSD calculation (default is "Ordinary").
   :type psd_type: str
   :param psd_channel: Channel type for PSD calculation (default is "ave").
   :type psd_channel: str
   :param psda_type: Type of PSDA method to use (default is "direct_compare").
   :type psda_type: str
   :param freq_range: Frequency range for analysis.
   :type freq_range: tuple, optional
   :param figure_: Whether to generate figures (default is False).
   :type figure_: bool
   :param save_path_base: Base path for saving figures (default is ["__", "__"]).
   :type save_path_base: list















   ..
       !! processed by numpydoc !!

   .. py:method:: calculate_snr(data)

      
           Calculates the signal-to-noise ratio (SNR) for each trial.

      :param data: Input data for SNR calculation.
      :type data: numpy.ndarray

      :returns: SNR values for each frequency for all trials.
      :rtype: numpy.ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: classify(data)

      
      Classifies the input data using PSDA.

      :param data: Input data for classification.
      :type data: numpy.ndarray

      :returns: Predicted labels, errors, and R-squared values for each trial.
      :rtype: tuple















      ..
          !! processed by numpydoc !!


   .. py:method:: slope_estimation(data)

      
      Estimates the slope of the PSD for each trial.

      :param data: Input data for slope estimation.
      :type data: numpy.ndarray

      :returns: Errors and R-squared values for each trial.
      :rtype: tuple















      ..
          !! processed by numpydoc !!


   .. py:attribute:: deltaf


   .. py:attribute:: figure_


   .. py:attribute:: freq_range


   .. py:attribute:: n_harmonics


   .. py:attribute:: psd_channel


   .. py:attribute:: psd_type


   .. py:attribute:: psda_type


   .. py:attribute:: save_path_base


.. py:class:: PSDA_SSVEP(data_psd, frequence, fre_doi, psd_channel='ave', harmonic=4, sfreq=250, n_times=1000, deltaf=0.25, freq_range=None, figure_=False, save_path_base=['__', '__'])

   
   Class for performing SSVEP-based PSD analysis.

   :param data_psd: Input PSD data.
   :type data_psd: numpy.ndarray
   :param frequence: Frequency array.
   :type frequence: numpy.ndarray
   :param fre_doi: Frequencies of interest for analysis.
   :type fre_doi: list
   :param psd_channel: Channel type for PSD calculation (default is "ave").
   :type psd_channel: str
   :param harmonic: Number of harmonics to consider (default is 4).
   :type harmonic: int
   :param sfreq: Sampling frequency (default is 250).
   :type sfreq: float
   :param n_times: Number of time points (default is 1000).
   :type n_times: int
   :param deltaf: Frequency resolution (default is 0.25).
   :type deltaf: float
   :param freq_range: Frequency range for analysis.
   :type freq_range: tuple, optional
   :param figure_: Whether to generate figures (default is False).
   :type figure_: bool
   :param save_path_base: Base path for saving figures (default is ["__", "__"]).
   :type save_path_base: list















   ..
       !! processed by numpydoc !!

   .. py:method:: calculate_snr(data_psd_channel, frequence, i_fre, deltaf)

      
      Calculates the signal-to-noise ratio (SNR) for a specific frequency.

      :param data_psd_channel: PSD values for a specific channel.
      :type data_psd_channel: numpy.ndarray
      :param frequence: Frequency array.
      :type frequence: numpy.ndarray
      :param i_fre: Frequency at which to calculate SNR.
      :type i_fre: float
      :param deltaf: Frequency resolution.
      :type deltaf: float

      :returns: Calculated SNR value.
      :rtype: float















      ..
          !! processed by numpydoc !!


   .. py:method:: calculate_snr_hqy(data_psd_channel, frequence, i_fre, deltaf)

      
      Calculates the Signal-to-Noise Ratio (SNR) for a specific frequency.

      This method computes the SNR for a given frequency `i_fre` by finding the
      nearest frequency in the data and using neighboring frequencies as a noise
      baseline. If the power spectral density (PSD) has negative values, they are
      adjusted to avoid computation errors.

      :param data_psd_channel: Power spectral density values for a given channel.
      :type data_psd_channel: np.ndarray
      :param frequence: Array of frequency values corresponding to `data_psd_channel`.
      :type frequence: np.ndarray
      :param i_fre: The frequency of interest for which SNR is calculated.
      :type i_fre: float
      :param deltaf: Frequency resolution or spacing used to estimate noise baseline.
      :type deltaf: float

      :returns: The calculated SNR in decibels (dB).
      :rtype: float

      .. rubric:: Notes

      - The method finds the frequency closest to `i_fre` and uses neighboring
        frequencies (± deltaf) to estimate noise.
      - The SNR is computed in decibels using the formula:
              SNR = 20 * log10(8 * y / (sum(noise) - y))
        where `y` is the PSD value at `i_fre`, and `noise` is the sum of PSD
        values at neighboring frequencies.















      ..
          !! processed by numpydoc !!


   .. py:method:: estimate_psd_value(data_psd_i_channel, frequence, i_fre)
      :staticmethod:


      
      Estimates the PSD value for a specific frequency.

      :param data_psd_i_channel: PSD values for a single channel.
      :type data_psd_i_channel: numpy.ndarray
      :param frequence: Frequency array.
      :type frequence: numpy.ndarray
      :param i_fre: Frequency at which to estimate the PSD value.
      :type i_fre: float

      :returns: Estimated PSD value.
      :rtype: float















      ..
          !! processed by numpydoc !!


   .. py:method:: psd_original()

      
      Calculates the Power Spectral Density (PSD) values for each frequency of interest.

      If the psd_channel is not "ave", computes PSD for each channel and then averages. Otherwise, it averages across channels first.

      :returns: Index of the frequency with the highest PSD value.
      :rtype: label (int)















      ..
          !! processed by numpydoc !!


   .. py:method:: psd_snr()

      
      Calculates the Signal-to-Noise Ratio (SNR) of the PSD for each frequency of interest.

      :returns: SNR values across frequencies for each channel.
      :rtype: indicators_values (ndarray)















      ..
          !! processed by numpydoc !!


   .. py:method:: psd_snr_hqy()

      
      Calculates the SNR of the PSD using a harmonic approach for each frequency of interest.

      :returns: Harmonic SNR values across frequencies for each channel.
      :rtype: indicators_values (ndarray)















      ..
          !! processed by numpydoc !!


   .. py:method:: psd_snr_hqy_ave_re()

      
           Calculates the harmonic SNR using the averaged PSD after removing the aperiodic component.

      :returns: Harmonic SNR values across frequencies.
                error (float): Error value from PSD analysis.
                r_squa (float): R-squared value from PSD analysis.
      :rtype: indicators_values (ndarray)















      ..
          !! processed by numpydoc !!


   .. py:method:: psda_classify(psda_type='direct_compare')

      
      Classifies based on the PSD analysis result.

      :param psda_type: Type of PSD analysis to perform. Defaults to "direct_compare".
      :type psda_type: str, optional

      :returns: Index of the maximum PSD value indicating the classification label.
                error (float): Error value from PSD analysis.
                r_squa (float): R-squared value from PSD analysis.
      :rtype: label (int)















      ..
          !! processed by numpydoc !!


   .. py:method:: psda_ex(psda_type='direct_compare')

      
      Executes the PSDA analysis based on the specified method type.

      :param psda_type: The type of PSDA method to use. Options include:
                        - "direct_compare": Direct comparison of PSD values.
                        - "snr": Signal-to-noise ratio analysis.
                        - "snr_hqy": SNR with high-quality estimates.
                        - "snr_hqy_ave_re": SNR with high-quality averaging, returning error and R-squared.
                        - "snr_hqy_ave_get": SNR high-quality averaging with different retrieval methods.
      :type psda_type: str

      :returns: Computed PSD values.
                float: Error metric (0 if not applicable).
                float: R-squared value (0 if not applicable).
      :rtype: numpy.ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: snr_hqy_ave_get()

      
      Calculates the harmonic SNR using the averaged PSD with the aperiodic component.

      :returns: Harmonic SNR values across frequencies.
      :rtype: indicators_values (ndarray)















      ..
          !! processed by numpydoc !!


   .. py:attribute:: data_psd


   .. py:attribute:: deltaf


   .. py:attribute:: figure_


   .. py:attribute:: fre_doi


   .. py:attribute:: freq_range


   .. py:attribute:: frequence


   .. py:attribute:: harmonic


   .. py:attribute:: n_fre


   .. py:attribute:: n_times


   .. py:attribute:: psd_channel


   .. py:attribute:: save_path_base


   .. py:attribute:: sfreq


.. py:data:: data_path
   :value: 'D:\\data\\ssvep_dataset\\MNE-lee2019-ssvep-data\\session1\\s1\\sess01_subj01_EEG_SSVEP.mat'


