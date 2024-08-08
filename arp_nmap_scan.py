"""
Script Python che integra nmap per eseguire una scansione ARP e raccogliere i risultati. 
Lo script esegue il comando nmap, analizza l'output e visualizza gli indirizzi IP e MAC 
dei dispositivi trovati nella rete.


"""

import subprocess

def scan_with_nmap(network):
    print(f"Scanning network: {network} with nmap")
    result = subprocess.run(['nmap', '-sn', '-PR', network], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return []

    devices = []
    current_device = {}
    for line in result.stdout.split('\n'):
        if 'Nmap scan report for' in line:
            if current_device:
                devices.append(current_device)
            current_device = {'ip': line.split(' ')[-1], 'mac': 'Unknown', 'vendor': 'Unknown'}
        elif 'MAC Address:' in line:
            parts = line.split(' ')
            if len(parts) > 2:
                current_device['mac'] = parts[2]
                if len(parts) > 3:
                    current_device['vendor'] = ' '.join(parts[3:]).strip('()')
    if current_device:
        devices.append(current_device)

    return devices

def main():
    network=input('Inserisci la rete sulla quale effettuare la scansione ARP (es 192.168.1.0/24): ')
    # network = '192.168.1.0/24'
    devices = scan_with_nmap(network)
    
    print("Available devices in the network:")
    print("{:<16} {:<18} {}".format("IP Address", "MAC Address", "Vendor"))
    print("----------------------------------------------------------")
    for device in devices:
        print("{:<16} {:<18} {}".format(device['ip'], device['mac'], device['vendor']))

if __name__ == "__main__":
    main()
