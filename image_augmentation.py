# 흑백,반전,회전,블러처리,

import cv2
import sys
import glob
import numpy as np

img_files = glob.glob('.//class_1//*.JPG')

if not img_files :
    print("There are no jpg files")
    sys.exit()

cnt = len(img_files)
idx = 0


while True :
    img = cv2.imread(img_files[idx])
    
    img_flip = cv2.flip(img,1)
    
    cp = (img.shape[1]/2,img.shape[0]/2)
    random_angle = np.random.randint(0,90)
    rot = cv2.getRotationMatrix2D(cp,random_angle,0.7)
    img_rotate = cv2.warpAffine(img,rot,(0,0))

    img_blur = cv2.GaussianBlur(img,(0,0),5)


    cv2.imwrite(".//total//noback_img_flip_{}.jpg".format(idx),img_flip)
    cv2.imwrite(".//total// noback_img_blur{}.jpg".format(idx),img_blur)
    cv2.imwrite(".//total// noback_img_rotate{}.jpg".format(idx),img_rotate)

    idx += 1
    if idx >= cnt:
        break

