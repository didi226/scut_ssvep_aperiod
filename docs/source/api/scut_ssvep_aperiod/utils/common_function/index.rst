scut_ssvep_aperiod.utils.common_function
========================================

.. py:module:: scut_ssvep_aperiod.utils.common_function


Attributes
----------

.. autoapisummary::

   scut_ssvep_aperiod.utils.common_function.D


Functions
---------

.. autoapisummary::

   scut_ssvep_aperiod.utils.common_function.cal_acc
   scut_ssvep_aperiod.utils.common_function.filterbank
   scut_ssvep_aperiod.utils.common_function.get_filelist
   scut_ssvep_aperiod.utils.common_function.ica_iclabel


Module Contents
---------------

.. py:function:: cal_acc(Y_true, Y_pred)

   
   Calculate accuracy

   :param Y_true: True labels
   :type Y_true: List[int]
   :param Y_pred: Predicted labels
   :type Y_pred: List[int]

   :returns: **acc** -- Accuracy
   :rtype: float















   ..
       !! processed by numpydoc !!

.. py:function:: filterbank(eeg, fs, idx_fb)

.. py:function:: get_filelist(dir, str='.mat')

   
   获取文件夹内后缀str的文件序列并且排序
   :param      dir        str      文件夹地址
   :param      str        str      后缀
   :return:    filelist   list
















   ..
       !! processed by numpydoc !!

.. py:function:: ica_iclabel(raw, n_components=None, remove_label={'muscle artifact': 0.9, 'eye blink': 0.9, 'heart beat': 0.9})

   
   去眼电 自动识别眼电通道去眼电
   :param raw:           mne raw 结构
   :return:
          reconst_raw:   去眼电后的raw结构
















   ..
       !! processed by numpydoc !!

.. py:data:: D

