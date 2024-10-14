import time

from ppc_scheduler.workflow.common.job_context import JobContext
from ppc_scheduler.workflow.common.worker_type import WorkerType
from ppc_scheduler.workflow.worker.engine.work_engine import WorkerEngine

class ModelWorkerEngine(WorkerEngine):
    def __init__(self, model_client, worker_type, worker_id, components, job_context: JobContext):
        self.model_client = model_client
        self.worker_type = worker_type
        self.worker_id = worker_id
        self.components = components
        self.job_context = job_context
        self.logger = self.components.logger()

    def run(self, *args) -> list:
        if self.worker_type == WorkerType.T_PREPROCESSING\
            or self.worker_type == WorkerType.T_FEATURE_ENGINEERING\
            or self.worker_type == WorkerType.T_TRAINING\
            or self.worker_type == WorkerType.T_PREDICTION:
            pass
        else:
            raise ValueError(f"Unsupported worker type: {self.worker_type}")
        
        job_id = self.job_context.job_id
        start_time = time.time()

        self.logger.info(f"## model engine run begin, job_id={job_id}, worker_id={self.worker_id}, args: {args}")
        
        # send job request to model node and wait for the job to finish
        self.model_client.run(*args)
        
        time_costs = time.time() - start_time
        self.logger.info(f"## model engine run finished, job_id={job_id}, timecost: {time_costs}s")
        
        return []
