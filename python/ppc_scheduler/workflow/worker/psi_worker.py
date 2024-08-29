from ppc_scheduler.node.computing_node_client.psi_node_client import PsiClient
from ppc_scheduler.workflow.worker.engine.psi_engine import PsiWorkerEngine
from ppc_scheduler.workflow.worker.worker import Worker


class PsiWorker(Worker):

    def __init__(self, components, job_context, worker_id, worker_type, *args, **kwargs):
        super().__init__(components, job_context, worker_id, worker_type, *args, **kwargs)

    def engine_run(self, worker_inputs) -> list:
        node_endpoint = self.node_manager.get_node(self.worker_type)
        psi_client = PsiClient(self.components.logger(), node_endpoint)
        psi_engine = PsiWorkerEngine(psi_client, self.worker_type, self.components, self.job_context)
        try:
            outputs = psi_engine.run()
            return outputs
        finally:
            self.node_manager.release_node(node_endpoint, self.worker_type)
