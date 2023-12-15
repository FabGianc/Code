from socket import *

msg = "\r\nI love computer networks!"
endmsg = "\r\n.\r\n"

# Scegli un server di posta (ad esempio il server di posta di Google) 
# e chiamalo server di posta
mailserver = 'smtp.gmail.com'  # Inserisci il server di posta SMTP desiderato

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 587))  # Connect to the mail server using its appropriate port

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'EHLO Alice\r\n'  # Using EHLO instead of HELO for extended SMTP
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send STARTTLS command to enable encryption
starttlsCommand = 'STARTTLS\r\n'
clientSocket.send(starttlsCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '220':
    print('220 reply not received from server.')

# Start TLS encryption
import ssl
clientSocket = ssl.wrap_socket(clientSocket)

# Send AUTH LOGIN command for authentication if required
authLoginCommand = 'AUTH LOGIN\r\n'
clientSocket.send(authLoginCommand.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '334':
    print('334 reply not received from server.')

# Add your base64 encoded username and password
base64_username = "your_base64_encoded_username"
base64_password = "your_base64_encoded_password"

clientSocket.send(base64_username.encode() + b'\r\n')
recv4 = clientSocket.recv(1024).decode()
print(recv4)
if recv4[:3] != '334':
    print('334 reply not received from server.')

clientSocket.send(base64_password.encode() + b'\r\n')
recv5 = clientSocket.recv(1024).decode()
print(recv5)
if recv5[:3] != '235':
    print('235 reply not received from server.')

# Send MAIL FROM command and print server response.
mailFromCommand = 'MAIL FROM: <your_email@gmail.com>\r\n'  # Use your own Gmail address here
clientSocket.send(mailFromCommand.encode())
recv6 = clientSocket.recv(1024).decode()
print(recv6)
if recv6[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.
rcptToCommand = 'RCPT TO: <recipient@example.com>\r\n'  # Use the recipient's email address
clientSocket.send(rcptToCommand.encode())
recv7 = clientSocket.recv(1024).decode()
print(recv7)
if recv7[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
recv8 = clientSocket.recv(1024).decode()
print(recv8)
if recv8[:3] != '354':
    print('354 reply not received from server.')

# Send message data.
clientSocket.send(msg.encode())

# Message ends with a single period.
clientSocket.send(endmsg.encode())
recv9 = clientSocket.recv(1024).decode()
print(recv9)
if recv9[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
recv10 = clientSocket.recv(1024).decode()
print(recv10)
if recv10[:3] != '221':
    print('221 reply not received from server.')

# Close the client socket
clientSocket.close()
