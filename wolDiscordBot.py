import binascii
import socket

def wakeUp():
    msg = 'send Magic Packet'
    print(msg)

    mac='D8:BB:C1:52:F5:6A'
    macbytes = binascii.unhexlify('D8BBC152F56A')

    magic_packet = bytes([255, 255, 255, 255, 255, 255]) + macbytes * 16

    print(magic_packet)
    so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    so.setblocking(False)
    so.settimeout(3)
    print('before connection')

    so.sendto(magic_packet, ('192.168.0.143', 9))
    print('packet send')
    so.close

    print('Magic Packet was sent')