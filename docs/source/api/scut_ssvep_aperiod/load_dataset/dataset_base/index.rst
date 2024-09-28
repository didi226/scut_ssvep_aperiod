scut_ssvep_aperiod.load_dataset.dataset_base
============================================

.. py:module:: scut_ssvep_aperiod.load_dataset.dataset_base


Classes
-------

.. autoapisummary::

   scut_ssvep_aperiod.load_dataset.dataset_base.LoadDataBase


Module Contents
---------------

.. py:class:: LoadDataBase(data_path)

   
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

   .. py:method:: get_data(ica_=True, filter_para=None)

      
      Abstract method for loading and retrieving data.

      :param ica_: Whether to apply ICA in data preprocessing. Defaults to True.
      :type ica_: bool, optional
      :param filter_para: Frequency filter parameters. Defaults to None (no filtering applied).
      :type filter_para: list or None, optional

      :raises NotImplementedError: To be implemented in subclasses that handle specific data formats.















      ..
          !! processed by numpydoc !!


   .. py:method:: preprocess(raw, ica_=True, filter_para=None)
      :staticmethod:


      
      Preprocesses the raw EEG data by applying filtering and ICA for artifact removal.

      :param raw: Raw EEG data in MNE format.
      :type raw: mne.io.BaseRaw
      :param ica_: Whether to apply ICA for removing noise artifacts. Defaults to True.
                   - True: Apply ICA to remove artifacts (e.g., muscle, eye blink, heartbeat).
                   - False: Do not apply ICA.
      :type ica_: bool, optional
      :param filter_para: Frequency filter parameters. Defaults to None (no filtering applied).
                          - [low_fre, high_fre]: Apply band-pass filtering between low_fre and high_fre.
      :type filter_para: list or None, optional

      :returns: The preprocessed raw EEG data after optional filtering and ICA.
      :rtype: mne.io.BaseRaw















      ..
          !! processed by numpydoc !!


   .. py:attribute:: data_path


   .. py:attribute:: window_time


