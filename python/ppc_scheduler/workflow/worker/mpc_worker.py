from ppc_scheduler.node.computing_node_client.mpc_client import MpcClient
from ppc_scheduler.workflow.worker.engine.mpc_engine import MpcWorkerEngine
from ppc_scheduler.workflow.worker.worker import Worker


class MpcWorker(Worker):

    def __init__(self, components, job_context, worker_id, worker_type, worker_args, *args, **kwargs):
        super().__init__(components, job_context, worker_id, worker_type, worker_args, *args, **kwargs)

    def engine_run(self, worker_inputs) -> list:
        logger = self.components.logger()
        mpc_client_node = self.computing_node_manager.get_node(self.worker_type)
        logger.info(f"## getting mpc client : {mpc_client_node}")
        mpc_client = MpcClient(mpc_client_node.url, mpc_client_node.token)
        mpc_engine = MpcWorkerEngine(mpc_client, self.worker_type, self.worker_id, self.components, self.job_context)
        try:
            outputs = mpc_engine.run(*self.worker_args)
            return outputs
        finally:
            self.computing_node_manager.release_node(mpc_client_node.id)
