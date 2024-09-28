from scut_ssvep_aperiod.load_dataset.dataset_Tsinghua_wearable import LoadDataTHWOne
from scut_ssvep_aperiod.ssvep_method import CCACommon,TRCA,FBCCA,TDCA,PSDA
from scut_ssvep_aperiod.utils.common_function import cal_acc
import pandas as pd
import numpy as np
import os
def ssvep_classify(form_path, pro_ica=True, filter_para=None, reconstruct_=False,
                   reconstruct_type=0, classify_method="cca", psda_type="snr_hqy",freq_range=None):
	"""
	Classify SSVEP data using different classification methods.

	Args:
		form_path (str): Path to the Excel file containing form data (subject_id, root_directory, file_name).
		pro_ica (bool, optional): Whether to perform ICA during preprocessing. Defaults to True.
		filter_para (list, optional): Filter parameters [low_freq, high_freq]. Defaults to None (no filtering).
		reconstruct_ (str, optional): Type of signal reconstruction. Defaults to None (no reconstruction).
									  Options:
										  "remove_aperiodic" - Reconstruct time signals and remove aperiodic components.
										  "get_periodic" - Reconstruct time signals and retain periodic components.
										  "get_aperiodic" - Reconstruct time signals and retain aperiodic components.
		reconstruct_type (int, optional): Type of reconstruction for the signal phase. Defaults to 0 (original phase).
										  Options:
											  0 - With original phase.
											  2 - With 0 phase.
		classify_method (str, optional): Classification method to use. Defaults to "cca".
										 Options:
											 "psda"
											 "cca"
											 "fbcca"
											 "trca"
											 "tdca"
		psda_type (str, optional): PSDA type, used when `classify_method` is "psda".
								   Options:
									   "snr_hqy"
									   "snr_hqy_ave_re"
									   "snr_hqy_ave_get". Defaults to "snr_hqy".
		freq_range (list, optional): Frequency range for filtering. Defaults to None.

	Returns:
		np.ndarray: Array of accuracy scores for each subject.
	"""
	info_form = pd.read_excel(form_path)
	unique_subject_ids = info_form['subject_id'].unique()
	acc_all = np.zeros(len(unique_subject_ids))
	for subject_id in unique_subject_ids:
		subject_rows = info_form.loc[info_form['subject_id'] == subject_id]
		root_directory = subject_rows['root_directory'].tolist()
		file_name = subject_rows['file_name'].tolist()
		data_path = os.path.join(root_directory[0], file_name[0])
		datasetone = LoadDataTHWOne(data_path)
		train_data, train_label,test_data, test_label  = datasetone.get_data(pro_ica = pro_ica, filter_para = filter_para,
                                                            resample = None, reconstruct_ = reconstruct_, reconstruct_type = reconstruct_type,freq_range=freq_range)
		if classify_method == "psda":
			ssvep_method = PSDA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs, 3,psd_type = "Ordinary",
			                    psd_channel = "ave", psda_type = psda_type,freq_range=[7,45])
			predict_label,_,_ = ssvep_method.classify(test_data)
		if classify_method == "cca":
			ccaoriginal_classify = CCACommon(sfreq = datasetone.sample_rate_test, ws = datasetone.window_time,
			                                 fres_list = datasetone.freqs, n_harmonics = 3)
			predict_label = ccaoriginal_classify.classify(test_data, ica_ = False)
		if classify_method == "fbcca":
			ssvep_method = FBCCA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs,
			                     3,8,1,[7.5,9,11,14, 18,20,24, 30, 32,38,40,43],
			                     [4,7,9, 10,14,16,20,24, 28,32,34,37],45,50)
			predict_label = ssvep_method.classify(test_data)
		if classify_method == "trca":
			ssvep_method = TRCA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs)
			ssvep_method.train(train_data, train_label)
			predict_label = ssvep_method.classifier(test_data)
		if classify_method == "tdca":
			ssvep_method = TDCA(datasetone.sample_rate_test, 1.98,
			                    datasetone.freqs,3,8,1, [8.5,9,11, 14, 18,20,24, 30, 32,38,40,43],
			                    [4,7,9, 10,14, 16,20, 24, 28,32,34,37],44,48,5)
			ssvep_method.train(train_data, train_label)
			predict_label = ssvep_method.classifier(test_data)
		acc = cal_acc(Y_true = test_label, Y_pred = predict_label)
		print(test_label, predict_label)
		print(acc)
		print(subject_id)
		acc_all[subject_id-1] = acc
	print(acc_all.mean())
	return acc_all
