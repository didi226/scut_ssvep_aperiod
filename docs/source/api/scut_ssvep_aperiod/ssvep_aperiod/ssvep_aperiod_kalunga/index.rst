scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_kalunga
======================================================

.. py:module:: scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_kalunga


Attributes
----------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_kalunga.form_path_kang


Functions
---------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_aperiod.ssvep_aperiod_kalunga.ssvep_classify


Module Contents
---------------

.. py:function:: ssvep_classify(form_path, harmonic=3)

   
   Classify SSVEP data using CCA with specified harmonics.

   :param form_path: Path to the Excel file containing form data (subject_id, root_directory, file_name, effectiveness).
   :type form_path: str
   :param harmonic: Number of harmonics to use in the CCA classification. Defaults to 3.
   :type harmonic: int, optional

   :returns: Array of accuracy scores for each subject.
   :rtype: np.ndarray















   ..
       !! processed by numpydoc !!

.. py:data:: form_path_kang
   :value: 'D:\\data\\ssvep_dataset\\MNE-ssvepexo-data\\ssvep_kang_sub_info.xlsx'


