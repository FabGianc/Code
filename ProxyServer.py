from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage: "python ProxyServer.py server_ip"\n[server_ip: It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# Fill in start.
# Define the port number to listen on
port = 8888  # You can change this port number as needed
tcpSerSock.bind(('', port))

# Start listening for incoming connections
tcpSerSock.listen(5)
# Fill in end.

while True:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024).decode()

    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = False
    filetouse = "/" + filename
    print(filetouse)

    try:
        # Check whether the file exists in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = True

        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        tcpCliSock.send("Content-Type: text/html\r\n")
        # Fill in start.
        for data in outputdata:
            tcpCliSock.send(data.encode())
        # Fill in end.
        print('Read from cache')

    except IOError:
        if not fileExist:
            # Create a socket on the proxy server
            c = socket(AF_INET, SOCK_STREAM)

            # Extract the host name from the filename
            hostn = filename.replace("www.", "", 1)
            print(hostn)

            try:
                # Connect to the socket to port 80
                c.connect((hostn, 80))

                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('r', 0)
                fileobj.write(f"GET http://{filename} HTTP/1.0\n\n")

                # Read the response into a buffer
                response = fileobj.readlines()

                # Create a new file in the cache for the requested file
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename, "w")
                # Fill in start.
                for data in response:
                    tcpCliSock.send(data.encode())
                    tmpFile.write(data)
                # Fill in end.
            except Exception as e:
                print("Illegal request or unable to connect:", e)

    # Close the client and the server sockets
    tcpCliSock.close()

tcpSerSock.close()
