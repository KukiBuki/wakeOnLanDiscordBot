import binascii
from ipaddress import ip_address
import socket
import wakeonlan

def wakeUp() -> None:
    msg = 'send Magic Packet'
    print(msg)

    boberMac = '44.8A.5B.D0.60.87'

    wakeonlan.send_magic_packet(boberMac)

    print('Magic Packet was sent')

if __name__ == '__main__':
    wakeUp()