if __name__ == "__main__":
	form_path_lee = "D:\data\ssvep_dataset\Tsinghua_dataset_ssvep_wearable\ssvep_lee_sub_info.xlsx"
	data = {}
	acc = ssvep_classify(form_path_lee, pro_ica=True, filter_para=[7, 45], reconstruct_=False,
	                     reconstruct_type=None, classify_method="psda", psda_type="snr_hqy",freq_range=None)
	data['psda_original'] = acc
	acc = ssvep_classify(form_path_lee, pro_ica=True, filter_para=[7, 45], reconstruct_=False,
	                     reconstruct_type=None, classify_method="psda", psda_type="snr_hqy_ave_get",freq_range=None)
	data['psda_ap'] = acc
	acc = ssvep_classify(form_path_lee, pro_ica=True, filter_para=[7, 45], reconstruct_=False,
	                     reconstruct_type=None, classify_method="psda", psda_type="snr_hqy_ave_re",freq_range=None)
	data['psda_pe'] = acc
	#
	#
	acc = ssvep_classify(form_path_lee, pro_ica=True, filter_para=[7, 45],
	                     reconstruct_=False, reconstruct_type=None, classify_method="cca",freq_range=None)
	data['cca_original'] = acc
	acc = ssvep_classify(form_path_lee,  pro_ica=True, filter_para=[7, 45],
	                     reconstruct_="get_aperiodic", reconstruct_type=0, classify_method="cca",freq_range=[7,45])
	data['cca_ap'] = acc
	acc = ssvep_classify(form_path_lee,  pro_ica=True, filter_para=[7, 45],
	                     reconstruct_="remove_aperiodic", reconstruct_type=2, classify_method="cca",freq_range=[7,45])
	data['cca_pe'] = acc
	#
	acc = ssvep_classify(form_path_lee,  pro_ica=True, filter_para=[7, 45],
	                     reconstruct_=False,reconstruct_type=None, classify_method="fbcca",freq_range=None)
	data['fbcca_original'] = acc
	acc = ssvep_classify(form_path_lee,  pro_ica=True, filter_para=[7, 45],
	                     reconstruct_="get_aperiodic", reconstruct_type=0, classify_method="fbcca",freq_range=[7,45])
	data['fbcca_ap'] = acc
	acc = ssvep_classify(form_path_lee,  pro_ica=True, filter_para=[7, 45],
	                     reconstruct_="remove_aperiodic", reconstruct_type=2, classify_method="fbcca",freq_range=[7,45])
	data['fbcca_pe'] = acc
	#
	# acc = ssvep_classify(form_path_lee,  pro_ica=True, filter_para=[7, 45], reconstruct_=False, reconstruct_type=None, classify_method="trca")
	# data['trca_original'] = acc
	# acc = ssvep_classify(form_path_lee,  pro_ica=True, filter_para=[7, 45], reconstruct_="get_aperiodic", reconstruct_type=0, classify_method="trca")
	# data['trca_ap'] = acc
	# acc = ssvep_classify(form_path_lee, pro_ica=True, filter_para=[7, 45], reconstruct_="remove_aperiodic", reconstruct_type=0, classify_method="trca")
	# data['trca_pe'] = acc

	acc = ssvep_classify(form_path_lee,  pro_ica=True, filter_para=[7, 45],
	                     reconstruct_=False,reconstruct_type=None, classify_method="tdca",freq_range=None)
	data['tdca_original'] = acc
	acc = ssvep_classify(form_path_lee,  pro_ica=True, filter_para=[7, 45],
	                     reconstruct_="get_aperiodic", reconstruct_type=0, classify_method="tdca",freq_range=[7,45])
	data['tdca_ap'] = acc
	acc = ssvep_classify(form_path_lee, pro_ica=True, filter_para=[7, 45],
	                     reconstruct_="remove_aperiodic", reconstruct_type=2, classify_method="tdca",freq_range=[7,45])
	data['tdca_pe'] = acc
	df = pd.DataFrame(data)
	df.to_excel('output_Tstinghua.xlsx', index=False)
