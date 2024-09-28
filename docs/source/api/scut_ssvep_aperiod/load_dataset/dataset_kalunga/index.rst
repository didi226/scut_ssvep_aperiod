scut_ssvep_aperiod.load_dataset.dataset_kalunga
===============================================

.. py:module:: scut_ssvep_aperiod.load_dataset.dataset_kalunga


Attributes
----------

.. autoapisummary::

   scut_ssvep_aperiod.load_dataset.dataset_kalunga.ssvep_data_kalunga


Classes
-------

.. autoapisummary::

   scut_ssvep_aperiod.load_dataset.dataset_kalunga.LoadDataKalungaOne


Functions
---------

.. autoapisummary::

   scut_ssvep_aperiod.load_dataset.dataset_kalunga.get_data_path_list


Module Contents
---------------

.. py:class:: LoadDataKalungaOne(data_path)

   Bases: :py:obj:`scut_ssvep_aperiod.load_dataset.dataset_base.LoadDataBase`


   
   Class for loading and preprocessing SSVEP data from the KalungaOne dataset.

   :param data_path: Path to the dataset file.
   :type data_path: str

   .. attribute:: window_time

      The time window for data processing (default is 5 seconds).

      :type: float















   ..
       !! processed by numpydoc !!

   .. py:method:: get_data(ica_=True, filter_para=None, resample=None)

      
      Loads and preprocesses the EEG data, extracts epochs, and returns the data and labels.

      :param ica_: Whether to apply ICA for noise removal. Defaults to True.
      :type ica_: bool, optional
      :param filter_para: Frequency filter parameters. Defaults to None (no filtering applied).
      :type filter_para: list or None, optional
      :param resample: Optionally resample the data. Defaults to None.
      :type resample: int or None, optional

      :returns: The preprocessed EEG data with shape (n_epochs, n_channels, n_times).
                np.ndarray: Labels for the data indicating the event type (based on frequency).
      :rtype: np.ndarray















      ..
          !! processed by numpydoc !!


   .. py:attribute:: window_time
      :value: 5



.. py:function:: get_data_path_list(form_path)

   
   Randomly marks two sessions per subject as effective in the input Excel file.

   :param form_path: Path to the Excel file containing subject and session information.
   :type form_path: str

   :returns: None. The modified Excel file is saved with an 'effectiveness' column indicating selected sessions.















   ..
       !! processed by numpydoc !!

.. py:data:: ssvep_data_kalunga

