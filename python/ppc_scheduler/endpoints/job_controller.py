# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Resource

from ppc_common.ppc_utils import utils
from ppc_scheduler.common.global_context import components
from ppc_scheduler.endpoints.body_schema import response_job_status, response_base
from ppc_scheduler.endpoints.restx import api

ns = api.namespace('ppc-scheduler/job',
                   description='Operations related to run job')


@ns.route('/<string:job_id>')
class JobCollection(Resource):

    @api.response(201, 'Job started successfully.', response_base)
    def post(self, job_id):
        """
        Run a specific job by job_id.
        """
        args = request.get_json()
        components.logger().info(f"run job request, job_id: {job_id}, args: {args}")
        components.job_manager.run_task(job_id, (args,))
        return utils.BASE_RESPONSE

    @api.response(200, 'Job status retrieved successfully.', response_job_status)
    def get(self, job_id):
        """
        Get the status of a specific job by job_id.
        """
        response = utils.BASE_RESPONSE
        status, time_costs = components.job_manager.status(job_id)
        response['data'] = {
            'status': status,
            'time_costs': time_costs
        }
        return response

    @api.response(200, 'Job killed successfully.', response_base)
    def delete(self, job_id):
        """
        Kill a specific job by job_id.
        """
        components.logger().info(f"kill request, job_id: {job_id}")
        components.job_manager.kill_job(job_id)
        return utils.BASE_RESPONSE
