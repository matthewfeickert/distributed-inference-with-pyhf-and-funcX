# Distributed Inference with `pyhf` and `funcX`

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/matthewfeickert/distributed-inference-with-pyhf-and-funcX/main.svg)](https://results.pre-commit.ci/latest/github/matthewfeickert/distributed-inference-with-pyhf-and-funcX/main)

Example code for vCHEP 2021 paper "Distributed statistical inference with pyhf enabled through funcX"

## Setup

Create a Python 3 virtual environment and then install the `pyhf` and `funcX` dependencies in `requirements.txt`.

```
(distributed-inference) $ python -m pip install --upgrade pip setuptools wheel
(distributed-inference) $ python -m pip install -r requirements.txt
```

### Reproducible environment

To install a reproducible environment that is consistent down to the hash level, use `pip-compile` to compile a lock file from `requirements.txt` and install it following the `pip-secure-install` recommendations

```
(distributed-inference) $ bash compile_dependencies.sh
(distributed-inference) $ bash secure_install.sh
```

### On XSEDE's EXPANSE

On EXPANSE, to use a Python 3.7+ runtime Conda must be used, so create a Conda environment from the `expanse-environment.yml` provided, which uses the different `requirements.txt` files to provide the dependencies.

```console
$ conda env create -f expanse-environment.yml
$ conda activate distributed-inference
```

Once a GPU session has been entered, source the `setup_expanse_funcx_test_env.sh` shell script to activate the environment and load all required modules

```
(distributed-inference) $ . setup_expanse_funcx_test_env.sh
```

#### Machine Configuration

EXPANSE has the following Nvidia drivers and GPUs:

```console
$ nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2020 NVIDIA Corporation
Built on Thu_Jun_11_22:26:38_PDT_2020
Cuda compilation tools, release 11.0, V11.0.194
Build cuda_11.0_bu.TC445_37.28540450_0
$ nvidia-smi --list-gpus
GPU 0: Tesla V100-SXM2-32GB (UUID: GPU-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX)
```

## Run

Create a file named `endpoint_id.txt` in the top level of this repository and save your funcX endpoint ID into the file.

```
(distributed-inference) $ touch endpoint_id.txt
```

This will be read in during the run.

Pass the config JSON file for the analysis you want to run to `fit_analysis.py`

```
(distributed-inference) $ python fit_analysis.py -c config/1Lbb.json -b numpy
```

```console
$ python fit_analysis.py --help
usage: fit_analysis.py [-h] [-c CONFIG_FILE] [-b BACKEND]

configuration arguments provided at run time from the CLI

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        config file
  -b BACKEND, --backend BACKEND
                        pyhf backend str alias
```
