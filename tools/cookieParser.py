import json
import datetime

from rich import print
from rich.console import Console

class Main:
    def __init__(self) -> None:
        self.console = Console()

    def load(self):
        filepath = self.console.input("Put the cookies file [red]>>[/] ")
        self.dumps = json.load(open(filepath, "r"))

    def search(self):
        found = False
        query = self.console.input("Search site [red]>>[/] ")
        domainsufx = query.split(".")[-1]

        for browser in self.dumps:
            for cookie in self.dumps[browser]["Cookies"]:
                if query.lower() == cookie["host"].lower():
                    print(cookie)

                    if len(query.split(".")) > 2:
                        mainHost = "."+query.split(".")[-2]+f".{domainsufx}"
                        for cookie in self.dumps[browser]["Cookies"]:
                                if mainHost.lower() == cookie["host"].lower():
                                    print(cookie)
                    
                    found = True
                    break
            
        if not found:
            print("Cookie not found")
            quit(1)

    def _convertExpires(self, sqlExpires):
        expires_sec = sqlExpires // 1000000
        expires_unix = expires_sec - 11644473600
        expires_unix_microsec = (sqlExpires % 1000000) / 1000000.0
        expires_unix_with_microsec = expires_unix + expires_unix_microsec
        expires_datetime = datetime.datetime.fromtimestamp(expires_unix_with_microsec, tz=datetime.timezone.utc)
        return expires_datetime.timestamp()

    def _export(self,
                domain: str,
                expiration_date: float,
                httponly: int,
                samesite: int,
                has_expires: int,
                secure: int,
                name: str,
                value: str,
                path: str):
        
        SAME_SITE_VALUES = {
            -1: 'null',
            0: 'no_restriction',
            1: 'lax',
            2: 'strict'
        }

        if bool(has_expires):
            session = True
        else:
            session = False

        cookie_export = {
        "domain": domain,
        "hostOnly": False,
        "httpOnly": bool(httponly),
        "path": path,
        "sameSite": SAME_SITE_VALUES[samesite],
        "secure": bool(secure),
        "session": session,
        "storeId": "null",
        "name": name,
        "value": value
    }
        if expiration_date > 0:
            cookie_export["expirationDate"] = self._convertExpires(expiration_date)
        
    def run(self):
        self.load()
        self.search()

if __name__ == "__main__":
    Main().run()
    