# -*- coding: utf-8 -*-
from ppc_common.db_models.job_worker_record import JobWorkerRecord
from ppc_common.ppc_utils import utils
from ppc_scheduler.common.global_context import components
from ppc_scheduler.database import job_worker_mapper
from ppc_scheduler.workflow.common import codec, flow_utils
from ppc_scheduler.workflow.common.job_context import JobContext
from ppc_scheduler.workflow.common.worker_status import WorkerStatus


class Constructor:
    def __init__(self):
        self.log = components.logger()

    def build_flow_context(self, job_context: JobContext):
        self.log.info(f"start build_flow_context, job_id: {job_context.job_id}")
        job_id = job_context.job_id
        flow_context = {}
        index_type_map = {}
        for worker_config in job_context.worker_configs:
            index_type_map[worker_config['index']] = worker_config['type']

        for worker_config in job_context.worker_configs:
            worker_type = worker_config['type']
            worker_id = flow_utils.cat_worker_id(job_id, worker_config['index'], worker_type)
            upstreams = []
            inputs_statement = []
            inputs_statement_tuple = []
            if 'upstream' in worker_config:
                for upstream_config in worker_config["upstreams"]:
                    index = upstream_config['index']
                    upstream_id = flow_utils.cat_worker_id(job_id, index, index_type_map[index])
                    upstreams.append(upstream_id),
                    if 'output_input_map' in upstream_config:
                        for mapping in upstream_config.get("output_input_map", []):
                            output_index, input_index = mapping.split(":")
                            inputs_statement_tuple.append((upstream_id, int(output_index), int(input_index)))

            inputs_statement_tuple.sort(key=lambda x: x[2])
            for upstream_id, output_index, _ in inputs_statement_tuple:
                inputs_statement.append(
                    {
                        'output_index': output_index,
                        'upstream': upstream_id
                    }
                )
            worker_context = self._construct_context(job_context, worker_id, worker_type,
                                                     upstreams, inputs_statement)
            flow_context[worker_id] = worker_context
        self.log.info(f"end build_flow_context, flow_context:\n{flow_context}")

    def _construct_context(self, job_context, worker_id, worker_type, upstreams, inputs_statement):
        context = {
            'type': worker_type,
            'status': WorkerStatus.PENDING,
            'upstreams': upstreams,
            'inputs_statement': inputs_statement
        }

        with components.create_sql_session() as session:
            worker_record = job_worker_mapper.query_job_worker(components.create_sql_session,
                                                               job_context.job_id, worker_id)
            if worker_record is None:
                worker_record = JobWorkerRecord(
                    worker_id=worker_id,
                    job_id=job_context.job_id,
                    type=worker_type,
                    status=WorkerStatus.PENDING,
                    upstreams=codec.serialize_upstreams_for_db(upstreams),
                    inputs_statement=codec.serialize_inputs_statement_for_db(inputs_statement),
                    create_time=utils.make_timestamp(),
                    update_time=utils.make_timestamp()
                )
                session.add(worker_record)
                session.commit()
            else:
                context['status'] = worker_record.status
                context['upstreams'] = codec.deserialize_upstreams(worker_record.upstreams)
                context['inputs_statement'] = codec.deserialize_inputs_statement(worker_record.inputs_statement)

            self.log.debug(f"Load worker_context successfully, worker_id: {worker_id}, context:\n{context}")
            return context
