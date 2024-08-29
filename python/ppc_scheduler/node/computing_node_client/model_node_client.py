import time

from ppc_common.ppc_utils import http_utils
from ppc_common.ppc_utils.exception import PpcException, PpcErrorCode

RUN_MODEL_API_PREFIX = "/api/ppc-model/pml/run-model-task/"
GET_MODEL_LOG_API_PREFIX = "/api/ppc-model/pml/record-model-log/"


class ModelClient:
    def __init__(self, log, endpoint, polling_interval_s: int = 5, max_retries: int = 5, retry_delay_s: int = 5):
        self.log = log
        self.endpoint = endpoint
        self.polling_interval_s = polling_interval_s
        self.max_retries = max_retries
        self.retry_delay_s = retry_delay_s
        self._completed_status = 'COMPLETED'
        self._failed_status = 'FAILED'

    def run(self, args):
        task_id = args['task_id']
        try:
            self.log.info(f"ModelApi: begin to run model task {task_id}")
            response = self._send_request_with_retry(http_utils.send_post_request,
                                                     endpoint=self.endpoint,
                                                     uri=RUN_MODEL_API_PREFIX + task_id,
                                                     params=args)
            check_response(response)
            return self._poll_task_status(task_id)
        except Exception as e:
            self.log.error(f"ModelApi: run model task error, task: {task_id}, error: {e}")
            raise e

    def kill(self, job_id):
        try:
            self.log.info(f"ModelApi: begin to kill model task {job_id}")
            response = self._send_request_with_retry(http_utils.send_delete_request,
                                                     endpoint=self.endpoint,
                                                     uri=RUN_MODEL_API_PREFIX + job_id)
            check_response(response)
            self.log.info(f"ModelApi: model task {job_id} was killed")
            return response
        except Exception as e:
            self.log.warn(f"ModelApi: kill model task {job_id} failed, error: {e}")
            raise e

    def _poll_task_status(self, task_id):
        while True:
            response = self._send_request_with_retry(http_utils.send_get_request,
                                                     endpoint=self.endpoint,
                                                     uri=RUN_MODEL_API_PREFIX + task_id)
            check_response(response)
            if response['data']['status'] == self._completed_status:
                self.log.info(f"task {task_id} completed, response: {response['data']}")
                return response
            elif response['data']['status'] == self._failed_status:
                self.log.warn(f"task {task_id} failed, response: {response['data']}")
                raise PpcException(PpcErrorCode.CALL_SCS_ERROR.get_code(), response['data'])
            else:
                time.sleep(self.polling_interval_s)

    def get_remote_log(self, job_id):
        response = self._send_request_with_retry(http_utils.send_get_request,
                                                 endpoint=self.endpoint,
                                                 uri=GET_MODEL_LOG_API_PREFIX + job_id)
        check_response(response)
        return response['data']

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


def check_response(response):
    if response['errorCode'] != 0:
        raise PpcException(PpcErrorCode.CALL_SCS_ERROR.get_code(), response['message'])
