import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 8000
s.connect((host,port))

while True:
    
    crc_generator = s.recv(1024).decode()
    print("Received CRC Generator : " + crc_generator)
    msg = "Receiver got the CRC Generator : " + crc_generator
    s.send(msg.encode())
    
    actual_data = s.recv(1024).decode()
    print("Received Data : " + actual_data)
    msg = "Receiver Got the Data : " + actual_data
    s.send(msg.encode())
    
    print("Checking if the Data is corrupted or not...")
    
    while(len(actual_data) >= len(crc_generator)):
         
         list1 = list(actual_data)  
         
         for i in range(len(crc_generator)):
             list1[i] = str(int(list1[i]) ^ int(crc_generator[i]))
         
         actual_data = "".join(list1)
         actual_data = actual_data.lstrip('0')
    
    actual_data = actual_data.zfill(len(crc_generator))
        
    remainder = actual_data

    if(int(remainder) != 0):
        print("DATA CORRUPTED")
        msg = "The Data got corrupted... Please send the data again..."
        s.send(msg.encode())
    else:
        print("DATA NOT CORRUPTED")
        msg = "The Data was not corrupted... Please send the new data..."
        s.send(msg.encode())     
   
s.close()