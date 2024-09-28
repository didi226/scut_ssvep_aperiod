scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_lee_parameter
============================================================

.. py:module:: scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_lee_parameter


Attributes
----------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_lee_parameter.form_path_lee


Functions
---------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_lee_parameter.cal_error_label_mean
   scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_lee_parameter.ssvep_classify_parameters


Module Contents
---------------

.. py:function:: cal_error_label_mean(test_label, error)

   
   Calculate the mean error for each label category.

   :param test_label: Array of true labels.
   :type test_label: np.ndarray
   :param error: Array of errors corresponding to predictions.
   :type error: np.ndarray

   :returns: Mean error for each of the 4 label categories.
   :rtype: np.ndarray















   ..
       !! processed by numpydoc !!

.. py:function:: ssvep_classify_parameters(form_path, info_path, pro_ica=True, filter_para=None, reconstruct_=False, reconstruct_type=0, classify_method='cca', psda_type='snr_hqy', freq_range=None)

   
   Classifies SSVEP data using different classification methods.

   :param form_path: Path to the Excel file containing form data (subject_id, root_directory, file_name).
   :type form_path: str
   :param info_path: Path to the info file (MAT file with data information).
   :type info_path: str
   :param pro_ica: Whether to perform ICA during preprocessing. Defaults to True.
   :type pro_ica: bool, optional
   :param filter_para: List specifying filter parameters [low_freq, high_freq]. Defaults to None (no filtering).
   :type filter_para: list, optional
   :param reconstruct_: Whether to reconstruct the data. Defaults to False.
   :type reconstruct_: bool, optional
   :param reconstruct_type: Type of reconstruction. Defaults to 0 (with original phase).
                            2 indicates reconstruction with 0 phase.
   :type reconstruct_type: int, optional
   :param classify_method: Classification method to use. Options are:
                           "psda", "cca", "fbcca", "trca", "tdca". Defaults to "cca".
   :type classify_method: str, optional
   :param psda_type: PSDA type, used when classify_method is "psda".
                     Options include "snr_hqy_ave_re", "snr_hqy", "snr_hqy_ave_get". Defaults to "snr_hqy".
   :type psda_type: str, optional
   :param freq_range: Frequency range for filtering. Defaults to None.
   :type freq_range: list, optional

   :returns:         error_all (np.ndarray): Array of average classification errors for each subject and label category.
                     r_squa_all (np.ndarray): Array of average R-square values for each subject and label category.
                     error_all_1 (np.ndarray): Array of slope estimation errors for each subject and label category.
                     r_squa_all_1 (np.ndarray): Array of slope estimation R-square values for each subject and label category.
   :rtype: tuple















   ..
       !! processed by numpydoc !!

.. py:data:: form_path_lee
   :value: 'D:\\data\\ssvep_dataset\\MNE-lee2019-ssvep-data\\ssvep_lee_sub_info.xlsx'


