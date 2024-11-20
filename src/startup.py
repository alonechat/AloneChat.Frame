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
    print('Missing one arg: STARTUP OPTIONS.')
    sys.exit(0)

if   startup_ops in ['c', 'client']:
    from client.client import Client
    client = Client()
    client.start()
    
elif startup_ops in ['s', 'server']:
    from server.server import Server
    server = Server()
    server.start()
    
else:
    raise IndexError('START OPTIONS must in c/s/client/server.')
