scut_ssvep_aperiod.ssvep_method.fbcca
=====================================

.. py:module:: scut_ssvep_aperiod.ssvep_method.fbcca


Attributes
----------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_method.fbcca.data_path


Classes
-------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_method.fbcca.FBCCA


Module Contents
---------------

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


.. py:data:: data_path
   :value: 'D:\\data\\ssvep_dataset\\MNE-lee2019-ssvep-data\\session1\\s1\\sess01_subj01_EEG_SSVEP.mat'


