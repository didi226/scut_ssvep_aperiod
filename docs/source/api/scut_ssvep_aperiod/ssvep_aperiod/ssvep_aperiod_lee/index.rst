scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_lee
==================================================

.. py:module:: scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_lee


Attributes
----------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_lee.form_path_lee


Functions
---------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_lee.ssvep_classify


Module Contents
---------------

.. py:function:: ssvep_classify(form_path, info_path, pro_ica=True, filter_para=None, reconstruct_=False, reconstruct_type=0, classify_method='cca', psda_type='snr_hqy', freq_range=None)

   
   Classifies SSVEP data using different classification methods and preprocessing options.

   :param form_path: Path to the form file, which contains subject information (subject_id, root_directory, file_name).
   :type form_path: str
   :param info_path: Path to the information file (e.g., .mat file) needed for data loading.
   :type info_path: str
   :param pro_ica: Whether to apply ICA preprocessing. Defaults to True.
   :type pro_ica: bool, optional
   :param filter_para: Parameters for filtering [low_freq, high_freq]. Defaults to None (no filtering).
   :type filter_para: list or None, optional
   :param reconstruct_: Whether to apply reconstruction. Defaults to False.
   :type reconstruct_: bool, optional
   :param reconstruct_type: Type of reconstruction to apply. Defaults to 0.
                            0: With original phase.
                            2: With zero phase.
   :type reconstruct_type: int, optional
   :param classify_method: Classification method to use. Options are:
                           - "psda"
                           - "cca"
                           - "fbcca"
                           - "trca"
                           - "tdca"
                           Defaults to "cca".
   :type classify_method: str, optional
   :param psda_type: Type of PSDA (only applicable when `classify_method` is "psda"). Options are:
                     - "snr_hqy_ave_re"
                     - "snr_hqy"
                     - "snr_hqy_ave_get"
   :type psda_type: str, optional
   :param freq_range: Frequency range for analysis. Defaults to None.
   :type freq_range: list or None, optional

   :returns: Array of classification accuracies for each subject.
   :rtype: np.ndarray















   ..
       !! processed by numpydoc !!

.. py:data:: form_path_lee
   :value: 'D:\\data\\ssvep_dataset\\MNE-lee2019-ssvep-data\\ssvep_lee_sub_info.xlsx'


