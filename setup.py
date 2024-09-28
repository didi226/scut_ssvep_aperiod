import setuptools
from setuptools import find_packages

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="scut_ssvep_aperiod",
    version="0.0.1",
    author="didi",
    author_email="3517725675@qq.com",
    description="aperiod extract and ssvep measure",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('src'),
    package_dir={"": "src"},
    install_requires=['numpy',
                      'fooof',
                      'mne',
                      'mne_icalabel',
                      'scikit-learn',
                      'scipy',
                      'statsmodels'],
)
