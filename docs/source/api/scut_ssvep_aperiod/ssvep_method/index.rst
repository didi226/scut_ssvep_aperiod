scut_ssvep_aperiod.ssvep_method
===============================

.. py:module:: scut_ssvep_aperiod.ssvep_method


Submodules
----------

.. toctree::
   :maxdepth: 1

   /api/scut_ssvep_aperiod/ssvep_method/cca/index
   /api/scut_ssvep_aperiod/ssvep_method/fbcca/index
   /api/scut_ssvep_aperiod/ssvep_method/psda/index
   /api/scut_ssvep_aperiod/ssvep_method/ssvep_methd_base/index
   /api/scut_ssvep_aperiod/ssvep_method/tdca/index
   /api/scut_ssvep_aperiod/ssvep_method/trca/index


Classes
-------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_method.CCABase
   scut_ssvep_aperiod.ssvep_method.CCACommon
   scut_ssvep_aperiod.ssvep_method.FBCCA
   scut_ssvep_aperiod.ssvep_method.PSDA
   scut_ssvep_aperiod.ssvep_method.TDCA
   scut_ssvep_aperiod.ssvep_method.TRCA


Package Contents
----------------

.. py:class:: CCABase(sfreq, ws, fres_list, n_harmonics)

   Bases: :py:obj:`SSVEPMethodBase`


   
   Class for Canonical Correlation Analysis (CCA) methods.

   Inherits from SSVEPMethodBase and adds harmonic analysis capabilities.

   .. attribute:: n_harmonics

      Number of harmonics to consider for reference signals.

      :type: int















   ..
       !! processed by numpydoc !!

   .. py:method:: find_correlation(n_components, X, Y)

      
      Finds the maximum correlation between data and reference signals.

      :param n_components: Number of components for CCA.
      :type n_components: int
      :param X: Data matrix (trials x features).
      :type X: np.ndarray
      :param Y: Reference signals (frequencies x time).
      :type Y: np.ndarray

      :returns: Maximum correlation values for each frequency.
      :rtype: np.ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: get_reference_signal()

      
      Generates reference signals for each frequency and harmonic.

      :returns: An array of reference signals shaped as (n_events, n_harmonics * 2, T).
      :rtype: np.ndarray















      ..
          !! processed by numpydoc !!


   .. py:attribute:: n_harmonics


.. py:class:: CCACommon(sfreq, ws, fres_list, n_harmonics)

   Bases: :py:obj:`scut_ssvep_aperiod.ssvep_method.ssvep_methd_base.CCABase`


   
   Class for Canonical Correlation Analysis (CCA) methods.

   Inherits from SSVEPMethodBase and adds harmonic analysis capabilities.

   .. attribute:: n_harmonics

      Number of harmonics to consider for reference signals.

      :type: int















   ..
       !! processed by numpydoc !!

   .. py:method:: _cca_classify(test_data, ica_=False)

      
      Classifies the test data using CCA.

      :param test_data: shape(n_channels,n_times)
      :type test_data: ndarray
      :param ica_: Whether to apply ICA.
      :type ica_: bool

      :returns: The index of the class with the highest correlation.
      :rtype: int















      ..
          !! processed by numpydoc !!


   .. py:method:: _cca_ex(test_data, ica_=False)

      
      Performs Canonical Correlation Analysis (CCA) on the provided test data.

      :param test_data: Input data with shape (n_channels, n_times).
      :type test_data: ndarray
      :param ica_: Flag indicating whether to apply Independent Component Analysis (ICA).
      :type ica_: bool

      :returns: The correlation results obtained from the CCA.
      :rtype: ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: calculate_ex(test_data, ica_=False)

      
      Calculates the CCA results for each sample in the test data.

      :param test_data: shape(n_epochs,n_channels,n_times)
      :type test_data: ndarray
      :param ica_: Whether to apply ICA.
      :type ica_: bool

      :returns: An array of CCA results for each sample.
      :rtype: ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: classify(test_data, ica_=False)

      
      Classifies the provided test data using Canonical Correlation Analysis (CCA).

      :param test_data: Input data with shape (n_channels, n_times).
      :type test_data: ndarray
      :param ica_: Flag indicating whether to apply ICA.
      :type ica_: bool

      :returns: The index of the class with the highest correlation result.
      :rtype: int















      ..
          !! processed by numpydoc !!


.. py:class:: FBCCA(sfreq, ws, fres_list, n_harmonics, Nc=9, Nm=5, passband=[6, 14, 22, 30, 38], stopband=[4, 10, 16, 24, 32], high_cut_pass=40, high_cut_stop=50)

   Bases: :py:obj:`scut_ssvep_aperiod.ssvep_method.ssvep_methd_base.CCABase`


   
   Class for Canonical Correlation Analysis (CCA) methods.

   Inherits from SSVEPMethodBase and adds harmonic analysis capabilities.

   .. attribute:: n_harmonics

      Number of harmonics to consider for reference signals.

      :type: int















   ..
       !! processed by numpydoc !!

   .. py:method:: calculate_ex()

      
      Returns the results of the classification experiments.

      :returns: The results of the classification experiments.
      :rtype: ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: classify(test_data)

      
      Classifies the test data using FBCCA.

      :param test_data: Input test data with shape (n_epochs, n_channels, n_times).
      :type test_data: ndarray

      :returns: An array of predicted class labels for each segment.
      :rtype: ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: filter_bank(eeg)

      
      Applies a filter bank to the EEG data.

      :param eeg: Input EEG data with shape (n_epoch, n_channels, n_times).
      :type eeg: ndarray

      :returns: Filtered data with shape (n_epoch, Nm, n_channels, n_times).
      :rtype: ndarray















      ..
          !! processed by numpydoc !!


   .. py:attribute:: Nc


   .. py:attribute:: Nf


   .. py:attribute:: Nm


   .. py:attribute:: high_cut_pass


   .. py:attribute:: high_cut_stop


   .. py:attribute:: pass_band


   .. py:attribute:: stop_band


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


