#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import zmq

from .names import generate_name

# FRB prefix so it won't clash with auto generated variables of docker compose
queue_host = os.environ.get("FRB_QUEUE_HOST", "localhost")
port = os.environ.get("FRB_SERVER_PORT", "5560")

# import pydevd;pydevd.settrace('localhost', port=2500, stdoutToServer=True, stderrToServer=True)


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    SVR_URI = "tcp://{}:{}".format(queue_host, port)
    print('SVR connection : ', SVR_URI)
    socket.connect(SVR_URI)
    server_id = generate_name()

    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN | zmq.POLLOUT)

    colors = {
        'bold': '\033[1m',
        'red': '\033[31m',
        'yellow': '\033[33m',
        'green': '\033[32m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'normal': '\033[0m',
    }

    def log(request):
        msg_template = (
            "{red}[SERVER: {}]"
            "{bold}{red}CLIENT "
            "{yellow}{} "
            "{blue}{}{normal}"
        )
        print(msg_template.format(server_id, request['client_id'], request['message'], **colors))

    while True:
        available = dict(poller.poll())

        if socket not in available:
            # print("{cyan} socket 5560 not in 'availliables'".format(**colors))
            continue

        if available[socket] == zmq.POLLOUT:
            response = {
                'server_id': server_id,
                'message': generate_name()
            }
            # print("{magenta} socket 5560 {bold} SENDING [{message}]".format(message=response, **colors))
            socket.send_json(response)

        if available[socket] == zmq.POLLIN:
            request = socket.recv_json()
            log(request)
        time.sleep(.1)


if __name__ == '__main__':
    main()