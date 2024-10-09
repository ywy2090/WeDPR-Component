# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Resource

from ppc_common.ppc_utils import utils
from ppc_common.ppc_utils.exception import PpcErrorCode, PpcException
from ppc_scheduler.common.global_context import components
from ppc_scheduler.endpoints.body_schema import response_job_status, response_base
from ppc_scheduler.endpoints.restx import api
from ppc_scheduler.mpc_generator.generator import CodeGenerator

ns = api.namespace('/wedpr/v3/scheduler/sql', description='SQL operations')

@ns.route('/transfer')
class SqlCollection(Resource):

    @api.response(200, 'transfer sql to mpc code successfully', response_base)
    def post(self):
        """
        Run a specific job by job_id.
        """
        request_body = request.get_json()
        
        if 'sql' not in request_body:
            raise PpcException(
                    PpcErrorCode.PARAMETER_CHECK_ERROR.get_code(),
                    f"Missing 'sql' in request")
        
        sql = request_body['sql']
        
        components.logger().info(f"Recv SQL conversion to MPC code request, sql: {sql}, request: {request_body}")
        
        code_generator = CodeGenerator(sql)
        try:
            mpc_code = code_generator.sql_to_mpc_code()
            
            response = utils.BASE_RESPONSE
            response['data'] = {
                'mpcContent': mpc_code
            }

            return response
        except PpcException as e:
            components.logger().error(f"PpcException: {e}, request: {request_body}")
            return e.to_dict()
        except Exception as e:
            components.logger().error(f"unexpected exception: {e}, request: {request_body}")
            return utils.INTERNAL_ERROR_RESPONSE
        