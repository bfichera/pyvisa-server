import socket
import argparse

import dill as pickle

from instruments.server.instrumentmanager import MessageHandler
from instruments.server import messages


def _getcfg():
    parser = argparse.ArgumentParser(description='Start instruments server')
    parser.add_argument(
        'address',
        default='127.0.0.1',
    )
    parser.add_argument(
        '--port',
        type=int,
        default=2264,
    )
    args = parser.parse_args()
    return vars(args)


def main(cfg):

    host = cfg['address']
    port = cfg['port']

    message_handler = MessageHandler()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    conn, addr = sock.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = pickle.loads(data)
            if isinstance(message, messages.RequestReturnMessage):
                return_message = message_handler.search_returned_messages(message.message)
                conn.sendall(pickle.dumps(return_message))
            else:
                message_handler.process_message(message)
                conn.sendall(pickle.dumps(messages.EmptyMessage()))


if __name__ == '__main__':
    
    cfg = _getcfg()
    main(cfg)
