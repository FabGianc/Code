"""
Questo script Python è un server UDP che riceve i pacchetti inviati da un client 
e risponde con il messaggio ricevuto convertito in maiuscolo. Tuttavia, 
c'è una probabilità del 40% (quando rand è minore di 4 su 10) 
che il server consideri il pacchetto perso e non risponda.
"""
# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
import random
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('', 12000))

while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    
    # Capitalize the message from the client
    message = message.upper()
    
    # If rand is less is than 4, we consider the packet lost and do not respond
    if rand < 4:
        continue
    
    # Otherwise, the server responds
    serverSocket.sendto(message, address)
