# minimalistic client example from
# https://github.com/seprich/py-bson-rpc/blob/master/README.md#quickstart

import socket
from bsonrpc import JSONRpc
from bsonrpc.framing import JSONFramingNone
from node import *

# cut-the-corners TCP Client:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50001))

rpc = JSONRpc(s, framing_cls=JSONFramingNone)
server = rpc.get_peer_proxy()

node6 = Node("node6", [])
node5 = Node("node5", [node6])
node4 = Node("node4", [])
node2 = Node("node2", [node4, node5, node5])
node7 = Node("node7", [])
node3 = Node("node3", [node7, node7])
node1 = Node("node1", [])
root = Node("root", [node1, node2, node2, node3])

print("Graph before increment:")
root.show()

flattened = flatten(root, {})  # flatten graph
result = server.increment(flattened)  # send graph to increment
root = recreate(result)['root']  # rebuild graph from result

print("Graph after increment:")
root.show()

rpc.close()  # Closes the socket 's' also
