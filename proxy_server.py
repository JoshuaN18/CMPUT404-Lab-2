#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():

    proxy_host = 'www.google.com'
    proxy_port = 80
    buffer_size = 4096

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            #create a new server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:


            #recieve data, wait a bit, then send it back
                remote_ip = get_remote_ip(proxy_host)
                proxy_end.connect((remote_ip, proxy_port))
                p = Process(target=echo_handler, args=(proxy_end, conn, addr))
                p.daemon = True
                p.start()
                print("Started Process ", p)
            conn.close()

def echo_handler(proxy_end, conn, addr):
    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
    proxy_end.sendall(full_data)
    time.sleep(0.5)
    proxy_end.shutdown(socket.SHUT_WR)
    data = proxy_end.recv(BUFFER_SIZE)
    conn.send(data)

if __name__ == "__main__":
    main()
