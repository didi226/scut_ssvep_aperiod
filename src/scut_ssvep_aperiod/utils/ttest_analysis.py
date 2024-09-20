import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
import os
import numpy as np
# def help_tttest(file_name,file_name_last_list,data_type):
#     t_stats = np.zeros((4))
#     p_values = np.zeros((4))
#     for i, i_class in enumerate([5.45,6.67,8.57,12]):
#         t_stats[i], p_values[i] = stats.ttest_rel(data[file_name + file_name_last_list[0] + data_type + str(i_class)],
#                                           data[file_name + file_name_last_list[1] + data_type + str(i_class)], alternative='greater')
#     print(t_stats,p_values)
#     return t_stats,p_values
# file_root = r"C:\Users\15956\Desktop\ssvep_result\cca"
# # file_name = 'psda_'
# data = {}
# for file_name in ['psda_','cca_','fbcca_','tdca_']:
#     file_name_last = ['original', 'pe', 'ap']
#     for i_file_last in file_name_last:
#         file_path = os.path.join(file_root, file_name + i_file_last + '.xlsx')
#         for data_type in ['snr','dif_snr']:
#             for i_class in [5.45,6.67,8.57,12]:
#                 data[file_name+i_file_last + data_type + str(i_class)] = pd.read_excel(file_path, sheet_name = data_type)[i_class]
# file_name = 'fbcca_'
# p_values_all=[]
# t_stats,p_values = help_tttest(file_name=file_name,file_name_last_list=['original', 'pe'],data_type='snr')
# p_values_all.extend(p_values.tolist())
# t_stats,p_values = help_tttest(file_name=file_name,file_name_last_list=['original', 'ap'],data_type='snr')
# p_values_all.extend(p_values.tolist())
# t_stats,p_values = help_tttest(file_name=file_name,file_name_last_list=['original' ,'pe'],data_type='dif_snr')
# p_values_all.extend(p_values.tolist())
# reject, corrected_p_values, _, _ = multipletests(p_values_all, alpha = 0.05, method = 'fdr_bh')
# print(corrected_p_values)

file_root = r"C:\Users\15956\Desktop\ssvep_result\cca\output_Tstinghua.xlsx"
acc = pd.read_excel(file_root)
t,p = stats.ttest_rel(acc['cca_original'],acc['psda_original'],alternative='greater')
print(t,p)
t,p =stats.ttest_rel(acc['fbcca_original'],acc['psda_original'],alternative='greater')
print(t,p)
t,p =stats.ttest_rel(acc['tdca_original'],acc['psda_original'],alternative='greater')
print(t,p)
t,p = stats.ttest_rel(acc['cca_original'],acc['cca_pe'],alternative='greater')
print(t,p)
t,p =stats.ttest_rel(acc['fbcca_original'],acc['fbcca_pe'],alternative='greater')
print(t,p)
t,p =stats.ttest_rel(acc['tdca_original'],acc['tdca_pe'],alternative='greater')
print(t,p)
t,p =stats.ttest_rel(acc['psda_original'],acc['psda_pe'],alternative='greater')
print(t,p)

t,p = stats.ttest_rel(acc['cca_ap'],acc['psda_ap'],alternative='greater')
print(t,p)
t,p =stats.ttest_rel(acc['fbcca_ap'],acc['psda_ap'],alternative='greater')
print(t,p)
t,p =stats.ttest_rel(acc['tdca_ap'],acc['psda_ap'],alternative='greater')
print(t,p)






