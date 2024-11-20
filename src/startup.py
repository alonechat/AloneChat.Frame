import os
import sys

sys.path.extend([
    os.path.abspath(
        os.path.join(os.path.dirname(
            __file__
        ), 'server')
    ),
    os.path.abspath(
        os.path.join(os.path.dirname(
            __file__
        ), 'client')
    )
])

try:
    startup_ops = sys.argv[1]
except IndexError:
    raise IndexError('Missing one arg: STARTUP OPTIONS.')

if sys.argv[1] in ['c', 'client']:
    from client.client import Client
    client = Client()
    client.start()
    
elif sys.argv[1] in ['s', 'server']:
    from server.server import Server
    server = Server()
    server.start()
    
else:
    raise IndexError('START OPTIONS must in c/s/client/server.')
