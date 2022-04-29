# `funcX` Endpoint Setup

## Installing funcX
On sites that support Python 3.8 and conda you should be able to simply create
a conda environment from `requrements.txt` or `requrements.lock`.

### Special Handling for BlueWaters
We ran into several issues getting the endpoint to run correctly on BlueWaters
given the lack of a Python 3.8 module.

We wound up manually installing conda on the login node. The site's admins
state that conda is not supported on BW and not recommended, however we are only
using conda on the login node to host the endpoint, so this doesn't seem against
the spirit of their advice.

We installed conda with
```console
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ bash ./Miniconda3-latest-Linux-x86_64.sh
```

Once installed, we needed to install pip
```console
$ conda install pip
```

FuncX-endpoint relies on two libraries that require careful handling.

Cryptography library can't be installed with pip, but needs additional resources
that are more easily provided by the conda installation process:

```console
$ conda install -c anaconda cryptography
```

The pyzmq library version 22.0 is very picky about the GCC environment.

```console
$ module load gcc/7.3.0
$ python -m pip install --no-binary :all: --force-reinstall pyzmq
```

With these preliminaries out of the way you can pip install the funcx-endpoint

```console
$ pip install funcx-endpoint
```

## Endpoint creation
With funcX endpoint software installed, you need to create a template
environment for your endpoint.

```console
$ funcx-endpoint configure pyhf
```

which will create a `funcX` configuration file at `~/.funcx/pyhf/config.py`.

## Endpoint configuration

The endpoint configuration can now be revised for the purposes of the studies
needed. The configuration files used for this analysis are included in the
`/funcx` directory

### Customising the installation
There are several parameters in the config file that can control scaling
behaviour for the endpoint:

|Property|Description|
|--------|-----------|
| queue   | The job queue where the workers will be launched |
| init_blocks | Number of initial jobs to start |
| max_blocks | Maximum number of jobs to start as scaling proceeds |
| nodes_per_block | Number of nodes to request for each job |
| parallelism | Parallelism is expressed as the ratio of task execution capacity to the sum of running tasks and available tasks. A parallelism value of 1 represents aggressive scaling where the maximum resources needed are used; parallelism close to 0 represents the opposite situation in which as few resources as possible are used. By selecting a fraction between 0 and 1, the provisioning aggressiveness can be controlled. |

## Endpoint start

To start the endpoint ensure that the working environment is setup to include all modules that might be needed

```console
$ . setup_expanse_funcx_test_env.sh
```

and then execute

```console
$ funcx-endpoint start pyhf
```

The endpoint ID that is generated is the value that will go in your `endpoint_id.txt` file.
