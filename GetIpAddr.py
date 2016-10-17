#!/usr/bin/python
import socket


def getLocalIP():
    ip = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('114.114.114.114', 80))
        ip = s.getsockname()[0]
    except:
        name = socket.gethostname()
        ip = socket.gethostbyname(name)

    return ip


if __name__ == '__main__':
    print getLocalIP()
