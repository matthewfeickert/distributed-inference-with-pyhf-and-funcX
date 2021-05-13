import argparse
import json
from pathlib import Path
from time import sleep

import pyhf
from funcx.sdk.client import FuncXClient
from pyhf.contrib.utils import download


def prepare_workspace(data):
    import pyhf

    return pyhf.Workspace(data)


def infer_hypotest(workspace, patches):
    import time

    import pyhf

    fit_results = {}
    # for patch_idx in range(len(patches)):
    for patch_idx in range(2):
        patch = patches[patch_idx]

        tick = time.time()
        model = workspace.model(
            patches=[patch.patch],
            modifier_settings={
                "normsys": {"interpcode": "code4"},
                "histosys": {"interpcode": "code4p"},
            },
        )
        data = workspace.data(model)
        test_poi = 1.0

        fit_results[patch.name] = {
            "metadata": patch.metadata,
            "CLs_obs": float(
                pyhf.infer.hypotest(test_poi, data, model, test_stat="qtilde")
            ),
            "Fit-Time": time.time() - tick,
        }
    return fit_results


def main(args):
    if args.config_file is not None:
        with open(args.config_file, "r") as infile:
            config = json.load(infile)

    pallet_path = Path(config["input_prefix"]).joinpath(config["pallet_name"])

    # locally get pyhf pallet for analysis
    if not pallet_path.exists():
        download(config["pallet_url"], pallet_path)

    analysis_name = config["analysis_name"]
    analysis_prefix_str = "" if analysis_name is None else f"{analysis_name}_"
    if config["analysis_dir"] is not None:
        pallet_path = pallet_path.joinpath(config["analysis_dir"])

    with open(
        pallet_path.joinpath(f"{analysis_prefix_str}BkgOnly.json")
    ) as bkgonly_json:
        bkgonly_workspace = json.load(bkgonly_json)

    # Initialize funcX client
    fxc = FuncXClient()
    fxc.max_requests = 200

    with open("endpoint_id.txt") as endpoint_file:
        pyhf_endpoint = str(endpoint_file.read().rstrip())

    # register functions
    prepare_func = fxc.register_function(prepare_workspace)
    infer_func = fxc.register_function(infer_hypotest)

    # execute background only workspace
    prepare_task = fxc.run(
        bkgonly_workspace, endpoint_id=pyhf_endpoint, function_id=prepare_func
    )

    # Read patchset in while background only workspace running
    with open(
        pallet_path.joinpath(f"{analysis_prefix_str}patchset.json")
    ) as patchset_json:
        patchset = pyhf.PatchSet(json.load(patchset_json))

    workspace = None
    while not workspace:
        try:
            workspace = fxc.get_result(prepare_task)
        except Exception as excep:
            print(f"prepare: {excep}")
            sleep(10)

    print("--------------------")
    print(workspace)

    # Fit all patches of the analysis on a single node
    # This is done only for comparison with the performance of funcX
    # across multiple workers
    infer_task = fxc.run(
        workspace, patchset.patches, endpoint_id=pyhf_endpoint, function_id=infer_func
    )

    fit_results = None
    while not fit_results:
        try:
            fit_results = fxc.get_result(infer_task)
        except Exception as excep:
            print(f"inference: {excep}")
            sleep(15)

    print("--------------------")
    print(fit_results.values())


if __name__ == "__main__":
    cli_parser = argparse.ArgumentParser(
        description="configuration arguments provided at run time from the CLI"
    )
    cli_parser.add_argument(
        "-c",
        "--config-file",
        dest="config_file",
        type=str,
        default=None,
        help="config file",
    )
    args, unknown = cli_parser.parse_known_args()

    parser = argparse.ArgumentParser(parents=[cli_parser], add_help=False)
    args = parser.parse_args()

    main(args)
