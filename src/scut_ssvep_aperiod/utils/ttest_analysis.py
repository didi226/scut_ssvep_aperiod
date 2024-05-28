import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
import os
import numpy as np
def help_tttest(file_name,file_name_last_list,data_type):
    t_stats = np.zeros((4))
    p_values = np.zeros((4))
    for i, i_class in enumerate([5.45,6.67,8.57,12]):
        t_stats[i], p_values[i] = stats.ttest_rel(data[file_name + file_name_last_list[0] + data_type + str(i_class)],
                                          data[file_name + file_name_last_list[1] + data_type + str(i_class)], alternative='greater')
    print(t_stats,p_values)
    return t_stats,p_values
file_root = r"C:\Users\15956\Desktop\ssvep_result\cca"
# file_name = 'psda_'
data = {}
for file_name in ['psda_','cca_','fbcca_','tdca_']:
    file_name_last = ['original', 'pe', 'ap']
    for i_file_last in file_name_last:
        file_path = os.path.join(file_root, file_name + i_file_last + '.xlsx')
        for data_type in ['snr','dif_snr']:
            for i_class in [5.45,6.67,8.57,12]:
                data[file_name+i_file_last + data_type + str(i_class)] = pd.read_excel(file_path, sheet_name = data_type)[i_class]
file_name = 'tdca_'
p_values_all=[]
t_stats,p_values = help_tttest(file_name=file_name,file_name_last_list=['original', 'pe'],data_type='snr')
p_values_all.extend(p_values.tolist())
t_stats,p_values = help_tttest(file_name=file_name,file_name_last_list=['original', 'ap'],data_type='snr')
p_values_all.extend(p_values.tolist())
t_stats,p_values = help_tttest(file_name=file_name,file_name_last_list=['original' ,'pe'],data_type='dif_snr')
p_values_all.extend(p_values.tolist())
reject, corrected_p_values, _, _ = multipletests(p_values_all, alpha = 0.05, method = 'fdr_bh')
print(corrected_p_values)








# file_path = "D:\data\ssvep_dataset\MNE-lee2019-ssvep-data\output_end_0501.xlsx"
# data = pd.read_excel(file_path, sheet_name=0)
# print(data.columns)
#
# psda_original = data['psda_original']
# cca_original  = data['cca_original']
# fbcca_original  = data['fbcca_original']
# tdca_original  = data['tdca_original']
# cca_pe =data['cca_pe']
# psda_pe = data['psda_pe']
# fbcca_pe =data['fbcca_pe']
# tdca_pe =data['tdca_pe']
# cca_ap =data['cca_ap']
# psda_ap = data['psda_ap']
# fbcca_ap =data['fbcca_ap']
# tdca_ap =data['tdca_ap']
#
# print('psda_original', psda_original.mean(),psda_original.std())
# print('cca_original', cca_original.mean(),cca_original.std())
# print('fbcca_original', fbcca_original.mean(),fbcca_original.std())
# print('tdca_original',tdca_original.mean(),tdca_original.std())
# print('cca_pe',cca_pe.mean(),cca_pe.std())
# print('psda_pe',psda_pe.mean(),psda_pe.std())
# print('fbcca_pe',fbcca_pe.mean(),fbcca_pe.std())
# print('tdca_pe',tdca_pe.mean(),tdca_pe.std())
# print('cca_ap',cca_ap.mean(),cca_ap.std())
# print('psda_ap',psda_ap.mean(),psda_ap.std())
# print('fbcca_ap',fbcca_ap.mean(),fbcca_ap.std())
# print('tdca_ap',tdca_ap.mean(),tdca_ap.std())
#
# t_stat, p_value = stats.ttest_ind(cca_original, psda_original, alternative='greater')
# print(t_stat,p_value)
# t_stat, p_value = stats.ttest_ind(fbcca_original, psda_original, alternative='greater')
# print(t_stat,p_value)
# t_stat, p_value = stats.ttest_ind(tdca_original, psda_original, alternative='greater')
# print(t_stat,p_value)
# t_stat, p_value = stats.ttest_ind(cca_original, cca_pe, alternative='greater')
# print(t_stat,p_value)
# t_stat, p_value = stats.ttest_ind(psda_original, psda_pe, alternative='greater')
# print(t_stat,p_value)
# t_stat, p_value = stats.ttest_ind(fbcca_original, fbcca_pe, alternative='greater')
# print(t_stat,p_value)
# t_stat, p_value = stats.ttest_ind(tdca_original, tdca_pe, alternative='greater')
# print(t_stat,p_value)
# t_stat, p_value = stats.ttest_ind(cca_ap, psda_ap, alternative='greater')
# print(t_stat,p_value)
# t_stat, p_value = stats.ttest_ind(fbcca_ap, psda_ap, alternative='greater')
# print(t_stat,p_value)
# t_stat, p_value = stats.ttest_ind(tdca_ap, psda_ap, alternative='greater')
# print(t_stat,p_value)
# p_values=[ 2.570084995700295e-06,7.776926452315703e-06,3.776754055310389e-08,2.299318219825501e-05,0.3057493921829397,
#            0.010525723544767255,2.0293716236172113e-16,6.293951408102441e-22,1.376759367655962e-17,5.974768212434907e-39]
# reject, corrected_p_values, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')
# print(corrected_p_values)