import cv2
import webbrowser
import os
img_name = input("insert image name (without format): ")
img_name = img_name + ".png"
img=cv2.imread(img_name)
det=cv2.QRCodeDetector()
val, pts, st_code=det.detectAndDecode(img)
os.system("curl " + val)

