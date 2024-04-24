from pyriemann.classification import MDM
from pyriemann.estimation import Covariances
from sklearn.pipeline import make_pipeline
from moabb.evaluations import WithinSessionEvaluation
from moabb.paradigms import LeftRightImagery
from moabb.datasets import Kalunga2016,MAMEM1,MAMEM2 ,Lee2019_SSVEP
from moabb.paradigms.ssvep import BaseSSVEP
import numpy as np
# dataset = Kalunga2016()
# dataset.get_data(subjects = np.arange(1,13).tolist())
# dataset = MAMEM1()
# dataset.get_data()
# # dataset.get_data(subjects = np.arange(1,11).tolist())
# # dataset = MAMEM2()
# # dataset.get_data(subjects = np.arange(1,11).tolist())
# # dataset = Lee2019_SSVEP(train_run = True, test_run = None, resting_state = False, sessions=(1,2))
# paradigm = BaseSSVEP()
# X, labels, meta = paradigm.get_data(dataset = dataset)
# evaluation = WithinSessionEvaluation(
#     paradigm = paradigm, datasets = dataset, overwrite = False, suffix = "newdataset")
# pipelines = {}
# pipelines["MDM"] = make_pipeline(Covariances("oas"), MDM(metric="riemann"))
# scores = evaluation.process(pipelines)
# print(scores)

import os
import shutil

# 设置原始文件夹和目标文件夹的路径
source_folder = r'D:\data\ssvep_dataset\Tsinghua_dataset_ssvep_wearable\ssvep_data'  # 将这个替换为您的原始文件夹路径
destination_folder = r'D:\data\ssvep_dataset\Tsinghua_dataset_ssvep_wearable\ssvep_data'  # 将这个替换为您的目标文件夹路径

# 获取源文件夹中所有.mat文件的列表
files = [f for f in os.listdir(source_folder) if f.endswith('.mat')]

# 遍历每个文件
for file in files:
	# 获取文件名的基准部分（不包括后缀）
	file_name = os.path.splitext(file)[0]

	# 创建目标文件夹路径
	target_folder = os.path.join(destination_folder, file_name)

	# 创建目标文件夹，如果不存在
	if not os.path.exists(target_folder):
		os.makedirs(target_folder)

	# 构建源文件的完整路径
	source_file_path = os.path.join(source_folder, file)

	# 构建目标文件的完整路径
	target_file_path = os.path.join(target_folder, file)

	# 将文件移动到目标文件夹
	shutil.move(source_file_path, target_file_path)

print('文件移动完成。')




