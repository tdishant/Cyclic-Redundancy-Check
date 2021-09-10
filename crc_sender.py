import socket
import random

def crc_sender(clientsocket, address):
    
    choice = 'y'
    
    while (choice == 'y'):
        data = input("Enter the data you want to send : ")
        crc_generator = input("Enter the CRC Generator : ")
        
        print("Sending the CRC Generator " + crc_generator + " to the receiver...")
        clientsocket.send(crc_generator.encode())
        print(clientsocket.recv(1024).decode())
        
        no_of_ones = crc_generator.count('1')
        
        modified_data = data
        
        for i in range(no_of_ones):
            modified_data += '0' 
        
        while(len(modified_data) >= len(crc_generator)):
            
            list1 = list(modified_data)  
            
            for i in range(len(crc_generator)):
                list1[i] = str(int(list1[i]) ^ int(crc_generator[i]))
            
            modified_data = "".join(list1)
            modified_data = modified_data.lstrip('0')
        
        modified_data = modified_data.zfill(len(crc_generator))
        
        actual_crc = modified_data
        
        start = len(actual_crc) - no_of_ones
        actual_crc = actual_crc[start:]
        
        actual_data = data
        
        ch = input("Do you want to corrupt the data ? (y/n) : ")
        
        if(ch == 'y'):
            index = random.randint(0, len(data) - 1)
            list1 = list(actual_data)
            
            if(list1[index] == '0'):
                list1[index] = '1'
            else:
                list1[index] = '0'
            
            actual_data = "".join(list1)
        
        actual_data = actual_data + actual_crc
        
        print("Sending the Data " + actual_data + " to the receiver...")
        clientsocket.send(actual_data.encode())
        print(clientsocket.recv(1024).decode())
        
        print(clientsocket.recv(1024).decode())
        
        choice = input("Do you want to send more data ? (y/n) : ")
    
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 8000

serversocket.bind((host, port))

serversocket.listen(5)
print ('Sender ready and is listening')

while True:

    #to accept all incoming connections
    clientsocket, address = serversocket.accept()
    print("Receiver "+str(address)+" connected")
    #create a different thread for every 
    #incoming connection 
    crc_sender(clientsocket, address)
    break
    