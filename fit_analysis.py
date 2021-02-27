import json
import sys
from pathlib import Path
from time import sleep

import requests
from funcx.sdk.client import FuncXClient
import pyhf
from pyhf.contrib.utils import download


def prepare_workspace(data):
    import pyhf

    return pyhf.Workspace(data)


def infer_hypotest(workspace, metadata, doc):
    import time

    import pyhf

    tick = time.time()
    model = workspace.model(
        patches=[doc],
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
            # pyhf.infer.hypotest(test_poi, data, model, test_stat="qtilde")
            # Use v0.5.4 API until endpoint fixed
            pyhf.infer.hypotest(test_poi, data, model, qtilde=True)
        ),
        "Fit-Time": time.time() - tick,
    }


def count_complete(l):
    return len(list(filter(lambda e: e["result"], l)))


def main():
    # locally get pyhf pallet for analysis
    # if not Path("1Lbb-pallet").exists():
    #     download("https://doi.org/10.17182/hepdata.90607.v3/r3", "1Lbb-pallet")

    input_prefix = "input"
    pallet_name = "InclSS3L-pallet"
    pallet_url = "https://www.hepdata.net/record/resource/1935157?view=true"
    analysis_name = "Rpc2L0b"
    # input_prefix = "input"
    # pallet_name = "1Lbb-pallet"
    # pallet_url = "https://www.hepdata.net/record/resource/1408476?view=true"
    # analysis_name = None

    pallet_path = Path(input_prefix).joinpath(pallet_name)
    analysis_prefix_str = "" if analysis_name is None else f"{analysis_name}_"

    if not pallet_path.exists():
        download(pallet_url, pallet_path)
    with open(
        pallet_path.joinpath(f"{analysis_prefix_str}BkgOnly.json")
    ) as bkgonly_json:
        bkgonly_workspace = json.load(bkgonly_json)

    # with open(f"{patchset_name}patchset.json") as patchset_json:
    #     patchset = pyhf.PatchSet(json.load(patchset_json))
    #     print(patchset)
    #     print(patchset.patches[0])

    #     patch = patchset.patches[0]
    #     patch_name = patch.name
    #     print(patch_name)
    #     print(patch.metadata)
    # ##

    with open("endpoint_id.txt") as endpoint_file:
        pyhf_endpoint = endpoint_file.read()

    print(pyhf_endpoint)

    # Initialize funcX client
    fxc = FuncXClient()
    fxc.max_requests = 200

    # # register and execute background only workspace
    # prepare_func = fxc.register_function(prepare_workspace)
    # infer_func = fxc.register_function(infer_hypotest)
    # prepare_task = fxc.run(
    #     bkgonly_workspace, endpoint_id=pyhf_endpoint, function_id=prepare_func
    # )

    # # While this cooks, let's read in the patch set
    # # patchset = None
    # # with open("1Lbb-pallet/patchset.json", "r") as readfile:
    # #     patchset = json.load(readfile)
    # # patch = patchset["patches"][0]
    # # name = patch["metadata"]["name"]

    with open(
        pallet_path.joinpath(f"{analysis_prefix_str}patchset.json")
    ) as patchset_json:
        patchset = pyhf.PatchSet(json.load(patchset_json))
    patch = patchset.patches[0]

    # workspace = None
    # while not workspace:
    #     try:
    #         workspace = fxc.get_result(prepare_task)
    #     except Exception as excep:
    #         print(f"prepare: {excep}")
    #         sleep(15)

    # print("--------------------")
    # print(workspace)

    # # NUM_RUNS = len(patchset.patches)
    # NUM_RUNS = 5
    # tasks = {}
    # for i in range(NUM_RUNS):
    #     patch = patchset.patches[i]
    #     task_id = fxc.run(
    #         workspace,
    #         patch.metadata,
    #         patch,
    #         endpoint_id=pyhf_endpoint,
    #         function_id=infer_func,
    #     )
    #     tasks[patch.name] = {"id": task_id, "result": None}

    # while count_complete(tasks.values()) < NUM_RUNS:
    #     for task in tasks.keys():
    #         if not tasks[task]["result"]:
    #             try:
    #                 result = fxc.get_result(tasks[task]["id"])
    #                 print(
    #                     f"Task {task} complete, there are {count_complete(tasks.values())} results now"
    #                 )
    #                 tasks[task]["result"] = result
    #             except Exception as excep:
    #                 print(excep)
    #                 sleep(15)

    # print("--------------------")
    # print(tasks.values())


if __name__ == "__main__":
    main()
