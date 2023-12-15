"""
Script Python per inviare e ricevere richieste di ping ICMP (Echo Requests). 
La funzione receiveOnePing recupera l'intestazione ICMP dal pacchetto ricevuto, 
verificando se si tratta di una risposta Echo in base alla struttura effettiva dei pacchetti ICMP ricevuti, 
"""

from socket import *
import os
import sys
import struct
import time
import select
import binascii
from socket import htons

ICMP_ECHO_REQUEST = 8

def checksum(packet):
    csum = 0
    countTo = (len(packet) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = packet[count+1] * 256 + packet[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(packet):
        csum = csum + packet[len(packet) - 1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff

    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []:  # Timeout
            return "Richiesta scaduta."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        # Recupero l'intestazione ICMP dal pacchetto IP
        header = recPacket[20:28]  # Supponendo che l'intestazione ICMP sia di 8 byte (dalla posizione 20 alla 28)

        # Scompatto l'intestazione ICMP
        tipo, codice, checksum, packetID, sequenza = struct.unpack("bbHHh", header)

        if tipo == 0:  # Echo Reply
            bytes = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytes])[0]
            return f"Risposta da {destAddr}: bytes={len(recPacket)} tempo={timeReceived - timeSent:.7f}ms"

        # Restituisco un messaggio riguardante il pacchetto ICMP ricevuto
        return f"Richiesta ricevuta da {addr[0]}: tipo={tipo} codice={codice}"

        # Continuo il controllo del timeout
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Richiesta scaduta."

def sendOnePing(mySocket, destAddr, ID):
    # Header del pacchetto ICMP
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, ID, 1)
    data = struct.pack("d", time.time())

    # Calcolo il checksum su header + data
    myChecksum = checksum(header + data)

    # Header con checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, htons(myChecksum), ID, 1)
    packet = header + data

    # Invio il pacchetto
    mySocket.sendto(packet, (destAddr, 1))

def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")

    # Creo un socket ICMP
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF  # Identificatore univoco

    # Invio il pacchetto ICMP
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay

def ping(host, timeout=1):
    dest = gethostbyname(host)
    print(f"PING {host} ({dest})")
    while True:
        delay = doOnePing(dest, timeout)
        print(delay)
        time.sleep(1)  # Aspetto un secondo prima di inviare il successivo ping

# Esecuzione del ping
dest = input("Inserisci l'indirizzo IP a cui inviare il ping: ")
ping(dest)  
