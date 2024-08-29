# -*- coding: utf-8 -*-
import json

from flask_restx import fields

from ppc_model.network.http.restx import api

response_base = api.model('Response base info', {
    'errorCode': fields.Integer(description='return code'),
    'message': fields.String(description='return message')
})

response_job_status = api.inherit('Task status', response_base, {
    'data': fields.Raw(description='Task status data as key-value dictionary', example={
        'status': 'RUNNING',
        'time_costs': '30s'
    })
})
