import socket, threading, sys

class server:

    def __init__(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = '0.0.0.0'
        self.port = port #Server port
        self.clients = {} #Clients address - sockets dictionary
        self.files = {} #Clients address - files dictionary

    '''
    Input: string - file name(or part of it)
    Function returns all the files it found & corresponding port and ip address
    '''
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
    
    '''
    Input: client address, port and files data
    This function save all information to server's database
    '''
    def save_client_info(self, client_address, port, files_str):
        #Save client's port
        self.clients[client_address]['port'] = port
        files = ""
        if(len(files_str) > 0): #If client does have files to share
            files = files_str
            if ',' in files_str: #If client has more than one file to share
                files = files.split(',')             
        #Save client's files
        self.files[client_address] = files
    
    def start_server(self):
        self.server.bind((self.server_address, self.port))
        self.server.listen(5)

        while True:
            #Accept new connection
            client_socket, client_address = self.server.accept()
            #Add to new client to database
            self.clients[client_address] = { 'socket' : client_socket }
            data = client_socket.recv(1024).strip('\n').split(' ')
            
            #Register and share files
            if(data[0] == '1'): 
                #Save client port & files
                port = int(data[1])
                self.save_client_info(client_address, port, data[2])

            #Search for files
            elif(data[0] == '2'): 
                name = data[1]
                found_files = self.search_for_files(name)
                client_socket.send(found_files) #Send client found files
            #Close socket
            client_socket.close() 

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print "Please specify all needed information"
        sys.exit()
    s = server(int(sys.argv[1]))
    s.start_server()
