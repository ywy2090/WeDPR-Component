from ppc_scheduler.node.computing_node_client.psi_client import PsiClient
from ppc_scheduler.workflow.worker.engine.psi_engine import PsiWorkerEngine
from ppc_scheduler.workflow.worker.worker import Worker


class PsiWorker(Worker):

    def __init__(self, components, job_context, worker_id, worker_type, worker_args, *args, **kwargs):
        super().__init__(components, job_context, worker_id, worker_type, worker_args, *args, **kwargs)

    def engine_run(self, worker_inputs) -> list:
        logger = self.components.logger()
        psi_client_node = self.computing_node_manager.get_node(self.worker_type)
        logger.info(f"## getting psi client : {psi_client_node}")
        psi_client = PsiClient(logger, psi_client_node.url, psi_client_node.token)
        psi_engine = PsiWorkerEngine(psi_client, self.worker_id, self.worker_type, self.components, self.job_context)
        try:
            outputs = psi_engine.run(*self.worker_args)
            return outputs
        finally:
            self.computing_node_manager.release_node(psi_client_node.id)
