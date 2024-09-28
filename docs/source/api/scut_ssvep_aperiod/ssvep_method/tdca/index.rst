scut_ssvep_aperiod.ssvep_method.tdca
====================================

.. py:module:: scut_ssvep_aperiod.ssvep_method.tdca


Attributes
----------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_method.tdca.data_path


Classes
-------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_method.tdca.TDCA


Functions
---------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_method.tdca.isPD
   scut_ssvep_aperiod.ssvep_method.tdca.lagging_aug
   scut_ssvep_aperiod.ssvep_method.tdca.nearestPD
   scut_ssvep_aperiod.ssvep_method.tdca.proj_ref
   scut_ssvep_aperiod.ssvep_method.tdca.robust_pattern
   scut_ssvep_aperiod.ssvep_method.tdca.tdca_feature
   scut_ssvep_aperiod.ssvep_method.tdca.xiang_dsp_feature
   scut_ssvep_aperiod.ssvep_method.tdca.xiang_dsp_kernel


Module Contents
---------------

.. py:class:: TDCA(sfreq, ws, fres_list, n_harmonics, Nc=10, Nm=1, passband=[6, 14, 22, 30, 38], stopband=[4, 10, 16, 24, 32], highcut_pass=40, highcut_stop=50, lagging_len=0)

   Bases: :py:obj:`scut_ssvep_aperiod.ssvep_method.ssvep_methd_base.CCABase`


   
   Class for TDCA (Temporal Discriminative Component Analysis).

   .. attribute:: sfreq

      Sampling frequency.

      :type: float

   .. attribute:: ws

      Window size.

      :type: int

   .. attribute:: fres_list

      Frequency list.

      :type: list

   .. attribute:: n_harmonics

      Number of harmonics.

      :type: int

   .. attribute:: Nm

      Number of channels.

      :type: int

   .. attribute:: Nc

      Number of components.

      :type: int

   .. attribute:: lagging_len

      Lagging length.

      :type: int

   .. attribute:: passband

      Passband frequencies.

      :type: list

   .. attribute:: stopband

      Stopband frequencies.

      :type: list

   .. attribute:: highcut_pass

      Highcut pass frequency.

      :type: float

   .. attribute:: highcut_stop

      Highcut stop frequency.

      :type: float















   ..
       !! processed by numpydoc !!

   .. py:method:: calculate_ex()

      
      Calculate features from the last transformation.

      :returns: Extracted features.
      :rtype: ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: classifier(X)

      
      Classify input EEG signals.

      :param X: Input EEG signals (n_trials, n_channels, n_points).
      :type X: ndarray

      :returns: Predicted labels (n_trials,).
      :rtype: ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: filter_bank(X)

      
      Apply filter bank to EEG signals.

      :param X: Input EEG signals (n_trials, n_channels, n_points).
      :type X: ndarray

      :returns: Output EEG signals of filter banks (n_fb, n_trials, n_channels, n_points).
      :rtype: ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: train(X, y)

      
      Train the TDCA model on input EEG signals and labels.

      :param X: Input EEG signals (n_trials, n_channels, n_points).
      :type X: ndarray
      :param y: Input labels (n_trials,).
      :type y: ndarray

      :returns: TDCA object.
      :rtype: self















      ..
          !! processed by numpydoc !!


   .. py:method:: transform(X, fb_i)

      
      Transform input EEG signals into features.

      :param X: Input EEG signals (n_trials, n_channels, n_points).
      :type X: ndarray
      :param fb_i: Filter bank index.
      :type fb_i: int

      :returns: Feature vectors (n_trials, n_freq).
      :rtype: ndarray















      ..
          !! processed by numpydoc !!


   .. py:attribute:: Nc


   .. py:attribute:: Nf


   .. py:attribute:: Nm


   .. py:attribute:: highcut_pass


   .. py:attribute:: highcut_stop


   .. py:attribute:: lagging_len


   .. py:attribute:: n_components
      :value: 3



   .. py:attribute:: passband


   .. py:attribute:: stopband


.. py:function:: isPD(B)

   
   Checks if the input matrix is positive-definite using Cholesky decomposition.

   This function determines whether the matrix B is positive-definite by attempting
   to perform a Cholesky decomposition. If the decomposition succeeds, the matrix
   is positive-definite; otherwise, it is not.

   :param B: Any matrix, shape (N, N).
   :type B: ndarray

   :returns: True if B is positive-definite, False otherwise.
   :rtype: bool















   ..
       !! processed by numpydoc !!

.. py:function:: lagging_aug(X, n_samples, lagging_len, P, training)

   
   Augment EEG signals with lagging.

   :param X: Input EEG signals (n_trials, n_channels, n_points).
   :type X: ndarray
   :param n_samples: Number of delayed sample points.
   :type n_samples: int
   :param lagging_len: Lagging length.
   :type lagging_len: int
   :param P: Projection matrix (n_points, n_points).
   :type P: ndarray
   :param training: True for training, False for testing.
   :type training: bool

   :returns: Augmented EEG signals (n_trials, (lagging_len + 1) * n_channels, n_samples).
   :rtype: ndarray

   :raises ValueError: If the length of X is not greater than lagging_len + n_samples.















   ..
       !! processed by numpydoc !!

