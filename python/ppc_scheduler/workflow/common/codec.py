from ppc_common.ppc_protos.generated.ppc_pb2 import JobWorkerOutputs, JobWorkerUpstreams, \
    InputStatement, JobWorkerInputsStatement
from ppc_common.ppc_utils import utils


def deserialize_worker_outputs(outputs_str):
    outputs = []
    outputs_pb = JobWorkerOutputs()
    utils.str_to_pb(outputs_pb, outputs_str)
    for output in outputs_pb.outputs:
        outputs.append(output)
    return outputs


def serialize_worker_outputs_for_db(outputs):
    outputs_pb = JobWorkerOutputs()
    for output in outputs:
        outputs_pb.outputs.append(output)
    return utils.pb_to_str(outputs_pb)


def deserialize_upstreams(upstreams_str):
    upstreams = []
    upstream_pb = JobWorkerUpstreams()
    utils.str_to_pb(upstream_pb, upstreams_str)
    for upstream in upstream_pb.upstreams:
        upstreams.append(upstream)
    return upstreams


def serialize_upstreams_for_db(upstreams):
    upstreams_pb = JobWorkerUpstreams()
    for upstream in upstreams:
        upstreams_pb.upstreams.append(upstream)
    return utils.pb_to_str(upstreams_pb)


def deserialize_inputs_statement(inputs_statement_str):
    inputs_statement = []
    inputs_statement_pb = JobWorkerInputsStatement()
    utils.str_to_pb(inputs_statement_pb, inputs_statement_str)
    for input_statement_pb in inputs_statement_pb.inputs_statement:
        inputs_statement.append({
            'upstream': input_statement_pb.upstream,
            'output_index': input_statement_pb.output_index
        })
    return inputs_statement


def serialize_inputs_statement_for_db(inputs_statement):
    inputs_statement_pb = JobWorkerInputsStatement()
    for input_statement in inputs_statement:
        input_statement_pb = InputStatement()
        input_statement_pb.upstream = input_statement['upstream']
        input_statement_pb.output_index = input_statement['output_index']
        inputs_statement_pb.inputs_statement.append(input_statement_pb)
    return utils.pb_to_str(inputs_statement_pb)
