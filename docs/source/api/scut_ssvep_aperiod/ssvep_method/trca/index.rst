scut_ssvep_aperiod.ssvep_method.trca
====================================

.. py:module:: scut_ssvep_aperiod.ssvep_method.trca


Attributes
----------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_method.trca.data_path


Classes
-------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_method.trca.TRCA


Module Contents
---------------

.. py:class:: TRCA(sfreq, ws, fres_list, n_harmonics, filter_=None)

   Bases: :py:obj:`scut_ssvep_aperiod.ssvep_method.ssvep_methd_base.CCABase`


   
   Class for Canonical Correlation Analysis (CCA) methods.

   Inherits from SSVEPMethodBase and adds harmonic analysis capabilities.

   .. attribute:: n_harmonics

      Number of harmonics to consider for reference signals.

      :type: int















   ..
       !! processed by numpydoc !!

   .. py:method:: classifier(test_data)

      
      Classifies test data using the trained TRCA model.

      :param test_data: Test data of shape (n_trials, n_channels, n_times).
      :type test_data: numpy.ndarray

      :returns: Predicted labels for test data.
      :rtype: numpy.ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: filter_bank(X)

      
      Applies a filter bank to the input EEG signals.

      :param X: Input EEG signals of shape (n_trials, n_channels, n_points).
      :type X: numpy.ndarray

      :returns: Filtered EEG signals of shape (n_fb, n_trials, n_channels, n_points).
      :rtype: numpy.ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: get_w(train_data, train_label)

      
      Computes the weight matrix for the TRCA method.

      :param train_data: Training data of shape (n_trials, n_channels, n_times).
      :type train_data: numpy.ndarray
      :param train_label: Labels for training data of shape (n_trials,).
      :type train_label: numpy.ndarray

      :returns: Weight matrix W of shape (n_events, n_channels).
                numpy.ndarray: Temporary matrix temp_X of shape (n_events, n_channels).
      :rtype: numpy.ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: train(train_data, train_label)

      
      Trains the TRCA model using the provided training data and labels.

      :param train_data: Training data of shape (n_trials, n_channels, n_times).
      :type train_data: numpy.ndarray
      :param train_label: Labels for training data of shape (n_trials,).
      :type train_label: numpy.ndarray

      :returns: Weight matrix w_all of shape (n_filters, n_channels).
                numpy.ndarray: Temporary matrix temp_x_all of shape (n_filters, n_trials).
      :rtype: numpy.ndarray















      ..
          !! processed by numpydoc !!


   .. py:attribute:: filter_


.. py:data:: data_path
   :value: 'D:\\data\\ssvep_dataset\\MNE-lee2019-ssvep-data\\session1\\s1\\sess01_subj01_EEG_SSVEP.mat'


