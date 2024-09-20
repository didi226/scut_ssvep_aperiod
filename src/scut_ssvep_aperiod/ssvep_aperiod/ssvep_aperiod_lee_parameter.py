from scut_ssvep_aperiod.load_dataset.dataset_kalunga import LoadDataKalungaOne
from scut_ssvep_aperiod.load_dataset.dataset_lee import LoadDataLeeOne
from scut_ssvep_aperiod.ssvep_method import CCACommon,TRCA,FBCCA,TDCA,PSDA
from scut_ssvep_aperiod.utils.common_function import cal_acc
import pandas as pd
import numpy as np
import os
def cal_error_label_mean(test_label,error):
	average_errors =np.zeros((4))
	for i in range(4):
	    indices = np.where(test_label == i)
	    category_error = error[indices]
	    average_error = np.mean(category_error)
	    average_errors[i]=average_error
	return average_errors
def ssvep_classify_parameters(form_path, info_path, pro_ica=True, filter_para=None, reconstruct_=False, reconstruct_type=0,
                   classify_method="cca", psda_type="snr_hqy",freq_range=None):
	"""

	:param form_path:              str             path of form (subject_id---root_directory---file_name)
	:param info_path:              str             path of info (mat file for infromation to data)
	:param pro_ica:                bool            whether to do ica in propresess
	:param filter_para:            None/list       Default None  no filters
	                                               [low_freq, high_freq]
	:param reconstruct_type:    int               the type of reconstruction
	                                              0 ---- with original phase
                                                  2 ---- with 0 phase
    :param classify_method:     str               "psda"
                                                  "cca"
                                                  "fbcca"
                                                  "trca"
                                                  "tdca"
	:param psda_type:           str               "snr_hqy_ave_re"
	                                              "snr_hqy"
	                                              "snr_hqy_ave_get"

	:return:
	"""
	info_form = pd.read_excel(form_path)
	unique_subject_ids = info_form['subject_id'].unique()
	error_all = np.zeros((len(unique_subject_ids),4))
	r_squa_all = np.zeros((len(unique_subject_ids),4))
	error_all_1 = np.zeros((len(unique_subject_ids),4))
	r_squa_all_1 = np.zeros((len(unique_subject_ids),4))
	for subject_id in unique_subject_ids:
		subject_rows = info_form.loc[info_form['subject_id'] == subject_id]
		root_directory = subject_rows['root_directory'].tolist()
		file_name = subject_rows['file_name'].tolist()
		data_path = os.path.join(root_directory[0], file_name[0])
		datasetone = LoadDataLeeOne(data_path,info_path = info_path)
		test_data, test_label, train_data, train_label = datasetone.get_data(pro_ica = pro_ica, filter_para = filter_para,
                                                            resample = 4, reconstruct_ = reconstruct_,
                                                            reconstruct_type = reconstruct_type,freq_range=freq_range)
		test_data = test_data [:,:9,:]
		train_data = train_data [:,:9,:]
		if classify_method == "psda":
			ssvep_method = PSDA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs, 3, psd_type="Ordinary", # "remove_aperiodic"
			                    psd_channel = "ave", psda_type=psda_type,freq_range=[3,40]) #"snr_hqy_ave_re"
			_, error, r_squa = ssvep_method.classify(test_data)
			error_1,r_squa_1 = ssvep_method.slope_estimation(test_data)
		error_all[subject_id-1] = cal_error_label_mean(test_label, error)
		r_squa_all[subject_id-1] = cal_error_label_mean(test_label, r_squa)
		error_all_1[subject_id-1] = cal_error_label_mean(test_label, error_1)
		r_squa_all_1[subject_id-1] = cal_error_label_mean(test_label,r_squa_1)
	return error_all, r_squa_all, error_all_1, r_squa_all_1
if __name__ == "__main__":
	form_path_lee = "D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\ssvep_lee_sub_info.xlsx"
	info_path = r"D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\info_ssvep_lee_dataset.mat"
	data = {}
	error, r_squa, error_1, r_squa_1 = ssvep_classify_parameters(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40],
	                     reconstruct_=False, reconstruct_type=None, classify_method="psda",
	                                          psda_type="snr_hqy_ave_re",freq_range=None)
	column_names = [60.0/5.0, 60.0/7.0, 60.0/9.0, 60.0/11.0]

	# 将 error 数组转换为 pandas DataFrame
	df1 = pd.DataFrame(error, columns=column_names)
	df2 = pd.DataFrame(r_squa, columns=column_names)
	df3 = pd.DataFrame(error_1, columns=column_names)
	df4 = pd.DataFrame(r_squa_1, columns=column_names)

	# 指定保存的 Excel 文件名称
	excel_filename = 'error_r_squa_output.xlsx'

	# 使用 ExcelWriter 创建一个写入器对象
	with pd.ExcelWriter(excel_filename) as writer:
		# 将每个 DataFrame 写入不同的工作表
		df1.to_excel(writer, sheet_name='error', index=False)
		df2.to_excel(writer, sheet_name='r_squa', index=False)
		df3.to_excel(writer, sheet_name='error_1', index=False)
		df4.to_excel(writer, sheet_name='r_squa_1', index=False)



