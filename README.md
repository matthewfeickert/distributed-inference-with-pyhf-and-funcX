# Distributed Inference with `pyhf` and `funcX`

Example code for vCHEP 2021 paper "Distributed statistical inference with pyhf enabled through funcX"

## Setup

Create a Python 3 virtual environment and then install the dependencies in `requirements.txt` and `jax-requirements.txt`.

```shell
(distributed-inference) $ python -m pip install --upgrade pip setuptools wheel
(distributed-inference) $ python -m pip install -r requirements.txt
(distributed-inference) $ python -m pip install -r jax-requirements.txt
```

### On XSEDE's EXPANSE

On EXPANSE, to use a Python 3.7+ runtime Conda must be used, so crete a Conda environment from the `expanse-environment.yml` provided, which uses the different `requirements.txt` files to provide the dependencies.

```
$ conda env create -f expanse-environment.yml
$ conda activate distributed-inference
(distributed-inference) $
```

## Run

Create a file named `endpoint_id.txt` in the top level of this repository and save your funcX endpoint ID into the file.

```shell
(distributed-inference) $ touch endpoint_id.txt
```

This will be read in during the run.

Pass the config JSON file for the analysis you want to run to `fit_analysis.json`

```shell
(distributed-inference) $ python fit_analysis.py -c config/1Lbb.json
```
