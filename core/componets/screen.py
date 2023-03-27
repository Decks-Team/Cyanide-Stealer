import pyautogui
import os

from core.componets import utils

class Screen:
    def __init__(self) -> None:
        self.tempname = utils.random_string.get(10)
        self.tempPath = os.path.join(os.environ["TEMP"], self.tempname+".cy")

    def screenshot(self) -> bytes:
        filename = self.tempPath+".png"
        myscreenshot = pyautogui.screenshot()
        myscreenshot.save(filename)
        with open(filename, "rb") as f:
            photobytes = f.read()

        os.remove(filename)
        return photobytes