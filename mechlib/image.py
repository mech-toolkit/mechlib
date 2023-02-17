import cv2
import urllib.request
from pathlib import Path
import numpy as np
import time


def get_bot_img(bot):
    req = urllib.request.urlopen(f"http://{bot}/capture")
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)  # 'Load it as it is'
    return img


def save_image(bot_image):
    fname = (
        str(Path.home() / "received3")
        + "/rwM"
        + time.strftime("%Y%m%d-%H%M%S")
        + ".jpg"
    )
    cv2.imwrite(fname, bot_image)
    print(f"Saved img: {fname}")
