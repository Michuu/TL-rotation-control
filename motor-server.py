# --------------------------------------------------------------------------- #
# File: pyrplserver.py                                                        #
# File Created: Thursday, 18th February 2021 @ HAL9k                          #
# Author: Mateusz Mazelanik (mateusz.mazelanik@gmail.com)                     #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Last Modified: Tuesday, 23rd February 2021 @ HAL9k                          #
# Modified By: Mateusz Mazelanik (mateusz.mazelanik@gmail.com)                #
# --------------------------------------------------------------------------- #
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(name=__name__)

import aiozmq.rpc
import aiozmq
import functools
import msgpack_numpy as m
import numpy
import msgpack
import sys
import socket


import asyncio
from elliptec import Motor, find_ports

#logger.setLevel(logging.INFO)
    
hostname = socket.gethostname()

#asyncio.set_event_loop(LOOP)


class ServerHandler(aiozmq.rpc.AttrHandler):
    def __init__(self, obj, logger):
        self.obj = obj
        self.logger = logger

    @aiozmq.rpc.method
    def rsetattr(self, attr, val):
        obj = self.obj
        pre, _, post = attr.rpartition('.')
        return setattr(self.rgetattr(pre) if pre else obj, post, val)

    @aiozmq.rpc.method
    def rgetattr(self, attr, *args):
        self.logger.info(f'getattr: {attr}')
        obj = self.obj

        def _getattr(obj, attr):
            return getattr(obj, attr, *args)
        return functools.reduce(_getattr, [obj] + attr.split('.'))

    @aiozmq.rpc.method
    def rcall(self, attr, *args):
        method = self.rgetattr(attr)
        return method(*args)

    @aiozmq.rpc.method
    def log(self, *args):
        self.logger.info(str(list(args)))

def pack_numpy(value):
    logger.debug(f'Packing {type(value)}')
    return msgpack.packb(value, default=m.encode)

def unpack_numpy(binary):
    logger.debug(f'UnPacking {type(binary)}')
    return msgpack.unpackb(binary, object_hook=m.decode)

translation_table = {
    0: (numpy.ndarray,
        pack_numpy,
        unpack_numpy)
}


@asyncio.coroutine
def start_server(obj, logger, port):
    local_ip = socket.gethostbyname(hostname)
    server = yield from aiozmq.rpc.serve_rpc(
        ServerHandler(obj, logger), bind='tcp://' + local_ip + ':' + str(port),
        translation_table=translation_table, log_exceptions=True)
    logger.info(
        f'Moror server listenning at: {list(server.transport.bindings())[0]} | hostname: {hostname}')
    yield from loop()

async def loop():
    #logger = logging.getLogger(name=__name__)
    #logger.setLevel(logging.INFO)
    while True:
        #logger.info('bib')
        await asyncio.sleep(1)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        print("usage: python motor-server.py [[comport=]comport] ")
    kwargs = dict()
    for i, arg in enumerate(sys.argv):
        print(i, arg)
        if i == 0:
            continue
        try:
            k, v = arg.split('=', 1)
        except ValueError:
            k, v = arg, ""
        if v == "":
            if i == 1:
                kwargs["comport"] = k
        else:
            kwargs[k] = v

    if '--help' in kwargs:
        print(help_message)
    else:
        port = kwargs.pop('port', 9970)
        print("Calling Pyrpl(**%s)" % str(kwargs))
        ports = find_ports()
        motor=Motor(ports[int(kwargs['comport'])].device)
        #task = asyncio.ensure_future(start_server(motor, logger, port))
        #print(task)
        #asyncio.run(loop())
        asyncio.run(start_server(motor, logger, port))
        #APP.exec_()
