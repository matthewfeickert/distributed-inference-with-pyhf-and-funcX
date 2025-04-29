import argparse
import json
from concurrent.futures import as_completed
from pathlib import Path
import pyhf
from pyhf.contrib.utils import download

from funcx import FuncXExecutor


def prepare_workspace(data, backend):
    import pyhf

    pyhf.set_backend(backend)
    return pyhf.Workspace(data)


def infer_hypotest(workspace, metadata, patches, backend):
    import time
    import pyhf
    import numpy as np

    pyhf.set_backend(backend)
    tick = time.time()
    model = workspace.model(
        patches=patches,
        modifier_settings={
            "normsys": {"interpcode": "code4"},
            "histosys": {"interpcode": "code4p"},
        },
    )
    data = workspace.data(model)
    test_poi = 1.0
    CLs_obs, CLs_exp_band = pyhf.infer.hypotest(
        test_poi, data, model, return_expected_set=True, test_stat="qtilde"
    )
    fit_time = time.time() - tick
    return {
        "metadata": metadata,
        "CLs_obs": float(CLs_obs),
        "CLs_exp": [float(cls_exp) for cls_exp in CLs_exp_band],
        "fit_time": fit_time,
    }


def main(args):
    if args.config_file is not None:
        with open(args.config_file, "r") as infile:
            config = json.load(infile)
    backend = args.backend

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

    with open("funcx/delta/funcx.json", "r") as funcx_file:
        funcx_object = json.load(funcx_file)

    with open(
        pallet_path.joinpath(f"{analysis_prefix_str}patchset.json")
    ) as patchset_json:
        patchset = pyhf.PatchSet(json.load(patchset_json))

    print("The endpoint is", funcx_object.get("endpoint_id"))
    fxe = FuncXExecutor(
        endpoint_id=funcx_object.get("endpoint_id"),
        container_id=funcx_object.get("container_id", None),
        batch_size=64,
    )
    future = fxe.submit(prepare_workspace, bkgonly_workspace, backend)
    workspace = future.result()

    # Read patchset in while background only workspace running
    message = "# Background Workspace Constructed"
    print(message)

    # execute patch fits across workers and retrieve them when done
    n_patches = len(patchset.patches)
    futures = []
    for patch_idx in range(n_patches):
        patch = patchset.patches[patch_idx]
        futures.append(
            fxe.submit(
                infer_hypotest,
                workspace,
                patch.metadata,
                [patch.patch],
                backend,
            )
        )

    results = {}

    for task in as_completed(futures):
        task_result = task.result()
        results[task_result["metadata"]["name"]] = {
            "mass_hypotheses": task_result["metadata"]["values"],
            "CLs_obs": task_result["CLs_obs"],
            "CLs_exp": task_result["CLs_exp"],
            "fit_time": task_result["fit_time"],
        }
        print(
            f'{task_result["metadata"]["name"]}: {results[task_result["metadata"]["name"]]}'
        )

    with open("results.json", "w") as results_file:
        results_file.write(json.dumps(results, sort_keys=True, indent=2))


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
    cli_parser.add_argument(
        "-b",
        "--backend",
        dest="backend",
        type=str,
        default="numpy",
        help="pyhf backend str alias",
    )

    parser = argparse.ArgumentParser(parents=[cli_parser], add_help=False)
    args = parser.parse_args()

    main(args)
