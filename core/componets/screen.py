import cv2
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
        
    def listCamera(self) -> list:
        self.cameras = []
        for i in range(10):
            try:
                cap = cv2.VideoCapture(i)
                if cap is not None and cap.isOpened():
                    self.cameras.append(i)
                    cap.release()
            except:
                pass

        return self.cameras
    
    def webcamSnap(self, i: list) -> list:
        photobytes = []
        for ci in i:
            filename = self.tempPath+f".{ci}.png"
            cap = cv2.VideoCapture(ci)

            if not cap.isOpened():
                continue

            ret, frame = cap.read()

            if not ret:
                continue
        
            cv2.imwrite(filename, frame)

            cap.release()

            with open(filename, "rb") as f:
                photobytes.append(f.read())

        return photobytes