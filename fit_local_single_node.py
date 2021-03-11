import argparse
import json
import time
from pathlib import Path
from time import sleep

import pyhf
from pyhf.contrib.utils import download


def infer_hypotest(workspace, patches):
    fit_results = {}
    for patch_idx in range(len(patches)):
    # for patch_idx in range(2):
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
                # Use v0.5.4 API until endpoint fixed
                # pyhf.infer.hypotest(test_poi, data, model, qtilde=True)
            ),
            "Fit-Time": time.time() - tick,
        }
    return fit_results


def main(args):
    if args.config_file is not None:
        with open(args.config_file, "r") as infile:
            config = json.load(infile)

    # TODO: Make backend configurable from argparse CLI
    backend = "jax"
    if backend is None:
        backend = "numpy"
    pyhf.set_backend(backend)
    print(f"pyhf backend: {pyhf.get_backend()[0].name}")

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

    # Read patchset in while background only workspace running
    with open(
        pallet_path.joinpath(f"{analysis_prefix_str}patchset.json")
    ) as patchset_json:
        patchset = pyhf.PatchSet(json.load(patchset_json))

    workspace = pyhf.Workspace(bkgonly_workspace)

    print("--------------------")
    print(workspace)

    fit_results = infer_hypotest(workspace, patchset.patches)
    print(f"\nfit results:\n\n{fit_results.values()}")


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