.. py:function:: nearestPD(A)

   
   Finds the nearest positive-definite matrix to the input.

   :param A: Any square matrix, shape (N, N).
   :type A: ndarray

   :returns: Positive-definite matrix closest to A.
   :rtype: ndarray

   .. rubric:: References

   N.J. Higham, "Computing a nearest symmetric positive semidefinite matrix" (1988):
   https://doi.org/10.1016/0024-3795(88)90223-6















   ..
       !! processed by numpydoc !!

.. py:function:: proj_ref(Yf)

   
   Calculate the projection matrix from Sin-Cosine reference signals.

   :param Yf: Sin-Cosine reference signals (n_freq, 2 * num_harmonics, n_points).
   :type Yf: ndarray

   :returns: Projection matrix.
   :rtype: ndarray















   ..
       !! processed by numpydoc !!

.. py:function:: robust_pattern(W, Cx, Cs)

   
   Transforms spatial filters to spatial patterns based on the method described in the literature.

   This function constructs spatial patterns from spatial filters, which illustrates how to combine
   information from different EEG channels to extract signals of interest. For neurophysiological
   interpretation or visualization of weights, it is essential to derive activation patterns from
   the obtained spatial filters.

   :param W: Spatial filters, shape (n_channels, n_filters).
   :type W: ndarray
   :param Cx: Covariance matrix of EEG data, shape (n_channels, n_channels).
   :type Cx: ndarray
   :param Cs: Covariance matrix of source data, shape (n_channels, n_channels).
   :type Cs: ndarray

   :returns: Spatial patterns, shape (n_channels, n_patterns), where each column represents a
             spatial pattern.
   :rtype: ndarray

   .. rubric:: References

   Haufe, Stefan, et al. "On the interpretation of weight vectors of linear models in multivariate
   neuroimaging." Neuroimage 87 (2014): 96-110.

   .. rubric:: Notes

   Use `linalg.solve` instead of `inv` to enhance numerical stability.
   For more details, see:
   - https://github.com/robintibor/fbcsp/blob/master/fbcsp/signalproc.py
   - https://ww2.mathworks.cn/help/matlab/ref/mldivide.html















   ..
       !! processed by numpydoc !!

.. py:function:: tdca_feature(X, templates, W, M, Ps, lagging_len, n_components, training=False)

   
   Compute the TDCA feature.

   :param X: Input EEG signals (n_trials, n_channels, n_points).
   :type X: ndarray
   :param templates: EEG template signals (n_freq, n_channels, n_points).
   :type templates: ndarray
   :param W: Spatial filters (n_channels, n_filters).
   :type W: ndarray
   :param M: Common templates for all categories (n_channels, n_points).
   :type M: ndarray
   :param Ps: Projection matrices (n_freq, n_channels, n_points).
   :type Ps: list
   :param lagging_len: Lagging length.
   :type lagging_len: int
   :param n_components: Number of components.
   :type n_components: int
   :param training: True for training, False for testing.
   :type training: bool

   :returns: Correlation coefficients (n_freq,).
   :rtype: list















   ..
       !! processed by numpydoc !!

.. py:function:: xiang_dsp_feature(W, M, X, n_components)

   
   Return DSP features as described in the paper.

   :param W: Spatial filters (n_channels, n_filters).
   :type W: ndarray
   :param M: Common template for all classes (n_channel, n_samples).
   :type M: ndarray
   :param X: EEG test data (n_trials, n_channels, n_samples).
   :type X: ndarray
   :param n_components: Length of the spatial filters; first k components to use (default is 1).
   :type n_components: int, optional

   :returns: Features (n_trials, n_components, n_samples).
   :rtype: ndarray

   :raises ValueError: If n_components is greater than the number of channels.

   .. rubric:: References

   Liao, Xiang, et al. "Combining spatial filters for the classification of single-trial EEG in a finger movement task."
   IEEE Transactions on Biomedical Engineering 54.5 (2007): 821-831.















   ..
       !! processed by numpydoc !!

.. py:function:: xiang_dsp_kernel(X, y)

   
   DSP: Discriminative Spatial Patterns, only for two classes.

   This function solves spatial filters with DSP by finding a projection matrix
   that maximizes the between-class scatter matrix and minimizes the within-class
   scatter matrix. Currently, it supports only two types of data.

   :param X: EEG train data (n_trials, n_channels, n_samples) with mean removed.
   :type X: ndarray
   :param y: Labels of EEG data (n_trials,).
   :type y: ndarray

   :returns:     W (ndarray): Spatial filters (n_channels, n_filters).
                 D (ndarray): Eigenvalues in descending order.
                 M (ndarray): Mean value of all classes and trials (n_channel, n_samples).
                 A (ndarray): Spatial patterns (n_channels, n_filters).
   :rtype: tuple

   :raises ValueError: If the number of components exceeds the number of channels.

   .. rubric:: References

   Liao, Xiang, et al. "Combining spatial filters for the classification of single-trial EEG in a finger movement task."
   IEEE Transactions on Biomedical Engineering 54.5 (2007): 821-831.















   ..
       !! processed by numpydoc !!

.. py:data:: data_path
   :value: 'D:\\data\\ssvep_dataset\\MNE-lee2019-ssvep-data\\session1\\s1\\sess01_subj01_EEG_SSVEP.mat'


