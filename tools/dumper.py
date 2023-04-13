import json
import click
import vdf

from colorama import Fore, Back, init

init(True)

@click.command()
@click.argument("query")
@click.option('-b', '--browser', help='File of browser dump')
@click.option('-s', '--steam', help='File of steam config dump')
def dumper(browserFile, steamFile):
    pass

if __name__ == "__main__":
    dumper()