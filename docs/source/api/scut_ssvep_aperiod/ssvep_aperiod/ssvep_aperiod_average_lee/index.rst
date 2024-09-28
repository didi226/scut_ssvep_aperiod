scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_average_lee
==========================================================

.. py:module:: scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_average_lee


Attributes
----------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_average_lee.form_path_lee


Functions
---------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_average_lee.average_by_label
   scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_average_lee.difference_of_two_max
   scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_average_lee.ssvep_classify


Module Contents
---------------

.. py:function:: average_by_label(test_data, test_label, unique_labels)

   
   Average the data by unique label.

   :param test_data: The test data with shape (samples, channels, timepoints).
   :type test_data: np.ndarray
   :param test_label: Array of labels corresponding to the test data.
   :type test_label: np.ndarray
   :param unique_labels: List of unique labels for averaging the data.
   :type unique_labels: list

   :returns: Averaged data with shape (len(unique_labels), channels, timepoints).
   :rtype: np.ndarray















   ..
       !! processed by numpydoc !!

.. py:function:: difference_of_two_max(mylist, i)

   
   Calculate the difference ratio between the max value and the second max value in a list.

   :param mylist: List of numerical values.
   :type mylist: list
   :param i: Index to compare the difference from the top two maximum values.
   :type i: int

   :returns: Difference ratio between the value at index `i` and the second highest value.
   :rtype: float















   ..
       !! processed by numpydoc !!

.. py:function:: ssvep_classify(form_path, info_path, pro_ica=True, filter_para=None, reconstruct_=False, reconstruct_type=0, classify_method='cca', psda_type='snr_hqy', freq_range=None)

   
   SSVEP (Steady-State Visual Evoked Potential) classification and SNR calculation.

   :param form_path: Path to the form file (Excel file with subject info).
   :type form_path: str
   :param info_path: Path to the information file (MAT file for data).
   :type info_path: str
   :param pro_ica: Whether to apply ICA in preprocessing. Defaults to True.
   :type pro_ica: bool
   :param filter_para: Filter parameters, e.g., [low_freq, high_freq]. Defaults to None (no filter).
   :type filter_para: None or list
   :param reconstruct_: Whether to apply reconstruction. Defaults to False.
   :type reconstruct_: bool
   :param reconstruct_type: Type of reconstruction (0 = with original phase, 2 = with 0 phase). Defaults to 0.
   :type reconstruct_type: int
   :param classify_method: Classification method, options include "psda", "cca", "fbcca", "trca", "tdca". Defaults to "cca".
   :type classify_method: str
   :param psda_type: PSDA method type, options include "snr_hqy_ave_re", "snr_hqy", "snr_hqy_ave_get". Defaults to "snr_hqy".
   :type psda_type: str
   :param freq_range: Frequency range for analysis. Defaults to None.
   :type freq_range: None or list

   :returns: SNR values for each subject and frequency.
             np.ndarray: Difference of SNR values between the top two frequencies.
   :rtype: np.ndarray















   ..
       !! processed by numpydoc !!

.. py:data:: form_path_lee
   :value: 'D:\\data\\ssvep_dataset\\MNE-lee2019-ssvep-data\\ssvep_lee_sub_info.xlsx'


