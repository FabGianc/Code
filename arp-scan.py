"""
Script Python che utilizza il modulo scapy per eseguire una scansione ARP. 
Questo script invia richieste ARP per ogni indirizzo IP in una determinata rete 
e raccoglie le risposte.

pip install scapy

"""

from scapy.all import ARP, Ether, srp
import sys

def arp_scan(network):
    # Create an ARP request packet
    arp_request = ARP(pdst=network)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    # Send the packet and capture the response
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    devices = []
    for sent, received in answered_list:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python arp_scan.py <network>")
        print("Example: python arp_scan.py 192.168.1.0/24")
        sys.exit(1)

    network = sys.argv[1]
    devices = arp_scan(network)
    print("Available devices in the network:")
    print("IP Address\tMAC Address")
    print("-----------------------------------")
    for device in devices:
        print(f"{device['ip']}\t{device['mac']}")
