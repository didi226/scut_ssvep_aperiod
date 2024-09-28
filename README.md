# scut_ssvep_aperiod

## Description

- Four traditional SSVEP detection methods: Power Spectral Density Analysis (PSDA), Canonical Correlation Analysis (CCA), Filter Bank Canonical Correlation Analysis (FBCCA), and Task-Related Component Analysis (TDCA).

- A method for extracting periodic and aperiodic components from time-domain signals.

- Quantification of the influence of periodic and aperiodic components on SSVEP.

  You can get more information about this package from [Document ](https://scut-ssvep-aperiod.readthedocs.io/en/latest/).

## Installation

```
pip install scut_ssvep_aperiod
```

## Usage

Simple demo for SSVEP detection methods.

```python
from scut_ssvep_aperiod.ssvep_method import CCACommon,TRCA,FBCCA,TDCA,PSDA
ssvep_method = PSDA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs, 3) 
predict_label,_,_ = ssvep_method.classify(test_data)

ssvep_method = CCACommon(sfreq = datasetone.sample_rate_test, ws = datasetone.window_time,fres_list = datasetone.freqs, n_harmonics = 3)
predict_label = ssvep_method.classify(test_data)

ssvep_method = FBCCA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs, 3)
predict_label = ssvep_method.classify(test_data)

ssvep_method = TRCA(datasetone.sample_rate_test, datasetone.window_time, datasetone.freqs)
ssvep_method.train(train_data, train_label)
predict_label = ssvep_method.classifier(test_data)

ssvep_method = TDCA(datasetone.sample_rate_test ,4,datasetone.freqs)
ssvep_method.train(train_data, train_label)
predict_label = ssvep_method.classifier(test_data)
```

## Cite 

```
@article{chen2024aperiodic,
  title={Aperiodic Component Analysis in Quantification of Steady-State Visually Evoked Potentials},
  author={Chen, Di and Song, Zhiqing and Du, Yang and Chen, Sicong and Zhang, Xin and Li, Yuanqing and Huang, Qiyun},
  journal={IEEE Transactions on Biomedical Engineering},
  year={2024},
  publisher={IEEE}
}
```