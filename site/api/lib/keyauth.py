import requests
import json

class Keyauth:
    def __init__(self, app_name: str, ownerid: str) -> None:
        self.app_name = app_name
        self.ownerid = ownerid

    def init(self):
        r=requests.get(f"https://keyauth.win/api/1.1/?type=init&ver=1.0&name={self.app_name}&ownerid={self.ownerid}")
        j=json.loads(r.text)
        session_id=j["sessionid"]
        self.session_id = session_id
        return session_id

    def register(self, username, password, key, hwid):
        r=requests.get(f"https://keyauth.win/api/1.1/?type=register&username={username}&pass={password}&key={key}&hwid={hwid}&sessionid={self.session_id}&name={self.app_name}&ownerid={self.ownerid}")
        j=json.loads(r.text)
        return j

    def login(self, username, password, hwid):
        r=requests.get(f"https://keyauth.win/api/1.1/?type=login&username={username}&pass={password}&hwid={hwid}&sessionid={self.session_id}&name={self.app_name}&ownerid={self.ownerid}")
        j=json.loads(r.text)
        return j

    def login_key(self, key, hwid):
        r=requests.get(f"https://keyauth.win/api/1.1/?type=license&key={key}&hwid={hwid}&sessionid={self.session_id}&name={self.app_name}&ownerid={self.ownerid}")
        j=json.load(r.text)
        return j
    def check_blacklist(self, hwid):
        r=requests.get(f"https://keyauth.win/api/1.2/?type=checkblacklist&name={self.app_name}&ownerid={self.ownerid}&sessionid={self.session_id}&hwid={hwid}")
        j=json.loads(r.text)
        return j
    def ban(self):
        r=requests.get(f"https://keyauth.win/api/1.2/?type=ban&sessionid={self.session_id}&name={self.app_name}&ownerid={self.ownerid}")
        j=json.loads(r.text)
        return j
    
    def fetch_online(self):
        r=requests.get(f"https://keyauth.win/api/1.2/?type=fetchOnline&name={self.app_name}&ownerid={self.ownerid}&sessionid={self.session_id}")
        j=json.loads(r.text)
        return j

class Seller:
    def __init__(self, seller_key) -> None:
        self.seller_key = seller_key

    def create_license(self, expiry: str, mask: str, amount: str):
        verify = requests.get(f"https://keyauth.win/api/seller/?sellerkey={self.seller_key}&type=verify&key={mask}").json()
        exist=verify["success"]
        if exist == False:
            r = requests.get(f"https://keyauth.win/api/seller/?sellerkey={self.seller_key}&type=add&expiry={expiry}&mask={mask}&amount={amount}&format=json").text
            return r
        else:
            return "this key already exists"
    
    def delete_license(self, key: str):
        r = requests.get(f"https://keyauth.win/api/seller/?sellerkey={self.seller_key}&type=del&key={key}&userToo=0").text
        return r
    def reset_hwid(self,user: str):
        r = requests.get(f"https://keyauth.win/api/seller/?sellerkey={self.seller_key}&type=resetuser&user={user}").text
        return r
    
    def ban_user(self, user: str, reason: str):
        r=requests.get(f"https://keyauth.win/api/seller/?sellerkey={self.seller_key}&type=banuser&user={user}&reason={reason}").text
        return r
    
    def unban_user(self, user: str):
        r=requests.get(f"https://keyauth.win/api/seller/?sellerkey={self.seller_key}&type=unbanuser&user={user}").text
        return r
    
    def change_passwd(self,user: str, passwd: str):
        r = requests.get(f"https://keyauth.win/api/seller/?sellerkey={self.seller_key}&type=resetpw&user={user}&passwd={passwd}").json()
        return r