import argparse
import json
from pathlib import Path
from time import sleep

import pyhf
from funcx.sdk.client import FuncXClient
from pyhf.contrib.utils import download


def prepare_workspace(data, backend):
    import pyhf

    pyhf.set_backend(backend)

    return pyhf.Workspace(data)


def infer_hypotest(workspace, metadata, patches, backend):
    import time

    import pyhf

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
    return {
        "metadata": metadata,
        "CLs_obs": float(
            pyhf.infer.hypotest(test_poi, data, model, test_stat="qtilde")
        ),
        "Fit-Time": time.time() - tick,
    }


def count_complete(l):
    return len(list(filter(lambda e: e["result"], l)))


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
    fxc = FuncXClient()
    fxc.max_requests = 200
    # Need to force funcX to allow posting of all patches
    fxc.throttling_enabled = False

    with open("endpoint_id.txt") as endpoint_file:
        pyhf_endpoint = str(endpoint_file.read().rstrip())

    # register functions
    prepare_func = fxc.register_function(prepare_workspace)
    infer_func = fxc.register_function(infer_hypotest)

    # execute background only workspace
    prepare_task = fxc.run(
        bkgonly_workspace, backend, endpoint_id=pyhf_endpoint, function_id=prepare_func
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

    # execute patch fits across workers and retrieve them when done
    n_patches = len(patchset.patches)

    batch = fxc.create_batch()

    for patch_idx in range(n_patches):
        patch = patchset.patches[patch_idx]
        batch.add(
            workspace,
            patch.metadata,
            [patch.patch],
            backend,
            endpoint_id=pyhf_endpoint,
            function_id=infer_func,
        )

    # Submit batch job to run
    batch_task_id_list = fxc.batch_run(batch)

    # While loop info
    batch_job_finished = False
    sleep_time = 15
    completed_task_ids = []

    while not batch_job_finished:
        batch_job_finished = True
        sleep(sleep_time)
        if sleep_time > 5:
            sleep_time -= 5

        batch_status = fxc.get_batch_status(batch_task_id_list)

        for task_id in batch_status.keys():
            task = batch_status[task_id]
            # If any task is still running do another loop
            if task["pending"]:
                batch_job_finished = False
            elif task["status"] == "success":
                if task_id not in completed_task_ids:
                    completed_task_ids.append(task_id)
                    print(
                        f"Task {task['result']['metadata']['name']} complete: {len(completed_task_ids)}/{n_patches}"
                    )

        # Status update to user per loop
        running_task_ids = [
            id for id in batch_status.keys() if id not in completed_task_ids
        ]
        if running_task_ids:
            arbitrary_id = running_task_ids[0]
            running_task_status = batch_status[arbitrary_id]["status"]
            if running_task_status != "success":
                print(f"Inference: {running_task_status}")

    # Return useful information to user
    output = fxc.get_batch_status(batch_task_id_list)
    fit_results = {}
    for task_id in output.keys():
        result = output[task_id]["result"]
        name = result["metadata"]["name"]
        fit_results[name] = result

    print(f"\n\nfit results: {fit_results}")


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
    args, unknown = cli_parser.parse_known_args()

    parser = argparse.ArgumentParser(parents=[cli_parser], add_help=False)
    args = parser.parse_args()

    main(args)
