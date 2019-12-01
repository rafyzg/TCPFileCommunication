# TCPFileCommunication
Just 2 simple client & server sockets for file sharing
###Client 
Client can select to share his files(Provider) just like that:
```
python client.py 0 [Server address] [server port] [your own port] 
```
On the otherhand client can select to only download existing file in server(Consumer):
```
python client.py 1 [Server address] [server port]
```

###Server
The server is used as a pipeline for the communication of the provider and consumer.
 - If a client is a provider the server saves his files and corresponding information
 - If a Client is a consumer the server sends his the available files and send him the needed information to connect to 
   the file owner
To start the Server just specify the port
```
python server.py [Server port]
```
