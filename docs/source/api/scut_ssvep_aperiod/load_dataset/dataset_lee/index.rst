scut_ssvep_aperiod.load_dataset.dataset_lee
===========================================

.. py:module:: scut_ssvep_aperiod.load_dataset.dataset_lee


Attributes
----------

.. autoapisummary::

   scut_ssvep_aperiod.load_dataset.dataset_lee.ssvep_data_lee


Classes
-------

.. autoapisummary::

   scut_ssvep_aperiod.load_dataset.dataset_lee.LoadDataLeeOne


Module Contents
---------------

.. py:class:: LoadDataLeeOne(data_path, info_path='D:\\data\\ssvep_dataset\\MNE-lee2019-ssvep-data\\info_ssvep_lee_dataset.mat')

   Bases: :py:obj:`scut_ssvep_aperiod.load_dataset.dataset_base.LoadDataBase`


   
   Base class for loading and preprocessing SSVEP data.

   :param data_path: Path to the dataset file.
   :type data_path: str

   .. attribute:: data_path

      Path to the dataset file.

      :type: str

   .. attribute:: window_time

      The time window for data processing, default is 4 - 0.14 seconds.

      :type: float















   ..
       !! processed by numpydoc !!

   .. py:method:: _get_info()

      
      Gets the info from the info file.
















      ..
          !! processed by numpydoc !!


   .. py:method:: _load_data_from_mat(pro_ica=True, filter_para=None, resample=None, picks=['P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10'])

      
      Loads dataset from .mat file.

      :param pro_ica: Whether to perform ICA in preprocessing.
      :type pro_ica: bool
      :param filter_para: Filter parameters, default is None (no filters).
                          [low_freq, high_freq].
      :type filter_para: None or list
      :param resample: Factor for resampling, default is None (no resample).
      :type resample: None or int
      :param picks: Channels to select, default is ['P7','P3','Pz','P4','P8','PO9','O1','Oz','O2','PO10'].
      :type picks: list

      :returns: Loads data into instance variables.
      :rtype: None















      ..
          !! processed by numpydoc !!


   .. py:method:: _load_data_from_npz(path)

      
      Loads the data from a npz file (preprocess).

      :param path: Path to the npz file.
      :type path: str

      .. attribute:: data_test

         Test data.

         :type: numpy.ndarray

      .. attribute:: label_test

         Test labels.

         :type: numpy.ndarray

      .. attribute:: n_epoch_test

         Number of test epochs.

         :type: int

      .. attribute:: n_channel_test

         Number of test channels.

         :type: int

      .. attribute:: sample_rate_test

         Sample rate for test data.

         :type: int

      .. attribute:: data_train

         Training data.

         :type: numpy.ndarray

      .. attribute:: label_train

         Training labels.

         :type: numpy.ndarray

      .. attribute:: n_epoch_train

         Number of training epochs.

         :type: int

      .. attribute:: n_channel_train

         Number of training channels.

         :type: int

      .. attribute:: sample_rate_train

         Sample rate for training data.

         :type: int















      ..
          !! processed by numpydoc !!


   .. py:method:: _load_data_from_structure(file_data, pro_ica=True, filter_para=None, resample=None, picks=['P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10'])

      
      Reads data from the structure in .mat file.

      :param file_data: Data loaded from .mat file.
      :type file_data: dict
      :param pro_ica: Whether to perform ICA in preprocessing.
      :type pro_ica: bool
      :param filter_para: Filter parameters, default is None (no filters).
                          [low_freq, high_freq].
      :type filter_para: None or list
      :param resample: Factor for resampling, default is None (no resample).
      :type resample: None or int
      :param picks: Channels to select, default is ['P7','P3','Pz','P4','P8','PO9','O1','Oz','O2','PO10'].
      :type picks: list

      :returns: Data split into shape (n_epochs, n_channels, n_samples).
                label (numpy.ndarray): Labels of the data.
                n_epoch (int): Number of epochs.
                n_channel (int): Number of channels.
                sample_rate (float): Sampling rate after resampling.
      :rtype: split_data (numpy.ndarray)















      ..
          !! processed by numpydoc !!


   .. py:method:: _load_resting_state_data_from_mat(pro_ica=True, filter_para=None, resample=None, picks=None)

      
      Load resting state dataset from a MAT file.

      :param pro_ica: If True, performs Independent Component Analysis (ICA) during preprocessing.
      :type pro_ica: bool
      :param filter_para: Frequency filter parameters, specified as [low_freq, high_freq].
                          Default is None (no filters).
      :type filter_para: list or None
      :param resample: Resampling factor. If None, no resampling is performed.
      :type resample: int or None
      :param picks: Channels to select. Default is
                    ['P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10'].
      :type picks: list

      :returns: Preprocessed training and testing data for the resting state.
      :rtype: tuple















      ..
          !! processed by numpydoc !!


   .. py:method:: _load_resting_state_data_from_structure(file_data, pro_ica=True, filter_para=None, resample=None, picks=None)

      
      Reads resting state data from the structure in .mat file.

      :param file_data: Data loaded from .mat file.
      :type file_data: dict
      :param pro_ica: Whether to perform ICA in preprocessing.
      :type pro_ica: bool
      :param filter_para: Filter parameters, default is None (no filters).
                          [low_freq, high_freq].
      :type filter_para: None or list
      :param resample: Factor for resampling, default is None (no resample).
      :type resample: None or int
      :param picks: Channels to select, default is ['P7','P3','Pz','P4','P8','PO9','O1','Oz','O2','PO10'].
      :type picks: list

      :returns: Pre-resting state data.
                post_rest_data (numpy.ndarray): Post-resting state data.
      :rtype: pre_rest_data (numpy.ndarray)















      ..
          !! processed by numpydoc !!


   .. py:method:: get_data(pro_ica=True, filter_para=None, resample=None, reconstruct_=False, reconstruct_type=0, freq_range=None, picks=['P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10'])

      
      Retrieve and preprocess EEG data.

      :param pro_ica: If True, performs Independent Component Analysis (ICA) during preprocessing.
      :type pro_ica: bool
      :param filter_para: Frequency filter parameters, specified as [low_freq, high_freq].
                          Default is None (no filters).
      :type filter_para: list or None
      :param resample: Resampling factor. If None, no resampling is performed.
      :type resample: int or None
      :param reconstruct_: Reconstruction method. Options include:
                           "remove_aperiodic", "get_periodic", "get_aperiodic".
                           Default is None (no reconstruction).
      :type reconstruct_: str or None
      :param reconstruct_type: Type of reconstruction phase invariance. Default is 0.
      :type reconstruct_type: int
      :param freq_range: Frequency range for filtering. Default is None (no filtering).
      :type freq_range: None or list
      :param picks: Channels to select. Default is
                    ['P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10'].
      :type picks: list

      :returns: Preprocessed training and testing data along with their labels.
      :rtype: tuple















      ..
          !! processed by numpydoc !!


   .. py:method:: get_data_resting_state(pro_ica=True, filter_para=None, resample=None, picks=None)

      
      Get resting state data after preprocessing.

      :param pro_ica: If True, performs Independent Component Analysis (ICA) during preprocessing.
      :type pro_ica: bool
      :param filter_para: Frequency filter parameters, specified as [low_freq, high_freq].
                          Default is None (no filters).
      :type filter_para: list or None
      :param resample: Resampling factor. If None, no resampling is performed.
      :type resample: int or None
      :param picks: Channels to select. Default is
                    ['P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10'].
      :type picks: list

      :returns: Preprocessed training and testing data for the resting state.
      :rtype: tuple















      ..
          !! processed by numpydoc !!


   .. py:attribute:: info_path


   .. py:attribute:: window_time


.. py:data:: ssvep_data_lee

