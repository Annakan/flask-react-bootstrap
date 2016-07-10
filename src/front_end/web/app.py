#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import eventlet
import eventlet.green.zmq as zmq
from subprocess import Popen, PIPE, STDOUT
import logging
import coloredlogs
from datetime import datetime
import random


from flask import Flask, render_template
from flask import copy_current_request_context
from flask import send_from_directory
from flask.ext.socketio import SocketIO, emit

# from werkzeug.debug import DebuggedApplication


# eventlet.monkey_patch()
eventlet.patcher.monkey_patch(all=False, socket=True, time=True, thread=False)

logger = logging.getLogger('flask-app')

queue_host = os.environ.get("FRB_QUEUE_HOST", "localhost")
monitor_port = os.environ.get("FRB_MONITOR_PORT", "5570")
MONITOR_URI = 'tcp://{}:{}'.format(queue_host, monitor_port)

web = Flask(__name__)
web.config['SECRET_KEY'] = 'thre is no secret in this source code!'
web.config['dist'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
# web.wsgi_app = DebuggedApplication(web.wsgi_app, evalex=True, pin_logging=False)

socketio = SocketIO(web, async_mode="eventlet")


zmq_context = zmq.Context()


def parse_monitor(raw):
    topic, binary, _, msg = raw
    data = json.loads(msg.decode())
    return {
        'topic': topic.decode(),
        'data': data
    }


@web.route('/')
def index():
    result = render_template('index.html')
    return result


@web.route('/favicon.ico')
def favicon():
    return send_from_directory('styles', 'favicon.ico')


@web.route('/dist/<path:path>')
def send_js(path):
    return send_from_directory(web.config['dist'], path)


@socketio.on('hello')
def websocket_hello(data):
    logger.info('web client HELLO : connected %s: ', data)
    emit('ready', {'ready': datetime.utcnow().strftime('%B %d, %Y')})
    eventlet.sleep(0)
    if int(data.get('connection_attempt', 0)) == 0:
        emit('zeromq', {"topic": "msg", "data": 'Hey, this is a message coming from flask through socket.io'})
        emit('zeromq', {"topic": "msg", "data": 'as acknowledgement that the client/server connection is healthy. Yay!'})
    else:
        emit('zeromq', {"topic": "msg", "data": 'reconnected to server'})

    eventlet.sleep(0)


@socketio.on('zeromq')
def websocket_zeromq(*args, **kwargs):
    # print("spawn emit queue change greenlet")
    eventlet.sleep(0)
    # print('After spanw : ', len(green_pool.coroutines_running))

#
# Dead code in the original code
#
#
# @socketio.on('publisher_spawn')
# def websocket_console(*data, **kw):
#     logger.info("Client asked for publisher: %s", data)
#     cmd = 'ping google.com'
#
#     process = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
#     emit('shell', {'clear': True, 'line': '{0}\n'.format(cmd)})
#
#     while True:
#         raw = process.stdout.readline()
#         if not raw:
#             break
#
#         eventlet.sleep(0)
#         emit('shell', {'line': str(raw, 'utf-8')})
#         eventlet.sleep(0)


def emit_queue_changes(monitor_zsocket):
    # logger.info('listening to zeromq on 0.0.0.0:8888')
    # running = True
    # while running:
    poller = zmq.Poller()
    poller.register(monitor_zsocket, zmq.POLLIN)
    socks = dict(poller.poll())
    eventlet.sleep(0)
    while True:
        if monitor_zsocket in socks and socks[monitor_zsocket] == zmq.POLLIN:
            raw = monitor_zsocket.recv_multipart()
            try:
                data = parse_monitor(raw)
                socketio.emit('zeromq', data)
                eventlet.sleep(0)
            except TypeError:
                logger.exception("could not json decode %s", repr(raw))
            eventlet.sleep(0)


def main():
    green_pool = eventlet.greenpool.GreenPool()
    monitor_zsocket = zmq_context.socket(zmq.SUB)
    monitor_zsocket.setsockopt(zmq.SUBSCRIBE, b'')
    monitor_zsocket.connect(MONITOR_URI)
    print("connected [{}]".format(MONITOR_URI))
    logging.getLogger("requests").setLevel(logging.WARNING)
    spawned_pool = [(i, green_pool.spawn(emit_queue_changes, monitor_zsocket)) for i in range(1, 25)]
    print(spawned_pool)

    coloredlogs.install(level=logging.DEBUG, show_hostname=False)
    socketio.run(web, host='0.0.0.0')


if __name__ == '__main__':
    main()
