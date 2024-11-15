import sys
from client.client import Client
from server.server import Server

try:
    startup_ops = sys.argv[1]
except IndexError:
    raise IndexError('Missing one arg: STARTUP OPTIONS.')

if sys.argv[1] in ['c', 'client']:
    client = Client()
    client.start()
    
elif sys.argv[1] in ['s', 'server']:
    server = Server()
    Server.start()
    
else:
    raise IndexError('START OPTIONS must in c/s/client/server.')
