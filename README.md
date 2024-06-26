# scut_ssvep_aperiod

- Four traditional SSVEP detection methods: Power Spectral Density Analysis (PSDA), Canonical Correlation Analysis (CCA), Filter Bank Canonical Correlation Analysis (FBCCA), and Task-Related Component Analysis (TDCA).
- A method for extracting periodic and aperiodic components from time-domain signals.
- Quantification of the influence of periodic and aperiodic components on SSVEP.



## Installation

You can either git clone this whole repo by:

```
git clone https://github.com/didi226/scut_ssvep_aperiod.git
cd scut_ssvep_aperiod/dist
pip install scut_ssvep_aperiod-0.0.1-py3-none-any.whl
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

The related article has not yet been published.