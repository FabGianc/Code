import struct
import socket
import os
import select
import time

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2

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

def build_packet():
    type = ICMP_ECHO_REQUEST
    code = 0
    mychecksum = 0
    identifier = os.getpid() & 0xFFFF
    sequence = 1

    header = struct.pack("bbHHh", type, code, mychecksum, identifier, sequence)
    data = "abcdefghijklmnopqrstuvwxyz"  # Esempio di dati (può essere qualsiasi cosa)

    mychecksum = checksum(header + data.encode())

    header = struct.pack("bbHHh", type, code, socket.htons(mychecksum), identifier, sequence)
    packet = header + data.encode()

    return packet

def get_route(hostname):
    timeLeft = TIMEOUT
    for ttl in range(1, MAX_HOPS):
        for tries in range(TRIES):
            destAddr = socket.gethostbyname(hostname)
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))

            mySocket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)

                if whatReady[0] == []:  # Timeout
                    print(" * * * Request timed out.")
                    continue

                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                types = recvPacket[20]

                if types == 11:  # Time exceeded message
                    print(" %d %s" % (ttl, addr[0]))
                elif types == 3:  # Destination unreachable message
                    print(" %d %s" % (ttl, addr[0]))
                elif types == 0:  # Echo reply message
                    print(" %d %s" % (ttl, addr[0]))
                    return
                else:
                    print("error")
                    break

            except socket.timeout:
                continue

            finally:
                mySocket.close()

try:
    # Richiedi all'utente di inserire l'hostname da tracciare
    hostname = input("Inserisci l'hostname da tracciare: ")
    get_route(hostname)
except KeyboardInterrupt:
    print("\nInterruzione manuale dell'esecuzione.")
