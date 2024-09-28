scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_Tsinghua
=======================================================

.. py:module:: scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_Tsinghua


Attributes
----------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_Tsinghua.form_path_lee


Functions
---------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_Tsinghua.ssvep_classify


Module Contents
---------------

.. py:function:: ssvep_classify(form_path, pro_ica=True, filter_para=None, reconstruct_=False, reconstruct_type=0, classify_method='cca', psda_type='snr_hqy', freq_range=None)

   
   Classify SSVEP data using different classification methods.

   :param form_path: Path to the Excel file containing form data (subject_id, root_directory, file_name).
   :type form_path: str
   :param pro_ica: Whether to perform ICA during preprocessing. Defaults to True.
   :type pro_ica: bool, optional
   :param filter_para: Filter parameters [low_freq, high_freq]. Defaults to None (no filtering).
   :type filter_para: list, optional
   :param reconstruct_: Type of signal reconstruction. Defaults to None (no reconstruction).
                        Options:
                                "remove_aperiodic" - Reconstruct time signals and remove aperiodic components.
                                "get_periodic" - Reconstruct time signals and retain periodic components.
                                "get_aperiodic" - Reconstruct time signals and retain aperiodic components.
   :type reconstruct_: str, optional
   :param reconstruct_type: Type of reconstruction for the signal phase. Defaults to 0 (original phase).
                            Options:
                                    0 - With original phase.
                                    2 - With 0 phase.
   :type reconstruct_type: int, optional
   :param classify_method: Classification method to use. Defaults to "cca".
                           Options:
                                   "psda"
                                   "cca"
                                   "fbcca"
                                   "trca"
                                   "tdca"
   :type classify_method: str, optional
   :param psda_type: PSDA type, used when `classify_method` is "psda".
                     Options:
                             "snr_hqy"
                             "snr_hqy_ave_re"
                             "snr_hqy_ave_get". Defaults to "snr_hqy".
   :type psda_type: str, optional
   :param freq_range: Frequency range for filtering. Defaults to None.
   :type freq_range: list, optional

   :returns: Array of accuracy scores for each subject.
   :rtype: np.ndarray















   ..
       !! processed by numpydoc !!

.. py:data:: form_path_lee
   :value: 'D:\\data\\ssvep_dataset\\Tsinghua_dataset_ssvep_wearable\\ssvep_lee_sub_info.xlsx'


