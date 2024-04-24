from scut_ssvep_aperiod.load_dataset.dataset_kalunga import LoadDataKalungaOne
from scut_ssvep_aperiod.load_dataset.dataset_lee import LoadDataLeeOne
from scut_ssvep_aperiod.ssvep_method.cca import CCA_Base
from scut_ssvep_aperiod.utils.common_function import cal_acc
import pandas as pd
import numpy as np
import os
def ssvep_classify(form_path, harmonic = 3):
	info_form = pd.read_excel(form_path)
	unique_subject_ids = info_form['subject_id'].unique()
	acc_all = np.zeros(len(unique_subject_ids))
	for subject_id in unique_subject_ids:
		subject_rows = info_form.loc[info_form['subject_id'] == subject_id]
		data_sub = []
		label_sub = []
		for index, row in subject_rows.iterrows():
			if row['effectiveness'] == 1:
				root_directory = row['root_directory']
				file_name = row['file_name']
				data_path = os.path.join(root_directory, file_name)
				datasetone = LoadDataKalungaOne(data_path)
				data, label = datasetone.get_data(ica_ = False,filter_para = [8,60])
				data_sub.extend(data)
				label_sub.extend(label)
		data_sub = np.array(data_sub)
		Y_test = np.array(label_sub)
		pred_label = []
		for i_data, i_label in zip(data_sub, Y_test):
		# cca
			ccaoriginal_classify = CCA_Base(Fs = datasetone.sample_rate, ws = datasetone.window_time)
			predict_label = ccaoriginal_classify.cca_classify(datasetone.freqs, i_data, num_harmonics = harmonic, ica_ = False)
			pred_label.append(predict_label)
			del ccaoriginal_classify
			#
			# PSD_temp = BuildPSDPeriod(i_data[0, :, :], 1000 / downsample_factor)
			# spectrum, freqs = PSD_temp.data_to_psd(psd_type = psd_type)
			# del PSD_temp
			# psd_classify = PSDA_SSVEP(spectrum, freqs, [60.0 / 5.0, 60.0 / 7.0, 60.0 / 9.0, 60.0 / 11.0],
			#                           psd_channel= psd_channel, harmonic= harmonic,sfreq = 1000 / downsample_factor)
			# pred_label_temp, error_temp, r_squa_temp = psd_classify.psda_classify(psda_type=psda_type)
			# pred_label.append(pred_label_temp)
			# error.append(error_temp)
			# r_squa.append(r_squa_temp)
			# del psd_classify
		acc = cal_acc(Y_true=Y_test, Y_pred = pred_label)
		print(Y_test, pred_label)
		print(acc)
		print(subject_id)
		acc_all[subject_id-1] = acc
	print(acc_all.mean())
if __name__ == "__main__":
	form_path_kang = "D:\data\ssvep_dataset\MNE-ssvepexo-data\ssvep_kang_sub_info.xlsx"
	ssvep_classify(form_path_kang)






# ssvep_data_kalunga = LoadDataKalungaOne(data_path = r"D:\data\ssvep_dataset\MNE-ssvepexo-data\subject01\subject01_run1_raw.fif")
# x, y = ssvep_data_kalunga.get_data()
# print(x.shape, y.shape)