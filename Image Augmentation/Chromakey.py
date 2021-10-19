import cv2
import sys
import glob

#크로마키 이용한 데이터 증식 코드
img_files = glob.glob('.//class1//*.jpg')
bg_files = glob.glob('.//background//*.jpg')

if not img_files or not bg_files :
    print("There are no jpg files")
    sys.exit()  

cnt = len(img_files)
bg_cnt = len(bg_files)
idx = 0
count = 0

while True:
    img = cv2.imread(img_files[idx])
    h,w = img.shape[:2]

    if img is None:
        print('Image load failed')
        break
    
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,(30,150,0),(90,255,255))

    for i in range(bg_cnt):
        back = cv2.imread(bg_files[i])
        back = cv2.resize(back, dsize=(w, h), interpolation=cv2.INTER_AREA)
        cv2.copyTo(back,mask,img)

        cv2.imshow("img",img)
        cv2.imwrite(".//output// {}.jpg".format(count),img)
        cv2.waitKey(1)
        count += 1
        

    idx += 1
    if idx >= cnt:
        break

cv2.destroyAllWindows()