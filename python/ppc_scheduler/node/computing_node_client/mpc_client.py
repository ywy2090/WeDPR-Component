import random

from ppc_common.ppc_utils import http_utils, utils
from ppc_scheduler.node.computing_node_client.utils import check_privacy_service_response


class MpcClient:
    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.token = token

    def run(self, job_info):
        params = {
            'jsonrpc': '2',
            'method': 'run',
            'token': self.token,
            'id': random.randint(1, 65535),
            'params': job_info
        }
        response = http_utils.send_post_request(self.endpoint, None, params)
        check_privacy_service_response(response)
        return response['result']

    def kill(self, job_id):
        params = {
            'jsonrpc': '2',
            'method': 'kill',
            'token': self.token,
            'id': random.randint(1, 65535),
            'params': {'jobId': job_id}
        }
        http_utils.send_post_request(self.endpoint, None, params)
        return utils.make_response(0, "success", None)
