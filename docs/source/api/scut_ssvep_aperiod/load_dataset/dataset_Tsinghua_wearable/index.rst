scut_ssvep_aperiod.load_dataset.dataset_Tsinghua_wearable
=========================================================

.. py:module:: scut_ssvep_aperiod.load_dataset.dataset_Tsinghua_wearable


Attributes
----------

.. autoapisummary::

   scut_ssvep_aperiod.load_dataset.dataset_Tsinghua_wearable.ssvep_data_lee


Classes
-------

.. autoapisummary::

   scut_ssvep_aperiod.load_dataset.dataset_Tsinghua_wearable.LoadDataTHWOne


Module Contents
---------------

.. py:class:: LoadDataTHWOne(data_path)

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

      
      Retrieves information about the dataset, including sample rate and channel names.
















      ..
          !! processed by numpydoc !!


   .. py:method:: _load_data_from_mat(pro_ica=True, filter_para=None, resample=None, reconstruct_=False, picks=['POz', 'PO3', 'PO4', 'PO5', 'PO6', 'Oz', 'O1', 'O2'])

      
      Loads dataset from a .mat file.

      :param pro_ica: Whether to perform ICA in preprocessing.
      :type pro_ica: bool
      :param filter_para: Filter parameters; default is None (no filters).
                          Can be a list [low_freq, high_freq].
      :type filter_para: None or list
      :param resample: Factor of resampling; default is None (no resample).
      :type resample: None or int
      :param reconstruct_: Type of reconstruction; options include:
                           - "remove_aperiodic": reconstruct signals and remove aperiodic component.
                           - "get_periodic": reconstruct signals to get periodic component.
                           - "get_aperiodic": reconstruct signals to get aperiodic component.
      :type reconstruct_: None or str
      :param picks: Channels to select; default is the list of channels specified.
      :type picks: list

      :returns: None















      ..
          !! processed by numpydoc !!


   .. py:method:: _load_data_from_npz(path)

      
      Loads the data from a .npz file after preprocessing.

      :param path: Path to the .npz file.
      :type path: str















      ..
          !! processed by numpydoc !!


   .. py:method:: get_data(pro_ica=True, filter_para=None, resample=None, reconstruct_=False, reconstruct_type=0, freq_range=None, picks=['P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10'])

      
      Retrieves data after preprocessing.

      :param pro_ica: Whether to perform ICA in preprocessing.
      :type pro_ica: bool
      :param filter_para: Filter parameters; default is None (no filters).
                          Can be a list [low_freq, high_freq].
      :type filter_para: None or list
      :param resample: Factor of resampling; default is None (no resample).
      :type resample: None or int
      :param reconstruct_: Type of reconstruction; options include:
                           - "remove_aperiodic": reconstruct signals and remove aperiodic component.
                           - "get_periodic": reconstruct signals to get periodic component.
                           - "get_aperiodic": reconstruct signals to get aperiodic component.
      :type reconstruct_: None or str
      :param reconstruct_type: Phase invariance type for reconstruction.
      :type reconstruct_type: int
      :param freq_range: Frequency range; default is None.
      :type freq_range: None
      :param picks: Channels to select; default is the specified list of channels.
      :type picks: list

      :returns: Processed training and testing data and labels.
      :rtype: tuple















      ..
          !! processed by numpydoc !!


   .. py:attribute:: window_time
      :value: 2



.. py:data:: ssvep_data_lee

