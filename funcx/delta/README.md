_# `funcX` Endpoint Setup

## Installing funcX
On sites that support Python 3.8 and conda you should be able to simply create
a conda environment from `requrements.txt` or `requrements.lock`.


Delta requires setup for running distributed inference on Singularity container.

#### Apptainer
We are using an Apptainer to manage dependencies on Delta.
[distributed-inference.def](funcx/delta/distributed_inference.def) builds the container.

```console
apptainer build /projects/bbmi/bengal1/distributed_inference.sif funcx/delta/distributed_inference.def
```
This builds the container and puts in our projects directory.

#### Fetch the Container Id

```console
python funcx/delta/funcx_register_image.py
```
This creates a funcx.json file with container_id and placeholder for endpoint_id, which should be added manually after endpoint configuration.

## Endpoint creation
With funcX endpoint software installed, you need to create a template
environment for your endpoint.

```console
$ funcx-endpoint configure pyhf
```

which will create a `funcX` configuration file at `~/.funcx/pyhf/config.py`.


```console
$ funcx-endpoint start pyhf
```
