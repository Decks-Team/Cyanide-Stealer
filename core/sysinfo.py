import subprocess

def runPowershell(cmd: str):
    cmdOut = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return cmdOut

def runCmd(cmd: str):
    return subprocess.getoutput(cmd)