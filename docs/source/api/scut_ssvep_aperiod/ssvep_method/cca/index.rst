scut_ssvep_aperiod.ssvep_method.cca
===================================

.. py:module:: scut_ssvep_aperiod.ssvep_method.cca


Classes
-------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_method.cca.CCACommon


Module Contents
---------------

.. py:class:: CCACommon(sfreq, ws, fres_list, n_harmonics)

   Bases: :py:obj:`scut_ssvep_aperiod.ssvep_method.ssvep_methd_base.CCABase`


   
   Class for Canonical Correlation Analysis (CCA) methods.

   Inherits from SSVEPMethodBase and adds harmonic analysis capabilities.

   .. attribute:: n_harmonics

      Number of harmonics to consider for reference signals.

      :type: int















   ..
       !! processed by numpydoc !!

   .. py:method:: _cca_classify(test_data, ica_=False)

      
      Classifies the test data using CCA.

      :param test_data: shape(n_channels,n_times)
      :type test_data: ndarray
      :param ica_: Whether to apply ICA.
      :type ica_: bool

      :returns: The index of the class with the highest correlation.
      :rtype: int















      ..
          !! processed by numpydoc !!


   .. py:method:: _cca_ex(test_data, ica_=False)

      
      Performs Canonical Correlation Analysis (CCA) on the provided test data.

      :param test_data: Input data with shape (n_channels, n_times).
      :type test_data: ndarray
      :param ica_: Flag indicating whether to apply Independent Component Analysis (ICA).
      :type ica_: bool

      :returns: The correlation results obtained from the CCA.
      :rtype: ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: calculate_ex(test_data, ica_=False)

      
      Calculates the CCA results for each sample in the test data.

      :param test_data: shape(n_epochs,n_channels,n_times)
      :type test_data: ndarray
      :param ica_: Whether to apply ICA.
      :type ica_: bool

      :returns: An array of CCA results for each sample.
      :rtype: ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: classify(test_data, ica_=False)

      
      Classifies the provided test data using Canonical Correlation Analysis (CCA).

      :param test_data: Input data with shape (n_channels, n_times).
      :type test_data: ndarray
      :param ica_: Flag indicating whether to apply ICA.
      :type ica_: bool

      :returns: The index of the class with the highest correlation result.
      :rtype: int















      ..
          !! processed by numpydoc !!


