# Distributed Inference with `pyhf` and `funcX`

Example code for vCHEP 2021 paper "Distributed statistical inference with pyhf enabled through funcX"

## Setup

Create a Python 3 virtual environment and then install the dependencies in `requirements.txt` and `jax-requirements.txt`.

```
(distributed-inference) $ python -m pip install --upgrade pip setuptools wheel
(distributed-inference) $ python -m pip install -r requirements.txt
(distributed-inference) $ python -m pip install -r jax-requirements.txt
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

Pass the config JSON file for the analysis you want to run to `fit_analysis.json`

```
(distributed-inference) $ python fit_analysis.py -c config/1Lbb.json
```
