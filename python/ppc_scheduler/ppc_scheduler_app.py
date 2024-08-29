# Note: here can't be refactored by autopep

from ppc_scheduler.endpoints.restx import api
from ppc_scheduler.endpoints.job_controller import ns as job_namespace
from ppc_scheduler.common.global_context import components
from paste.translogger import TransLogger
from flask import Flask, Blueprint
from cheroot.wsgi import Server as WSGIServer
from cheroot.ssl.builtin import BuiltinSSLAdapter
import os
import sys
sys.path.append("../")


app = Flask(__name__)


def initialize_app(app):
    # 初始化应用功能组件
    components.init_all()

    app.config.update(components.config_data)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(job_namespace)
    app.register_blueprint(blueprint)


if __name__ == '__main__':
    initialize_app(app)

    app.config['SECRET_KEY'] = os.urandom(24)
    server = WSGIServer((app.config['HOST'], app.config['HTTP_PORT']),
                        TransLogger(app, setup_console_handler=False), numthreads=2)

    ssl_switch = app.config['SSL_SWITCH']
    protocol = 'http'
    if ssl_switch == 1:
        protocol = 'https'
        server.ssl_adapter = BuiltinSSLAdapter(
            certificate=app.config['SSL_CRT'],
            private_key=app.config['SSL_KEY'],
            certificate_chain=app.config['CA_CRT'])

    message = f"Starting ppc scheduler server at {protocol}://{app.config['HOST']}:{app.config['HTTP_PORT']}"
    print(message)
    components.logger().info(message)
    server.start()
