:orphan:

Installation
============

Dependencies
------------
* ``python`` (>=3.8)
* ``mne`` (>=1.6)
* ``numpy`` (>=1.21)
* ``scipy`` (>=1.4.0)
* ``mne_icalabel`` (>=0.7.0)
* ``fooof`` (>=1.1.0)
* ``statsmodels`` (>=0.14.3)


We require that you use Python 3.9 or higher.
You may choose to install ``scut_ssvep_aperiod`` `via pip <Installation via pip>`,
or conda.

Installation via Conda
----------------------

To install Scut Ssvep Aperiod using conda in a virtual environment,
simply run the following at the root of the repository:

.. code-block:: bash

   # with python>=3.9 at least
   conda create -n scut_ssvep
   conda activate scut_ssvep
   conda install -c conda-forge scut_ssvep_aperiod


Installation via Pip
--------------------

To install Sleep-Semantic-Segmentation including all dependencies required to use all features,
simply run the following at the root of the repository:

.. code-block:: bash

    python -m venv .venv
    pip install -U scut_ssvep_aperiod


To check if everything worked fine, the following command should not give any
error messages:

.. code-block:: bash

   python -c 'import scut_ssvep_aperiod'

scut-ssvep-aperiod works best with the latest stable release of SSA. To ensure
SSA is up-to-date, run:

.. code-block:: bash

   pip install --user -U scut_ssvep_aperiod
