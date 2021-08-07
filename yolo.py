import cv2
import numpy as np
import glob
import random
import math
import sys

# Load Yolo
net = cv2.dnn.readNet("yolov3_custom_last.weights", "yolov3_custom.cfg")

# Name custom object
classes = ["hit"]

# Images path
cap = cv2.VideoCapture("./data/test3.mp4")

if not cap.isOpened():
    print('open failed!')
    sys.exit()


layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

ret,img = cap.read()
height, width, channels = img.shape

# Insert here the path of your images
#random.shuffle(images_path)
# loop through all the images

crops = []
while True:
    # Loading image
    ret,img = cap.read()

    if not ret:
        break


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

    
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 2)
            crop = img[y:y+h,x:x+w]
            crops.append(crop)


    cv2.imshow("Image", img)
    key = cv2.waitKey(10)
    if key == 27:
        break
    

img = crops[0]

height, width, channels = img.shape


gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #grayscale로 변환
gray1 = cv2.resize(gray1, (width, height), interpolation=cv2.INTER_AREA) 

for i in range(1,len(crops)):
    img = crops[i]

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

    print(m_mag)
    if m_mag > 3.0:
         cv2.putText(img, label2, (10,30 ), font, 3, (0,0,255), 2)


    cv2.imshow('crop',img)
    if cv2.waitKey(1000) == 27:
        break

    gray1 = gray2


cap.release()
cv2.destroyAllWindows()