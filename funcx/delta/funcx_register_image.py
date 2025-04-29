from funcx import FuncXClient
import json

fx = FuncXClient()
uuid = fx.register_container(
    "/projects/bbmi/bengal1/distributed_inference.sif", container_type="singularity"
)
# distributed-inference: ea20bfaf-b8ef-4b11-ba9b-282152569adf
print("Container ID for distributed_inference is ", uuid)
funcx_object = {"endpoint_id": "", "container_id": uuid}
with open("funcx/delta/funcx.json", "w") as funcx_file:
    json.dump(funcx_object, funcx_file)
