import cv2
import numpy as np
import glob
import random
import math
import sys

# Load Yolo
net = cv2.dnn.readNet("yolov4_custom_train_last.weights", "yolov4.cfg")

# Name custom object
classes = ["hit"]

# Images path
cap = cv2.VideoCapture("./test2.mp4")

if not cap.isOpened():
    print('open failed!')
    sys.exit()


layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

ret,img = cap.read()

img = cv2.resize(img, None, fx=0.4, fy=0.4)
height, width, channels = img.shape

img = cv2.flip(img, 1)  # 좌우 대칭 ->기본적인 카메라로 동작을 시키면  (손동작)반대방향으로 인식
gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #grayscale로 변환
gray1 = cv2.resize(gray1, (width, height), interpolation=cv2.INTER_AREA)  

# Insert here the path of your images
#random.shuffle(images_path)
# loop through all the images
while True:
    # Loading image
    ret,img = cap.read()

    if ret is None :
        break

    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape

    gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.resize(gray2, (width, height), interpolation=cv2.INTER_AREA)

    flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.1, 0) #벡터의 결과를 받음
    vx, vy = flow[..., 0], flow[..., 1]
    mag, ang = cv2.cartToPolar(vx, vy) 

    # 움직임이 충분히 큰 영역 선택
    motion_mask = np.zeros((height, width), dtype=np.uint8)
    motion_mask[mag > 2.0] = 255 #mag가 크게 움직인 부분만 출력하게, 노이즈 제거

    mx = cv2.mean(vx, mask=motion_mask)[0] #움직임 벡터의 평균을 계산,[0]으로 해야 grayscale로.
    my = cv2.mean(vy, mask=motion_mask)[0]
    m_mag = math.sqrt(mx*mx + my*my)
    label2 = '!!!!!!!!!!!!'


    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                # Object detected
                print(class_id)
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN


    print(m_mag)

    if m_mag > 5.0: #평균 벡터가 12이상인것만 다루게 함-> 충분히 움직이 큰것만 처리 위에서

        #cv2.putText(img, label2, (50 ,200), cv2.FONT_HERSHEY_SIMPLEX,
        #           5, (0, 0, 255), 3, cv2.LINE_AA)
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 2)

    cv2.imshow("Image", img)
    key = cv2.waitKey(10)
    gray1 = gray2

cap.release()
cv2.destroyAllWindows()




