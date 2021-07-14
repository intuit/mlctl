import gevent.monkey
gevent.monkey.patch_all()

import os
import json
import logging
import sys
import inspect
import signal
import subprocess

import six
import psutil
from flask import Flask, request
import gunicorn.app.base


# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------

logger = logging.getLogger('baklava')
logger.addHandler(logging.NullHandler())


class FlaskRequestFormatter(logging.Formatter):
    """
    Class to add tid to log messages.
    """

    def format(self, record):
        # Runtime error will occur if not in a request context
        try:
            record.tid = request.headers.get("X-Amzn-SageMaker-Custom-Attributes", "-")
        except RuntimeError as e:
            record.tid = "-"
        return super().format(record)


def configure_logger():
    """
    Configure a logger to use standard format and levels.
    """
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = FlaskRequestFormatter(
        fmt="time=%(asctime)s.%(msecs)03d level=%(levelname)s tid=%(tid)s file=%(filename)s:%(lineno)s %(message)s",
        datefmt='%Y-%m-%d,%H:%M:%S'
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


# ------------------------------------------------------------------------------
# Server Setup
# ------------------------------------------------------------------------------

def application(func):

    configure_logger()

    # --------------------------------------------------------------------------
    # Check that function is lambda-like
    # --------------------------------------------------------------------------

    if sys.version_info.major == 2:
        spec = inspect.getargspec(func)
    else:
        spec = inspect.getfullargspec(func)

    if len(spec.args) != 1:
        raise ValueError(
            'Expected method to have exactly 1 argument, got {} arguments: {}'
            .format(len(spec.args), spec.args)
        )

    if spec.varargs is not None:
        raise ValueError(
            'Expected method to have 1 argument, but got variable arguments: {}'
            .format(spec.varargs)
        )

    # --------------------------------------------------------------------------
    # Flask
    # --------------------------------------------------------------------------

    app = Flask(__name__)

    # --------------------------------------------------------------------------
    # Routes
    # --------------------------------------------------------------------------

    @app.route('/invocations', methods=['POST'])
    def invocations():
        """
        Execute a python function
        Uses the JSON body of the POST request to as an input to the python
        function. The JSON inputwill be parsed into a dictionary and passed into
        the function. The output of the function is expected to be a JSON
        string.
        ---
        tags:
            - endpoint
        consumes:
            - application/json
        produces:
            - application/json
        parameters:

            - in: body
              name: body
              description: The data to use as the model inputs
              required: true
              type: object
              schema:
                properties:
                  tid:
                    type: str
                    default: "748babba-d287-4082-9c12-ea46e7a5146e"
                  id:
                    type: str
                    default: "123456789"
                  data:
                    type: object
                    schema:
                      properties:
                        example:
                          type: int
                          default: 1
        """

        if request.content_type == 'application/json':
            data = request.get_json()  # type: dict[str, object]
        else:
            data = request.get_data()  # type: bytes

        # Execute lambda
        result = func(data)
        return result

    @app.route('/ping', methods=['GET'])
    def ping():
        """
        Check if the server is running

        Will always output success as long as the server is running. Otherwise
        expect a 404.
        ---
        tags:
            - endpoint
        produces:
            - application/json
        """
        return json.dumps({'success': True})

    def sigterm_handler(signum, frame):
        # Shutdown Flask application when SIGTERM is received as a result of
        # "docker stop" command
        app.shutdown()

    signal.signal(signal.SIGTERM, sigterm_handler)
    return app


class Server(gunicorn.app.base.BaseApplication):

    def __init__(self, func, initializer=None, **options):
        self.initializer = initializer
        self.options = options or {}
        self.app = application(func)
        super(Server, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in six.iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in six.iteritems(config):
            self.cfg.set(key.lower(), value)

        # Register initialization function with the worker
        def initialize(arbiter, worker):
            self.initializer()

        if self.initializer:
            self.cfg.set('post_fork', initialize)

    def load(self):
        return self.app


def timeout():
    if 'LAMBDA_SERVER_TIMEOUT' in os.environ:
        return int(os.environ['LAMBDA_SERVER_TIMEOUT'])
    return 600


def number_of_workers():
    """
    Get the number of workers for gunicorn.

    This can be explicitly set by using the LAMBDA_SERVER_WORKERS environment
    variable. The number is expected to be an integer.

    This returns 2 by default. The default option is generally used during
    testing, so use the minimum number of workers to test a multi-worker server.

    By setting the environment variable to "auto", the number of workers will
    scale by the number of physical cores. Note that this can cause unexpected
    behavior in local docker containers. Without specific configuration, docker
    will report 1 physical core (default for OSX).

    Returns:
        n_workers (int): The number of workers
    """
    if 'LAMBDA_SERVER_WORKERS' in os.environ:
        value = os.environ['LAMBDA_SERVER_WORKERS']
        if value == 'auto':
            return psutil.cpu_count(logical=False)
        try:
            return int(value)
        except:
            pass
    return 2


def run(func, initializer=None):

    # Create gunicorn application
    server = Server(
        func=func,
        initializer=initializer,
        bind='unix:/tmp/gunicorn.sock',
        workers=number_of_workers(),
        worker_class='gevent',
        worker_tmp_dir='/dev/shm',
        timeout=timeout(),
    )

    # Start nginx
    subprocess.Popen(['nginx', '-c', '/opt/nginx.conf'])

    # Start gunicorn server
    server.run()


if __name__ == '__main__':
    $entrypoint
    $initializer
    run(entrypoint, initializer)
