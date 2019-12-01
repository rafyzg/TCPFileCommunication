import socket, sys, os

class client:

    def __init__(self, argv):
        self.action = argv[1]
        if(self.action == '0'): #If client shares files then set port
            self.client_port = int(argv[4])
        self.address = argv[2]
        self.dest_port = int(argv[3])
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    '''
    Input: file's name, ip and port
    This function connects to the owner of the requested file,
    and gets the file information and saves it as a new file
    '''
    def download_file(self, file_name, ip, port):
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_socket.connect(( ip, port ))
        new_socket.send(file_name)
        #Receive file content
        file_content = new_socket.recv(4096)
        #Create new file and set its data
        with open((file_name), 'w') as f:
            f.write(file_content)

    #Prints optional files in alphabatic order & returns sorted list
    '''
    Input: files string
    This function organizes & splits the files string and prints it to the user
    '''
    def sort_files_name(self, files):
        files = files.split(',')
        sorted_files = sorted(files)
        counter = 1
        for f in sorted_files:
            print (str(counter) + " " + f.split(" ")[0])
            counter+=1
        return sorted_files

    #Gets all shareable files by the client
    def get_client_files(self):
        #Find all files in current directory
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        files.remove('client.py') #Remove the running python file
        files_text = ','.join(files)
        return files_text

    '''
    Input: client socket, file name
    This function reads the requested file and sends the content to the requestor
    '''
    def send_file(self, client_socket, file_name):
        if not os.path.isfile(file_name):
            return False
        with open(file_name, 'r') as f:
            bytes_to_send = f.read(4096)
            client_socket.send(bytes_to_send)

    '''

    '''
    def set_client_as_server(self):
        files = self.get_client_files()
        #Register at server
        self.s.send("1 " + str(self.client_port) + " " + files)
        #Create new socket for client
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind(("0.0.0.0" , self.client_port))
        listen_socket.listen(2)
        while True:
            client_socket, client_address = listen_socket.accept() 
            file_name = client_socket.recv(4096)
            #Send file to requestor
            self.send_file(client_socket, file_name)
            #Close connection with the requestor
            client_socket.close()

    def start_client(self):
        self.s.connect((self.address, self.dest_port))

        #If user wants to share files
        if(self.action == '0'):
            self.set_client_as_server()
        
        #if user want to download files
        elif(self.action == '1'):
            while True:
                file_name = raw_input("Search: ")
                #Tell server to search for files
                self.s.send("2 " + file_name)
                #Receive all available files
                files_info = self.s.recv(4096) 
                if files_info == '\n': #If no files found
                    file_num = (int(raw_input("Choose: ")) -1)
                    continue
                #Print files to user
                sorted_files = self.sort_files_name(files_info)
                file_num = (int(raw_input("Choose: ")) -1)
                if(len(sorted_files) >= file_num): #Check file exists
                    file_name, ip, port =  sorted_files[file_num].split(" ")
                    #Download file from file owner
                    self.download_file(file_name, ip, int(port)) 

        self.s.close()

if __name__ == '__main__':
    #Correct argument length
    if((len(sys.argv) == 4) or (len(sys.argv) == 5)):
        c = client(sys.argv)
        c.start_client()
    #Incorrect argument length
    else :
        print "Please specify all needed information"
        sys.exit()



