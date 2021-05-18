from funcx_endpoint.endpoint.utils.config import Config
from funcx_endpoint.executors import HighThroughputExecutor
from parsl.providers import TorqueProvider
from parsl.launchers import AprunLauncher
from parsl.addresses import address_by_hostname

# PLEASE UPDATE user_opts BEFORE USE
user_opts = {
    "bluewaters": {
        "worker_init": "module load shifter",
        "scheduler_options": "#PBS -l gres=shifter",
    }
}

config = Config(
    executors=[
        HighThroughputExecutor(
            max_workers_per_node=1,
            worker_debug=True,
            address=address_by_hostname(),
            provider=TorqueProvider(
                queue="debug",
                launcher=AprunLauncher(
                    overrides="-b -- shifter --image=neubauergroup/bluewaters-pyhf:0.6.1 -- "
                ),
                # string to prepend to #SBATCH blocks in the submit
                scheduler_options=user_opts["bluewaters"]["scheduler_options"],
                # Command to be run before starting a worker, such as:
                # 'module load bwpy; source activate parsl_env'.
                worker_init=user_opts["bluewaters"]["worker_init"],
                init_blocks=1,
                max_blocks=1,
                min_blocks=1,
                nodes_per_block=4,
                walltime="00:10:00",
            ),
        )
    ],
)
