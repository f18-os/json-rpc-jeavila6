# minimalistic server example from
# https://github.com/seprich/py-bson-rpc/blob/master/README.md#quickstart

from node import *
import socket
from bsonrpc import JSONRpc
from bsonrpc import request, service_class
from bsonrpc.framing import JSONFramingNone


# class providing functions for the client to use
@service_class
class ServerServices(object):

    @request
    def increment(self, flattened):
        graph = recreate(flattened)
        root = graph['root']
        self.increment_rec(root)
        flattened = flatten(root, {})
        return flattened

    def increment_rec(self, graph):
        graph.val += 1
        for c in graph.children:
            self.increment_rec(c)
        return graph


# quick-and-dirty TCP Server
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('localhost', 50001))
ss.listen(10)

while True:
    s, _ = ss.accept()
    # JSONRpc object spawns internal thread to serve the connection
    JSONRpc(s, ServerServices(), framing_cls=JSONFramingNone)
