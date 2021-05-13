# `funcX` Endpoint Setup

## Endpoint creation
To create a `funcX` endpoint in an virtual environment with the `funcx-endpoint` library installed (such as provided by `requirements.txt`) run

```console
$ funcx-endpoint configure pyhf
```

which will create a `funcX` configuration file at `~/.funcx/pyhf/config.py`.

## Endpoint configuration

The endpoint configuration can now be revised for the purposes of the studies needed.
The configuration file used for this analysis is the included `pyhf-config.py`.

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
