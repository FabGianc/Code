"""
Script Python che esegue una scansione ARP su tutta la rete LAN utilizzando la libreria scapy. 
Questo script individua automaticamente l'interfaccia di rete e la subnet, 
quindi invia richieste ARP a tutti gli indirizzi IP all'interno della subnet.

"""


import scapy.all as scapy
import socket
import struct
import os
import subprocess

def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue
            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

def get_network_range():
    gateway_ip = None
    subnet_mask = None
    ip_address = None

    if os.name == 'nt':
        # For Windows
        output = subprocess.check_output("ipconfig").decode()
        print("Output from ipconfig:")
        print(output)  # Debug: Print the entire output of ipconfig
        current_interface = None
        for line in output.split("\n"):
            line = line.strip()
            if "Ethernet adapter" in line or "Scheda" in line:
                current_interface = line
            if "Indirizzo IPv4" in line:
                ip_address = line.split(":")[1].strip()
            if "Subnet mask" in line:
                subnet_mask = line.split(":")[1].strip()
            if "Gateway predefinito" in line:
                parts = line.split(":")
                if len(parts) == 2:
                    gateway_ip = parts[1].strip()
                    if gateway_ip:  # If gateway_ip is not empty
                        print(f"Found Gateway IP: {gateway_ip} for interface {current_interface}")  # Debug: Print the found Gateway IP
                        break  # Exit loop once the correct gateway is found
    else:
        # For Linux
        gateway_ip = get_default_gateway_linux()
        output = os.popen("ip -o -f inet addr show").read().split()
        subnet_mask = output[7]

    if gateway_ip is None or subnet_mask is None:
        raise ValueError(f"Could not determine the gateway IP or subnet mask. Gateway: {gateway_ip}, Subnet Mask: {subnet_mask}")
    
    return gateway_ip, subnet_mask

def ip_to_network(ip, mask):
    ip = struct.unpack('>I', socket.inet_aton(ip))[0]
    mask = struct.unpack('>I', socket.inet_aton(mask))[0]
    network = ip & mask
    return socket.inet_ntoa(struct.pack('>I', network))

def get_cidr_notation(ip, mask):
    mask = struct.unpack('>I', socket.inet_aton(mask))[0]
    cidr = 32
    while(mask & 1 == 0):
        cidr -= 1
        mask >>= 1
    return f"{ip}/{cidr}"

def scan(network):
    arp_request = scapy.ARP(pdst=network)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    print(f"Sending ARP requests to network: {network}")
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=10, retry=3, verbose=True)

    devices = []
    for sent, received in answered_list:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices

def main():
    try:
        gateway_ip, subnet_mask = get_network_range()
        print(f"Gateway IP: {gateway_ip}")
        print(f"Subnet Mask: {subnet_mask}")

        network_ip = ip_to_network(gateway_ip, subnet_mask)
        print(f"Network IP: {network_ip}")

        network = get_cidr_notation(network_ip, subnet_mask)
        print(f"Network CIDR: {network}")
        
        print(f"Scanning network: {network}")
        devices = scan(network)
        
        print("Available devices in the network:")
        print("IP Address\tMAC Address")
        print("-----------------------------------")
        for device in devices:
            print(f"{device['ip']}\t{device['mac']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
