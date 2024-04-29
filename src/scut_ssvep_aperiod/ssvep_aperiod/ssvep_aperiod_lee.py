from scut_ssvep_aperiod.load_dataset.dataset_kalunga import LoadDataKalungaOne
from scut_ssvep_aperiod.load_dataset.dataset_lee import LoadDataLeeOne
from scut_ssvep_aperiod.ssvep_method import CCACommon,TRCA,FBCCA,TDCA,PSDA
from scut_ssvep_aperiod.utils.common_function import cal_acc
import pandas as pd
import numpy as np
import os
def ssvep_classify(form_path, info_path, pro_ica=True, filter_para=None, reconstruct_=False, reconstruct_type=0,
                   classify_method="cca", psda_type="snr_hqy",freq_range=None):
	"""
	:param form_path:              str             path of form (subject_id---root_directory---file_name)
	:param info_path:              str             path of info (mat file for infromation to data)
	:param pro_ica:                bool            whether to do ica in propresess
	:param filter_para:            None/list       Default None  no filters
	                                               [low_freq, high_freq]

	:param reconstruct_:          None/str        Default None  no reconstruct
	                                              "remove_aperiodic" ---- reconstruct time signals and remove_aperiodic
	                                              "get_periodic" ---- reconstruct time signals and get_periodic
	                                              "get_aperiodic" ---- reconstruct time signals and get_aperiodic

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
	acc_all = np.zeros(len(unique_subject_ids))
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
			predict_label,error, r_squa = ssvep_method.classify(test_data)
		elif classify_method == "cca":
			ssvep_method = CCACommon(sfreq = datasetone.sample_rate_test, ws = datasetone.window_time,
			                                 fres_list = datasetone.freqs, n_harmonics = 3)
			predict_label = ssvep_method.classify(test_data, ica_ = False)
		elif classify_method == "fbcca":
			ssvep_method = FBCCA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs, 3)
			predict_label = ssvep_method.classify(test_data)
		elif classify_method == "trca":
			ssvep_method = TRCA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs, [3.4,40])
			ssvep_method.train(train_data, train_label)
			predict_label = ssvep_method.classifier(test_data)
		elif classify_method == "tdca":
			ssvep_method = TDCA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs,3,9,5)
			ssvep_method.train(train_data, train_label)
			predict_label = ssvep_method.classifier(test_data)
		del ssvep_method
		acc = cal_acc(Y_true = test_label, Y_pred = predict_label)
		print(predict_label,test_label)
		acc_all[subject_id-1] = acc
		print(acc)
	print("mean",acc_all.mean())
	return acc_all
if __name__ == "__main__":
	form_path_lee = "D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\ssvep_lee_sub_info.xlsx"
	info_path = r"D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\info_ssvep_lee_dataset.mat"
	data = {}
	acc = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40], reconstruct_=False, reconstruct_type=None, classify_method="psda", psda_type="snr_hqy",freq_range=None)
	data['psda_original'] = acc
	acc = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40], reconstruct_=False, reconstruct_type=None, classify_method="psda", psda_type="snr_hqy_ave_re",freq_range=None)
	data['psda_pe'] = acc
	acc = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40], reconstruct_=False, reconstruct_type=None, classify_method="psda", psda_type="snr_hqy_ave_get",freq_range=None)
	data['psda_ap'] = acc
	# #
	# acc = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40], reconstruct_=False, reconstruct_type=None, classify_method="cca",freq_range=None)
	# data['cca_original'] = acc
	# acc = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3,40], reconstruct_="remove_aperiodic", reconstruct_type=2, classify_method="cca",freq_range=[3,40])
	# data['cca_pe'] = acc
	# acc = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3,40], reconstruct_="get_aperiodic", reconstruct_type=0, classify_method="cca",freq_range=[3,40])
	# data['cca_ap'] = acc
	# #
	# # #
	acc = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40], reconstruct_=False,reconstruct_type=None, classify_method="fbcca",freq_range=None)
	data['fbcca_original'] = acc
	acc = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40], reconstruct_="remove_aperiodic", reconstruct_type=2, classify_method="fbcca",freq_range=[3, 40])
	data['fbcca_pe'] = acc
	acc = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40], reconstruct_="get_aperiodic", reconstruct_type=0, classify_method="fbcca",freq_range=[3, 40])
	data['fbcca_ap'] = acc

	# #
	# acc = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40], reconstruct_=False, reconstruct_type=None, classify_method="trca",freq_range=None)
	# data['trca_original'] = acc
	# acc = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40], reconstruct_="remove_aperiodic", reconstruct_type=2, classify_method="trca",freq_range=[3, 40])
	# data['trca_pe'] = acc
	# acc = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40], reconstruct_="get_aperiodic", reconstruct_type=0, classify_method="trca",freq_range=[3, 40])
	# data['trca_ap'] = acc


	# acc = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40], reconstruct_=False,reconstruct_type=None, classify_method="tdca",freq_range=None)
	# data['tdca_original'] = acc
	# acc = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40], reconstruct_="remove_aperiodic", reconstruct_type=2, classify_method="tdca",freq_range=[3, 40])
	# data['tdca_pe'] = acc
	# acc = ssvep_classify(form_path_lee, info_path, pro_ica=True, filter_para=[3, 40], reconstruct_="get_aperiodic", reconstruct_type=0, classify_method="tdca",freq_range=[3, 40])
	# data['tdca_ap'] = acc

	df = pd.DataFrame(data)
	print(data)
	df.to_excel('output.xlsx', index=False)


