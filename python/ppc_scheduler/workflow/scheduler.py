from prefect import Flow
from prefect.executors import LocalDaskExecutor
from prefect.triggers import all_successful, any_failed

from ppc_scheduler.workflow.common import flow_utils
from ppc_scheduler.workflow.common.job_context import JobContext
from ppc_scheduler.workflow.common.worker_status import WorkerStatus
from ppc_scheduler.workflow.common.worker_type import WorkerType
from ppc_scheduler.workflow.constructor import Constructor
from ppc_scheduler.workflow.worker.worker_factory import WorkerFactory


class Scheduler:
    def __init__(self, workspace):
        self.workspace = workspace
        self.constructor = Constructor()

    def schedule_job_flow(self, args):
        job_context = JobContext.load_from_args(args, self.workspace)
        flow_context = self.constructor.build_flow_context(job_context)
        self._run(job_context, flow_context)

    @staticmethod
    def _run(job_context, flow_context):
        job_workers = {}
        job_id = job_context.job_id
        job_flow = Flow(f"job_flow_{job_id}")

        # create a final job worker to handle success
        finish_job_on_success = WorkerFactory.build_worker(
            job_context,
            flow_utils.success_id(job_id),
            WorkerType.T_ON_SUCCESS)

        finish_job_on_success.trigger = all_successful
        finish_job_on_success.bind(worker_status=WorkerStatus.PENDING, worker_inputs=[], flow=job_flow)
        job_flow.add_task(finish_job_on_success)

        # set reference task to bind job flow status
        job_flow.set_reference_tasks([finish_job_on_success])

        # create a final job worker to handle failure
        finish_job_on_failure = WorkerFactory.build_worker(
            job_context,
            flow_utils.failure_id(job_id),
            WorkerType.T_ON_FAILURE)

        # do finish_job_on_failure while any job worker failed
        finish_job_on_failure.trigger = any_failed
        finish_job_on_failure.bind(worker_status=WorkerStatus.PENDING, worker_inputs=[], flow=job_flow)
        job_flow.add_task(finish_job_on_failure)

        # create main job workers
        for worker_id in flow_context:
            worker_type = flow_context[worker_id]['type']
            job_worker = WorkerFactory.build_worker(job_context, worker_id, worker_type)
            job_flow.add_task(job_worker)
            job_workers[worker_id] = job_worker

            # set upstream for final job
            finish_job_on_success.set_upstream(job_worker, flow=job_flow)
            finish_job_on_failure.set_upstream(job_worker, flow=job_flow)

        # customize main job workers
        for worker_id in flow_context:
            # set upstream
            upstreams = flow_context[worker_id]['upstreams']
            for upstream in upstreams:
                if upstream not in job_workers:
                    raise Exception(-1, f"upstream job worker not found: {upstream}, "
                                        f"job_id: {job_context.job_id}")
                job_workers[worker_id].set_upstream(job_workers[upstream], flow=job_flow)

            # bind worker inputs
            inputs_statement = flow_context[worker_id]['inputs_statement']
            worker_inputs = flow_utils.to_worker_inputs(job_workers, inputs_statement)
            job_workers[worker_id].bind(worker_status=flow_context[worker_id]['status'],
                                        worker_inputs=worker_inputs, flow=job_flow)

        # enable parallel execution
        job_flow.executor = LocalDaskExecutor()

        # run dag workflow
        job_flow_state = job_flow.run()

        # save workflow view as file
        job_flow.visualize(job_flow_state, job_context.workflow_view_path, 'svg')
