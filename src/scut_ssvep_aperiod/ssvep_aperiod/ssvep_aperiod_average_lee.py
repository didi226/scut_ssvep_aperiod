from scut_ssvep_aperiod.load_dataset.dataset_kalunga import LoadDataKalungaOne
from scut_ssvep_aperiod.load_dataset.dataset_lee import LoadDataLeeOne
from scut_ssvep_aperiod.ssvep_method import CCACommon,TRCA,FBCCA,TDCA,PSDA
from scut_ssvep_aperiod.utils.common_function import cal_acc
import pandas as pd
import numpy as np
import os


def average_by_label(test_data, test_label,unique_labels):
	"""
	Average the data by unique label.

	Args:
		test_data (np.ndarray): The test data with shape (samples, channels, timepoints).
		test_label (np.ndarray): Array of labels corresponding to the test data.
		unique_labels (list): List of unique labels for averaging the data.

	Returns:
		np.ndarray: Averaged data with shape (len(unique_labels), channels, timepoints).
	"""
	averaged_data_dict = {}
	for label in unique_labels:
		indices = np.where(test_label == label)
		data_subset = test_data[indices]
		averaged_data_dict[label] = np.mean(data_subset, axis=0)
	num_labels = len(unique_labels)
	n_channel = test_data.shape[1]
	n_times = test_data.shape[2]
	averaged_data = np.empty((num_labels, n_channel, n_times))
	for i, label in enumerate(unique_labels):
		averaged_data[i] = averaged_data_dict[label]
	return averaged_data
def difference_of_two_max(mylist,i):
	"""
	Calculate the difference ratio between the max value and the second max value in a list.

	Args:
		mylist (list): List of numerical values.
		i (int): Index to compare the difference from the top two maximum values.

	Returns:
		float: Difference ratio between the value at index `i` and the second highest value.
	"""
	enumerated_list = list(enumerate(mylist))
	sorted_list = sorted(enumerated_list, key=lambda x: x[1], reverse=True)
	top_two_positions = [index for index, value in sorted_list[:2]]
	if i == top_two_positions[0] :
		result = (mylist[i]-mylist[top_two_positions[1]])/mylist[i]
	else:
		result = (mylist[i] - mylist[top_two_positions[0]])/mylist[i]
	return result
def ssvep_classify(form_path, info_path, pro_ica=True, filter_para=None, reconstruct_=False, reconstruct_type=0,
                   classify_method="cca", psda_type="snr_hqy",freq_range=None):
	"""
	SSVEP (Steady-State Visual Evoked Potential) classification and SNR calculation.

	Args:
		form_path (str): Path to the form file (Excel file with subject info).
		info_path (str): Path to the information file (MAT file for data).
		pro_ica (bool): Whether to apply ICA in preprocessing. Defaults to True.
		filter_para (None or list): Filter parameters, e.g., [low_freq, high_freq]. Defaults to None (no filter).
		reconstruct_ (bool): Whether to apply reconstruction. Defaults to False.
		reconstruct_type (int): Type of reconstruction (0 = with original phase, 2 = with 0 phase). Defaults to 0.
		classify_method (str): Classification method, options include "psda", "cca", "fbcca", "trca", "tdca". Defaults to "cca".
		psda_type (str): PSDA method type, options include "snr_hqy_ave_re", "snr_hqy", "snr_hqy_ave_get". Defaults to "snr_hqy".
		freq_range (None or list): Frequency range for analysis. Defaults to None.

	Returns:
		np.ndarray: SNR values for each subject and frequency.
		np.ndarray: Difference of SNR values between the top two frequencies.
	"""
	info_form = pd.read_excel(form_path)
	unique_subject_ids = info_form['subject_id'].unique()
	acc_all = np.zeros(len(unique_subject_ids))
	snr = np.zeros((len(unique_subject_ids),4))
	dif_snr = np.zeros((len(unique_subject_ids),4))
	for subject_id in unique_subject_ids:
		subject_rows = info_form.loc[info_form['subject_id'] == subject_id]
		root_directory = subject_rows['root_directory'].tolist()
		file_name = subject_rows['file_name'].tolist()
		data_path = os.path.join(root_directory[0], file_name[0])
		datasetone = LoadDataLeeOne(data_path,info_path = info_path)
		test_data, test_label, train_data, train_label = datasetone.get_data(pro_ica=pro_ica, filter_para=filter_para,
                                                            resample = 4, reconstruct_=reconstruct_,
                                                            reconstruct_type=reconstruct_type,freq_range=freq_range)
		test_data = test_data [:,:9,:]
		train_data = train_data [:,:9,:]
		test_data = average_by_label(test_data,test_label,[0,1,2,3])
		if classify_method == "psda":
			save_path_base = os.path.join(r"D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\save_figure",f'subject{subject_id}')
			#绘图
			# ssvep_method = PSDA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs, 3, psd_type="Ordinary", # "remove_aperiodic"
			#                     psd_channel = "ave", psda_type=psda_type,freq_range=[3,40],figure_=True,save_path_base=save_path_base) #"snr_hqy_ave_re"
			# predict_label = ssvep_method.classify(test_data)
			#计算SNR
			ssvep_method = PSDA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs, 3,
			                    psd_type="Ordinary",  # "remove_aperiodic"
			                    psd_channel="ave", psda_type=psda_type, freq_range=[3, 40], figure_=False,
			                    save_path_base=save_path_base)  # "snr_hqy_ave_re"
			snr_temp = ssvep_method.calculate_snr(test_data)

		if classify_method == "cca":
			ssvep_method = CCACommon(sfreq=datasetone.sample_rate_test, ws=datasetone.window_time,
			                         fres_list=datasetone.freqs, n_harmonics=3)
			snr_temp = ssvep_method.calculate_ex(test_data, ica_ = False)
		elif classify_method == "fbcca":
			ssvep_method = FBCCA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs, 3)
			_ = ssvep_method.classify(test_data)
			snr_temp = ssvep_method.calculate_ex()
		# elif classify_method == "trca":
		# 	ssvep_method = TRCA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs, [3.4,40])
		# 	ssvep_method.train(train_data, train_label)
		# 	predict_label = ssvep_method.classifier(test_data)
		elif classify_method == "tdca":
			ssvep_method = TDCA(datasetone.sample_rate_test,3.848,
			                    datasetone.freqs,3,9,1,[6, 14, 22, 30, 38],[4, 10, 16, 24, 32],40,50,3)# datasetone.window_time
			ssvep_method.train(train_data, train_label)
			_ = ssvep_method.classifier(test_data)
			snr_temp = ssvep_method.calculate_ex()
		del ssvep_method
		for i in range(4):
			snr[subject_id - 1,i] = snr_temp[i, i]
			dif_snr[subject_id - 1, i] = difference_of_two_max(snr_temp[i, :].tolist(), i)


	dif_snr = dif_snr[:, ::-1]
	snr = snr[:, ::-1]
	return snr, dif_snr
