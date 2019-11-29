import socket, sys, os

class client:

    def __init__(self, argv):
        self.action = argv[1]
        if(self.action == '0'):
            self.client_port = int(argv[4])
        self.address = argv[2]
        self.dest_port = int(argv[3])
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def download_file(self, file_name, ip, port):
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_socket.connect((ip, int(port)))
        new_socket.send(file_name)
        file_content = new_socket.recv(4096)
        with open((file_name), 'w') as f:
            f.write(file_content)
        new_socket.close()

    #Prints optional files in alphabatic order & returns sorted list
    def sort_files_name(self, files):
        files = files.split(',')
        sorted_files = sorted(files)
        counter = 1
        for f in sorted_files:
            print (str(counter) + " " + f.split(" ")[0])
            counter+=1
        return sorted_files

    def get_client_files(self):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        files.remove('client.py')
        files_text = ','.join(files)
        return files_text

    def send_file(self, client_socket, file_name):
        if not os.path.isfile(file_name):
            return False
        with open(file_name, 'r') as f:
            bytes_to_send = f.read(4096)
            client_socket.send(bytes_to_send)

    def set_client_as_server(self):
        files = self.get_client_files()
        self.s.send("1 " + str(self.client_port) + " " + files)
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind(("localhost" , self.client_port))
        listen_socket.listen(2)
        while True:
            client_socket, client_address = listen_socket.accept()
            file_name = client_socket.recv(4096)
            self.send_file(client_socket, file_name)
            client_socket.close()

    def start_client(self):
        self.s.connect((self.address, self.dest_port))

        if(self.action == '0'):
            self.set_client_as_server()
        
        elif(self.action == '1'):
            while True:
                file_name = raw_input("Search: ")
                self.s.send("2 " + file_name) #Tell server to search for files
                files_info = self.s.recv(4096) #receives all available files
                if files_info == '\n':
                    file_num = (int(raw_input("Choose: ")) -1)
                    continue
                sorted_files = self.sort_files_name(files_info)
                file_num = (int(raw_input("Choose: ")) -1)
                if(len(sorted_files) >= file_num): #Check file exists
                    file_name, ip, port =  sorted_files[file_num].split(" ")
                    self.download_file(file_name, ip, port)

        self.s.close()

if __name__ == '__main__':
    if((len(sys.argv) == 4) or (len(sys.argv) == 5)):
        c = client(sys.argv)
        c.start_client()
    print "Please specify all needed information"
    sys.exit()



