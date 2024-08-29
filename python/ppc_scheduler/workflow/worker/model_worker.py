from ppc_scheduler.node.computing_node_client import ModelClient
from ppc_scheduler.workflow.worker.engine.model_engine import ModelWorkerEngine
from ppc_scheduler.workflow.worker.worker import Worker


class ModelWorker(Worker):

    def __init__(self, components, job_context, worker_id, worker_type, *args, **kwargs):
        super().__init__(components, job_context, worker_id, worker_type, *args, **kwargs)

    def engine_run(self, worker_inputs):
        node_endpoint = self.node_manager.get_node(self.worker_type)
        model_client = ModelClient(self.components.logger(), node_endpoint)
        model_engine = ModelWorkerEngine(model_client, self.worker_type, self.components, self.job_context)
        try:
            outputs = model_engine.run()
            return outputs
        finally:
            self.node_manager.release_node(node_endpoint, self.worker_type)