if __name__ == "__main__":
	form_path_lee = "D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\ssvep_lee_sub_info.xlsx"
	info_path = r"D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\info_ssvep_lee_dataset.mat"
	data = {}
	columns = [5.45,6.67,8.57,12]
	##plot
	# snr, dif_snr = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40], reconstruct_=False,
	#                      reconstruct_type=None, classify_method="psda", psda_type="snr_hqy_ave_re",freq_range=None)
	# snr
	for psda_type in ["snr_hqy","snr_hqy_ave_re","snr_hqy_ave_get"]:
		save_path = os.path.join(r"C:\Users\15956\Desktop\ssvep_result\psda",f"{psda_type}.xlsx")
		snr, dif_snr = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40], reconstruct_=False,
		                              reconstruct_type=None, classify_method="psda", psda_type=psda_type, freq_range=None)
		with pd.ExcelWriter(save_path, mode='w') as writer:
			pd.DataFrame(snr,columns=columns).to_excel(writer, index=False, sheet_name='snr')
		with pd.ExcelWriter(save_path, mode='a', if_sheet_exists='replace') as writer:
			pd.DataFrame(dif_snr,columns=columns).to_excel(writer, index=False, sheet_name='dif_snr')



	snr, dif_snr = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40],
	                     reconstruct_=False, reconstruct_type=None, classify_method="cca",freq_range=None)
	save_path = os.path.join(r"C:\Users\15956\Desktop\ssvep_result\cca", "cca_original.xlsx")
	with pd.ExcelWriter(save_path, mode='w') as writer:
		pd.DataFrame(snr,columns=columns).to_excel(writer, index=False,  sheet_name='snr')
	with pd.ExcelWriter(save_path, mode='a', if_sheet_exists='replace') as writer:
		pd.DataFrame(dif_snr,columns=columns).to_excel(writer, index=False,  sheet_name='dif_snr')

	snr, dif_snr = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3,40],
	                     reconstruct_="remove_aperiodic", reconstruct_type=0, classify_method="cca",freq_range=[3,40])
	save_path = os.path.join(r"C:\Users\15956\Desktop\ssvep_result\cca", "cca_pe.xlsx")
	with pd.ExcelWriter(save_path, mode='w') as writer:
		pd.DataFrame(snr,columns=columns).to_excel(writer, index=False,  sheet_name='snr')
	with pd.ExcelWriter(save_path, mode='a', if_sheet_exists='replace') as writer:
		pd.DataFrame(dif_snr,columns=columns).to_excel(writer, index=False, sheet_name='dif_snr')

	snr, dif_snr = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3,40],
	                     reconstruct_="get_aperiodic", reconstruct_type=0, classify_method="cca",freq_range=[3,40])
	save_path = os.path.join(r"C:\Users\15956\Desktop\ssvep_result\cca", "cca_ap.xlsx")
	with pd.ExcelWriter(save_path, mode='w') as writer:
		pd.DataFrame(snr,columns=columns).to_excel(writer, index=False,  sheet_name='snr')
	with pd.ExcelWriter(save_path, mode='a', if_sheet_exists='replace') as writer:
		pd.DataFrame(dif_snr,columns=columns).to_excel(writer, index=False, sheet_name='dif_snr')

	#
	snr, dif_snr = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40],
	                              reconstruct_=False,reconstruct_type=None, classify_method="fbcca",freq_range=None)
	save_path = os.path.join(r"C:\Users\15956\Desktop\ssvep_result\cca", "fbcca_original.xlsx")
	with pd.ExcelWriter(save_path, mode='w') as writer:
		pd.DataFrame(snr,columns=columns).to_excel(writer, index=False,  sheet_name='snr')
	with pd.ExcelWriter(save_path, mode='a', if_sheet_exists='replace') as writer:
		pd.DataFrame(dif_snr,columns=columns).to_excel(writer, index=False,  sheet_name='dif_snr')

	snr, dif_snr = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40],
	                              reconstruct_="remove_aperiodic", reconstruct_type=0, classify_method="fbcca",freq_range=[3, 40])
	save_path = os.path.join(r"C:\Users\15956\Desktop\ssvep_result\cca", "fbcca_pe.xlsx")
	with pd.ExcelWriter(save_path, mode='w') as writer:
		pd.DataFrame(snr,columns=columns).to_excel(writer, index=False, sheet_name='snr')
	with pd.ExcelWriter(save_path, mode='a', if_sheet_exists='replace') as writer:
		pd.DataFrame(dif_snr,columns=columns).to_excel(writer, index=False, sheet_name='dif_snr')

	snr, dif_snr = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40],
	                              reconstruct_="get_aperiodic", reconstruct_type=0, classify_method="fbcca",freq_range=[3, 40])
	save_path = os.path.join(r"C:\Users\15956\Desktop\ssvep_result\cca", "fbcca_ap.xlsx")
	with pd.ExcelWriter(save_path, mode='w') as writer:
		pd.DataFrame(snr,columns=columns).to_excel(writer, index=False,  sheet_name='snr')
	with pd.ExcelWriter(save_path, mode='a', if_sheet_exists='replace') as writer:
		pd.DataFrame(dif_snr,columns=columns).to_excel(writer, index=False, sheet_name='dif_snr')

	snr, dif_snr = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40],
	                              reconstruct_=False,reconstruct_type=None, classify_method="tdca",freq_range=None)
	save_path = os.path.join(r"C:\Users\15956\Desktop\ssvep_result\cca", "tdca_original.xlsx")
	with pd.ExcelWriter(save_path, mode='w') as writer:
		pd.DataFrame(snr,columns=columns).to_excel(writer, index=False, sheet_name='snr')
	with pd.ExcelWriter(save_path, mode='a', if_sheet_exists='replace') as writer:
		pd.DataFrame(dif_snr,columns=columns).to_excel(writer, index=False, sheet_name='dif_snr')

	snr, dif_snr = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40],
	                              reconstruct_="remove_aperiodic", reconstruct_type=0, classify_method="tdca",freq_range=[3, 40])
	save_path = os.path.join(r"C:\Users\15956\Desktop\ssvep_result\cca", "tdca_pe.xlsx")
	with pd.ExcelWriter(save_path, mode='w') as writer:
		pd.DataFrame(snr,columns=columns).to_excel(writer, index=False, sheet_name='snr')
	with pd.ExcelWriter(save_path, mode='a', if_sheet_exists='replace') as writer:
		pd.DataFrame(dif_snr,columns=columns).to_excel(writer, index=False, sheet_name='dif_snr')

	snr, dif_snr = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40],
	                              reconstruct_="get_aperiodic", reconstruct_type=0, classify_method="tdca",freq_range=[3, 40])
	save_path = os.path.join(r"C:\Users\15956\Desktop\ssvep_result\cca", "tdca_ap.xlsx")
	with pd.ExcelWriter(save_path, mode='w') as writer:
		pd.DataFrame(snr,columns=columns).to_excel(writer, index=False, sheet_name='snr')
	with pd.ExcelWriter(save_path, mode='a', if_sheet_exists='replace') as writer:
		pd.DataFrame(dif_snr,columns=columns).to_excel(writer, index=False, sheet_name='dif_snr')





