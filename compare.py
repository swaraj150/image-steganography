import cv2
import numpy as np

def compare(path1,path2):

    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    mse = np.mean((gray1 - gray2) ** 2)
    print(f"Mean Squared Error: {mse}")

    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    print(f"Peak Signal-to-Noise Ratio: {psnr} dB")

