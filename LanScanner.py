""""
Programma che verifica lo stato della LAN, elenca gli host e fornisce informazioni 
su indirizzi IP e porte aperte. 
Esempio base che usa il modulo socket di Python per verificare le porte aperte degli host.
"""

import socket
import threading

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, port))
        print(f"[*] Port {port} on {ip} is open")
    except (socket.timeout, socket.error):
        pass
    finally:
        sock.close()

def scan_host(ip, ports):
    print(f"Scanning host {ip}")
    for port in ports:
        thread = threading.Thread(target=scan_port, args=(ip, port))
        thread.start()

def main():
    target_subnet = "192.168.1"
    ports_to_scan = range(1, 1025)
    threads = []

    for i in range(1, 255):
        target_ip = f"{target_subnet}.{i}"
        thread = threading.Thread(target=scan_host, args=(target_ip, ports_to_scan))
        threads.append(thread)
        thread.start()

    # Attendere che tutti i thread abbiano finito
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()