.. py:class:: TDCA(sfreq, ws, fres_list, n_harmonics, Nc=10, Nm=1, passband=[6, 14, 22, 30, 38], stopband=[4, 10, 16, 24, 32], highcut_pass=40, highcut_stop=50, lagging_len=0)

   Bases: :py:obj:`scut_ssvep_aperiod.ssvep_method.ssvep_methd_base.CCABase`


   
   Class for TDCA (Temporal Discriminative Component Analysis).

   .. attribute:: sfreq

      Sampling frequency.

      :type: float

   .. attribute:: ws

      Window size.

      :type: int

   .. attribute:: fres_list

      Frequency list.

      :type: list

   .. attribute:: n_harmonics

      Number of harmonics.

      :type: int

   .. attribute:: Nm

      Number of channels.

      :type: int

   .. attribute:: Nc

      Number of components.

      :type: int

   .. attribute:: lagging_len

      Lagging length.

      :type: int

   .. attribute:: passband

      Passband frequencies.

      :type: list

   .. attribute:: stopband

      Stopband frequencies.

      :type: list

   .. attribute:: highcut_pass

      Highcut pass frequency.

      :type: float

   .. attribute:: highcut_stop

      Highcut stop frequency.

      :type: float















   ..
       !! processed by numpydoc !!

   .. py:method:: calculate_ex()

      
      Calculate features from the last transformation.

      :returns: Extracted features.
      :rtype: ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: classifier(X)

      
      Classify input EEG signals.

      :param X: Input EEG signals (n_trials, n_channels, n_points).
      :type X: ndarray

      :returns: Predicted labels (n_trials,).
      :rtype: ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: filter_bank(X)

      
      Apply filter bank to EEG signals.

      :param X: Input EEG signals (n_trials, n_channels, n_points).
      :type X: ndarray

      :returns: Output EEG signals of filter banks (n_fb, n_trials, n_channels, n_points).
      :rtype: ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: train(X, y)

      
      Train the TDCA model on input EEG signals and labels.

      :param X: Input EEG signals (n_trials, n_channels, n_points).
      :type X: ndarray
      :param y: Input labels (n_trials,).
      :type y: ndarray

      :returns: TDCA object.
      :rtype: self















      ..
          !! processed by numpydoc !!


   .. py:method:: transform(X, fb_i)

      
      Transform input EEG signals into features.

      :param X: Input EEG signals (n_trials, n_channels, n_points).
      :type X: ndarray
      :param fb_i: Filter bank index.
      :type fb_i: int

      :returns: Feature vectors (n_trials, n_freq).
      :rtype: ndarray















      ..
          !! processed by numpydoc !!


   .. py:attribute:: Nc


   .. py:attribute:: Nf


   .. py:attribute:: Nm


   .. py:attribute:: highcut_pass


   .. py:attribute:: highcut_stop


   .. py:attribute:: lagging_len


   .. py:attribute:: n_components
      :value: 3



   .. py:attribute:: passband


   .. py:attribute:: stopband


.. py:class:: TRCA(sfreq, ws, fres_list, n_harmonics, filter_=None)

   Bases: :py:obj:`scut_ssvep_aperiod.ssvep_method.ssvep_methd_base.CCABase`


   
   Class for Canonical Correlation Analysis (CCA) methods.

   Inherits from SSVEPMethodBase and adds harmonic analysis capabilities.

   .. attribute:: n_harmonics

      Number of harmonics to consider for reference signals.

      :type: int















   ..
       !! processed by numpydoc !!

   .. py:method:: classifier(test_data)

      
      Classifies test data using the trained TRCA model.

      :param test_data: Test data of shape (n_trials, n_channels, n_times).
      :type test_data: numpy.ndarray

      :returns: Predicted labels for test data.
      :rtype: numpy.ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: filter_bank(X)

      
      Applies a filter bank to the input EEG signals.

      :param X: Input EEG signals of shape (n_trials, n_channels, n_points).
      :type X: numpy.ndarray

      :returns: Filtered EEG signals of shape (n_fb, n_trials, n_channels, n_points).
      :rtype: numpy.ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: get_w(train_data, train_label)

      
      Computes the weight matrix for the TRCA method.

      :param train_data: Training data of shape (n_trials, n_channels, n_times).
      :type train_data: numpy.ndarray
      :param train_label: Labels for training data of shape (n_trials,).
      :type train_label: numpy.ndarray

      :returns: Weight matrix W of shape (n_events, n_channels).
                numpy.ndarray: Temporary matrix temp_X of shape (n_events, n_channels).
      :rtype: numpy.ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: train(train_data, train_label)

      
      Trains the TRCA model using the provided training data and labels.

      :param train_data: Training data of shape (n_trials, n_channels, n_times).
      :type train_data: numpy.ndarray
      :param train_label: Labels for training data of shape (n_trials,).
      :type train_label: numpy.ndarray

      :returns: Weight matrix w_all of shape (n_filters, n_channels).
                numpy.ndarray: Temporary matrix temp_x_all of shape (n_filters, n_trials).
      :rtype: numpy.ndarray















      ..
          !! processed by numpydoc !!


   .. py:attribute:: filter_


