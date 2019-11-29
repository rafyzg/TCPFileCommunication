import socket, threading, sys

class server:

    def __init__(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = '0.0.0.0'
        self.port = port
        self.clients = {} #Clients address - sockets dictionary
        self.files = {} #Clients address - files dictionary

    def search_for_files(self, name):
        found_files = ""
        for client in self.files:
            for f in self.files[client]:
                if(name in f):
                    found_files += f + " " + str(client[0]) + " " + str(self.clients[client]['port']) + ","
        if(found_files[-1:] == ','):
            found_files = found_files[:-1]
        found_files += '\n'
        return found_files
    
    def start_server(self):
        self.server.bind((self.server_address, self.port))
        self.server.listen(5)

        while True:

            client_socket, client_address = self.server.accept()
            self.clients[client_address] = { 'socket' : client_socket }
            data = client_socket.recv(1024).split(' ')
            if(data[0] == '1'): #Register and share files
                #Save client socket & port
                self.clients[client_address]['port'] = int(data[1])
                files = data[2].split(',')
                #Save client files
                self.files[client_address] = files

            elif(data[0] == '2'): #Search files
                found_files = self.search_for_files(data[1])
                client_socket.send(found_files)

            client_socket.close()

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print "Please specify all needed information"
        sys.exit()
    s = server(int(sys.argv[1]))
    s.start_server()
