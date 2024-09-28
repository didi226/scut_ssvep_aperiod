scut_ssvep_aperiod.ssvep_method.ssvep_methd_base
================================================

.. py:module:: scut_ssvep_aperiod.ssvep_method.ssvep_methd_base


Classes
-------

.. autoapisummary::

   scut_ssvep_aperiod.ssvep_method.ssvep_methd_base.CCABase
   scut_ssvep_aperiod.ssvep_method.ssvep_methd_base.SSVEPMethodBase


Module Contents
---------------

.. py:class:: CCABase(sfreq, ws, fres_list, n_harmonics)

   Bases: :py:obj:`SSVEPMethodBase`


   
   Class for Canonical Correlation Analysis (CCA) methods.

   Inherits from SSVEPMethodBase and adds harmonic analysis capabilities.

   .. attribute:: n_harmonics

      Number of harmonics to consider for reference signals.

      :type: int















   ..
       !! processed by numpydoc !!

   .. py:method:: find_correlation(n_components, X, Y)

      
      Finds the maximum correlation between data and reference signals.

      :param n_components: Number of components for CCA.
      :type n_components: int
      :param X: Data matrix (trials x features).
      :type X: np.ndarray
      :param Y: Reference signals (frequencies x time).
      :type Y: np.ndarray

      :returns: Maximum correlation values for each frequency.
      :rtype: np.ndarray















      ..
          !! processed by numpydoc !!


   .. py:method:: get_reference_signal()

      
      Generates reference signals for each frequency and harmonic.

      :returns: An array of reference signals shaped as (n_events, n_harmonics * 2, T).
      :rtype: np.ndarray















      ..
          !! processed by numpydoc !!


   .. py:attribute:: n_harmonics


.. py:class:: SSVEPMethodBase(sfreq, ws, fres_list)

   
   Base class for SSVEP methods.

   .. attribute:: sfreq

      Sampling frequency of the data.

      :type: float

   .. attribute:: ws

      Window size in seconds.

      :type: float

   .. attribute:: T

      Number of samples per window.

      :type: int

   .. attribute:: fres_list

      List of frequencies for stimulation.

      :type: list

   .. attribute:: n_event

      Number of events (stimuli).

      :type: int















   ..
       !! processed by numpydoc !!

   .. py:attribute:: T


   .. py:attribute:: fres_list


   .. py:attribute:: n_event


   .. py:attribute:: sfreq


   .. py:attribute:: ws


