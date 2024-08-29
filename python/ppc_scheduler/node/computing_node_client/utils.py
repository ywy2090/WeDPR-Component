from ppc_common.ppc_utils.exception import PpcErrorCode, PpcException


def check_privacy_service_response(response):
    if 'result' not in response.keys():
        raise PpcException(PpcErrorCode.CALL_SCS_ERROR.get_code(), "http request error")
    elif 0 != response['result']['code'] or response['result']['status'] == 'FAILED':
        raise PpcException(PpcErrorCode.CALL_SCS_ERROR.get_code(), response['result']['message'])
