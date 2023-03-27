import json
import click
import vdf

from colorama import Fore, Back, init

init(True)

@click.command()
@click.option('-b', '--browser', help='File of browser dump')
@click.option('-s', '--steam', help='File of steam config dump')
def dumper(browserFile, steamFile):
    if browserFile:
        with open(browserFile, "r") as f:
            browserDump = json.load(f)
        
        for browser in browserDump:
            keys = browserDump[browser].keys()
            print(f"{'='*20} {Back.YELLOW}{browser}{Back.RESET} {'='*20}")
            for key in keys:
                print(f"[{Fore.RED}{key}{Fore.RESET}]")
                for site in browserDump[browser][key].keys():
                        username = browserDump[browser][key][site]['username']
                        password = browserDump[browser][key][site]['password']
                        print(f"{site} {username}:{password}")

if __name__ == "__main__":
    dumper()