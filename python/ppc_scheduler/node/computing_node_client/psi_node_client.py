import random
import time

from ppc_common.ppc_utils import http_utils
from ppc_common.ppc_utils.exception import PpcException, PpcErrorCode
from ppc_scheduler.node.computing_node_client.utils import check_privacy_service_response


class PsiClient:
    def __init__(self, log, endpoint, polling_interval_s: int = 5, max_retries: int = 5, retry_delay_s: int = 5):
        self.log = log
        self.endpoint = endpoint
        self.polling_interval_s = polling_interval_s
        self.max_retries = max_retries
        self.retry_delay_s = retry_delay_s
        self._async_run_task_method = 'asyncRunTask'
        self._get_task_status_method = 'getTaskStatus'
        self._completed_status = 'COMPLETED'
        self._failed_status = 'FAILED'

    def run(self, job_info, token):
        params = {
            'jsonrpc': '1',
            'method': self._async_run_task_method,
            'token': token,
            'id': random.randint(1, 65535),
            'params': job_info
        }
        response = self._send_request_with_retry(http_utils.send_post_request, self.endpoint, None, params)
        check_privacy_service_response(response)
        return self._poll_task_status(job_info['taskID'], token)

    def _poll_task_status(self, task_id, token):
        while True:
            params = {
                'jsonrpc': '1',
                'method': self._get_task_status_method,
                'token': token,
                'id': random.randint(1, 65535),
                'params': {
                    'taskID': task_id,
                }
            }
            response = self._send_request_with_retry(http_utils.send_post_request, self.endpoint, None, params)
            check_privacy_service_response(response)
            if response['result']['status'] == self._completed_status:
                return response['result']
            elif response['result']['status'] == self._failed_status:
                self.log.warn(f"task {task_id} failed, response: {response['data']}")
                raise PpcException(PpcErrorCode.CALL_SCS_ERROR.get_code(), response['data'])
            time.sleep(self.polling_interval_s)

    def _send_request_with_retry(self, request_func, *args, **kwargs):
        attempt = 0
        while attempt < self.max_retries:
            try:
                response = request_func(*args, **kwargs)
                return response
            except Exception as e:
                self.log.warn(f"Request failed: {e}, attempt {attempt + 1}/{self.max_retries}")
                attempt += 1
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay_s)
                else:
                    self.log.warn(f"Request failed after {self.max_retries} attempts")
                    raise e
