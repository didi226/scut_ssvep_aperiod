scut_ssvep_aperiod.fooof_parameter.decode_rebuild
=================================================

.. py:module:: scut_ssvep_aperiod.fooof_parameter.decode_rebuild


Classes
-------

.. autoapisummary::

   scut_ssvep_aperiod.fooof_parameter.decode_rebuild.BuildPSDPeriod


Functions
---------

.. autoapisummary::

   scut_ssvep_aperiod.fooof_parameter.decode_rebuild.reconstruct_signal


Module Contents
---------------

.. py:class:: BuildPSDPeriod(data, sfreq, save_path_base=['__', '__'])

   .. py:method:: calculate_fft(data, sfreq)
      :staticmethod:


      
         :param data:  narray   shape (n_channel, n_times) Multi-channel time-domain data
         :param sfreq: int      sfreq  sampling frequency
         :return:
              spectrum_frequencies narray   shape (n_channel，n_freqs)   The amplitude matrix after FFT
      spectrum_phase       narray   shape (n_channel，n_freqs)   The phase matrix after FFT
      freqs                narray   shape (n_freqs)              Corresponding frequency point matrix
















      ..
          !! processed by numpydoc !!


   .. py:method:: data_to_fft(psd_type='Ordinary', freq_range=None)

      
      :param psd_type:   str          Calculate the type of PSD:  "Ordinary"             Original PSD
                                                                      "get_periodic"         periodic signal PSD
                                                                      "remove_aperiodic"     remove aperiod signal PSD
                                                                      "get_aperiodic"        aperiod signal PSD
      :param freq_range: None/list    The default None is determined by foof fitting in the frequency range list, for example [2,50]
      :return:
               gaussian_values  narray   shape (n_channel,n_fres)
               freqs            narray   shape (n_fres)
















      ..
          !! processed by numpydoc !!


   .. py:method:: get_aperiodic_value(gaussian_values, fg, n_channel, freqs, spectrum_frequencies, freq_range=None)
      :staticmethod:


      
      Get the values of aperiodic signals.

      :param gaussian_values: Empty matrix for storing results, shape (n_channel, n_freqs).
      :type gaussian_values: numpy.ndarray
      :param fg: FOOOF fitting class.
      :type fg: FOOOF
      :param n_channel: Number of channels.
      :type n_channel: int
      :param freqs: Corresponding frequency points, shape (n_freqs).
      :type freqs: numpy.ndarray
      :param spectrum_frequencies: FFT spectrum, shape (n_channel, n_freqs).
      :type spectrum_frequencies: numpy.ndarray
      :param freq_range: Frequency range for FOOOF fitting.
      :type freq_range: list, optional

      :returns: Updated aperiodic signal values.
      :rtype: numpy.ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: get_period_psd(spectrum_frequencies, freqs, freq_range=None, method='remove_aperiodic', figure_=False)

      
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
















      ..
          !! processed by numpydoc !!


   .. py:method:: get_periodic_value(gaussian_values, fg, n_channel, freqs, spectrum_frequencies, freq_range=None)
      :staticmethod:


      
      Get the values of periodic signals.

      :param gaussian_values: Empty matrix for storing results, shape (n_channel, n_freqs).
      :type gaussian_values: numpy.ndarray
      :param fg: FOOOF fitting class.
      :type fg: FOOOF
      :param n_channel: Number of channels.
      :type n_channel: int
      :param freqs: Corresponding frequency points, shape (n_freqs).
      :type freqs: numpy.ndarray
      :param spectrum_frequencies: FFT spectrum, shape (n_channel, n_freqs).
      :type spectrum_frequencies: numpy.ndarray
      :param freq_range: Frequency range for FOOOF fitting.
      :type freq_range: list, optional

      :returns: Updated periodic signal values.
      :rtype: numpy.ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: get_reconstructed_signal(freq_range=None, para_=False, method='get_periodic', phase_invariance=1)

      
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
















      ..
          !! processed by numpydoc !!


   .. py:method:: remove_aperiodic_value(gaussian_values, fg, n_channel, freqs, spectrum_frequencies, freq_range=None)
      :staticmethod:


      
      Get the values after removing aperiodic signals.

      :param gaussian_values: Matrix for storing results, shape (n_channel, n_freqs).
      :type gaussian_values: numpy.ndarray
      :param fg: FOOOF fitting class.
      :type fg: FOOOF
      :param n_channel: Number of channels.
      :type n_channel: int
      :param freqs: Corresponding frequency points, shape (n_freqs).
      :type freqs: numpy.ndarray
      :param spectrum_frequencies: FFT spectrum, shape (n_channel, n_freqs).
      :type spectrum_frequencies: numpy.ndarray
      :param freq_range: Frequency range for FOOOF fitting.
      :type freq_range: list, optional

      :returns: Updated values after removing aperiodic signals.
                float: Standard error.
                float: R² value.
      :rtype: numpy.ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: slope_estimate(spectrum, freqs, freq_range=None)
      :staticmethod:


      
      Estimate the slope and R² value of a given spectrum.

      :param spectrum: Spectrum data.
      :type spectrum: numpy.ndarray
      :param freqs: Corresponding frequency points.
      :type freqs: numpy.ndarray
      :param freq_range: Frequency range for estimation.
      :type freq_range: list, optional

      :returns:

                A tuple containing:
                        - float: Standard error.
                        - float: R² value.
      :rtype: tuple















      ..
          !! processed by numpydoc !!


   .. py:attribute:: data


   .. py:attribute:: save_path_base


   .. py:attribute:: sfreq


.. py:function:: reconstruct_signal(data, label, sfreq, method='remove_aperiodic', phase_invariance=2, freq_range=None)

   
   Reconstruct signals by extracting periodic and aperiodic components from time series data.

   :param data: Time series data of shape (n_epoch, n_channels, n_times).
   :type data: numpy.ndarray
   :param label: Labels of shape (n_epoch,).
   :type label: numpy.ndarray
   :param sfreq: Sampling frequency of the signal.
   :type sfreq: float
   :param method: Reconstruction method. Options:
                  "remove_aperiodic": Reconstruct time signal and remove aperiodic components.
                  "get_periodic": Reconstruct time signal and extract periodic components.
                  "get_aperiodic": Reconstruct time signal and extract aperiodic components.
   :type method: str
   :param phase_invariance: Phase invariance option:
                            0: Use original phase.
                            2: Use zero phase.
   :type phase_invariance: int
   :param freq_range: Frequency range for reconstruction.
   :type freq_range: list, optional

   :returns:

             A tuple containing:
                     - numpy.ndarray: Reconstructed data of shape (n_epoch, n_channels, n_times).
                     - numpy.ndarray: New labels of shape (n_epoch,).
   :rtype: tuple















   ..
       !! processed by numpydoc !!

