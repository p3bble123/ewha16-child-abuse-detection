import sys
import cv2
import numpy as np 
import math

def openpose(frame,out,nparts): #점만 검출하는 역할


    h, w = frame.shape[:2]

    # 검출된 점 추출
    points = []
    for i in range(nparts):
        heatMap = out[0, i, :, :]
        _, conf, _, point = cv2.minMaxLoc(heatMap) #최대값 찾기(최대값만 받음)
        x = int(w * point[0] / out.shape[3])
        y = int(h * point[1] / out.shape[2])

        points.append((x, y) if conf > 0.1 else None)  # heat map threshold=0.1 #에러일 수 있는 부분 무시
    
    return points



################################### main ########################################################

cap = cv2.VideoCapture(0)
time = 1/30

if not cap.isOpened():
    print("camera not open!")
    sys.exit()

w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS) 

fourcc = cv2.VideoWriter_fourcc(*"DIVX")
delay = round(1000/fps)

# yolov3 모델 & 설정 파일
yolo = './yolo_v3/yolov3.weights'
yolo_config = './yolo_v3/yolov3.cfg'
class_labels = './yolo_v3/coco.names'
confThreshold = 0.5
nmsThreshold = 0.4

# openpose 모델 & 설정 파일
openpose = './openpose/pose_iter_440000.caffemodel' #절대경로 지정
openpose_config = './openpose/pose_deploy_linevec.prototxt' #절대경로 지정


# 네트워크 생성
yolo_net = cv2.dnn.readNet(yolo, yolo_config)
openpose_net = cv2.dnn.readNet(openpose, openpose_config)

if yolo_net.empty() or openpose_net.empty():
    print('Net open failed!')
    sys.exit()


# 클래스 이름 불러오기

classes = []
with open(class_labels, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

colors = np.random.uniform(0, 255, size=(len(classes), 3))

# 출력 레이어 이름 받아오기

layer_names = yolo_net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in yolo_net.getUnconnectedOutLayers()]


flag = [False,0,0,0,0] # True이면 openpose로 넘겨주기 위함
count = 1

while True:
    name = "./test/{}.avi".format(count)
    out = cv2.VideoWriter(name,fourcc,fps,(w,h))

    if not out.isOpened():
        print("output file open failed")
        cap.release()
        sys.exit()
    for i in range(300):
        ret, frame = cap.read()
        if not ret:
            break
        
        blob = cv2.dnn.blobFromImage(frame, 1/255., (320, 320), swapRB=True)
        yolo_net.setInput(blob)
        outs = yolo_net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []



        #detection 감지하기
        for detect in outs:
            for detection in detect:
                
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > confThreshold:
                    # 바운딩 박스 중심 좌표 & 박스 크기
                    cx = int(detection[0] * w)
                    cy = int(detection[1] * h)
                    bw = int(detection[2] * w)
                    bh = int(detection[3] * h)

                    # 바운딩 박스 좌상단 좌표
                    sx = int(cx - bw / 2)
                    sy = int(cy - bh / 2)

                    boxes.append([sx, sy, bw, bh])
                    confidences.append(float(confidence))
                    class_ids.append(int(class_id))

        # 비최대 억제
        indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)

        for j in indices:
            j = j[0]
            sx, sy, bw, bh = boxes[j]
            label = f'{classes[class_ids[j]]}: {confidences[j]:.2}'
            if 'person' in label:
                
                flag[0] = True
                flag[1] = sx
                flag[2] = sy
                flag[3] = bw
                flag[4] = bh
            color = colors[class_ids[j]]
            cv2.rectangle(frame, (sx, sy, bw, bh), color, 2)
            cv2.putText(frame, label, (sx, sy - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)

        check = 'i = {}, count = {}'.format(i,count)
        cv2.putText(frame, check, (50 ,200), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 3, cv2.LINE_AA)

        out.write(frame)
        
        cv2.imshow("frame",frame)
        cv2.waitKey(delay)


    #openpose 넘겨주기   

    if flag[0]:
        
        
        cap_openpose = cv2.VideoCapture(name)
        ret,frame = cap_openpose.read()
       
        x = flag[1]
        y = flag[3]
        h2 = flag[4]
        w2 = flag[2]

        #frame_crop = frame[y:y+h,x:x+w] #일단 좀더 늘려보고
        
        prv_pt = []
        cur_pt = []
        nparts = 8
        
        if not ret:
            print("없음")
            break


        frame = cv2.resize(frame, dsize=(480, 640), interpolation=cv2.INTER_AREA)

        blob = cv2.dnn.blobFromImage(frame, 1/255., (368, 368))
        openpose_net.setInput(blob)
        out = openpose_net.forward()  # out.shape=(1, 57, 46, 46)
        
        
        
        prv_pt = openpose(frame,out,nparts)

        while True:
            ret,frame = cap_openpose.read()
            #frame_crop = frame[y:y+h,x:x+w] #일단 좀더 늘려보기

            frame = cv2.resize(frame, dsize=(480, 640), interpolation=cv2.INTER_AREA)

            blob = cv2.dnn.blobFromImage(frame, 1/255., (368, 368))
            openpose_net.setInput(blob)
            out = openpose_net.forward()  # out.shape=(1, 57, 46, 46)
            
            cur_pt = openpose(frame,out,nparts)

            # #cur 과 prv pt 속도 계산 ->vx,vy넘겨주기
            # vx,vy = (cur_pt[1] - prv_pt[1]) / time

            # mag, ang = cv2.cartToPolar(vx, vy) #극좌표계 성분으로 바뀌면서 벡터의 크기와 각도로 계산.


            
            # label = '!!!!!!!!!!!!'
            # print("크기: ",mag)
            # if mag > 10.0: #평균 벡터가 12이상인것만 다루게 함-> 충분히 움직이 큰것만 처리 위에서

            #     cv2.putText(frame, label, (50 ,200), cv2.FONT_HERSHEY_SIMPLEX,
            #                 5, (0, 0, 255), 3, cv2.LINE_AA)

            cv2.imshow('frame', frame)

            if cv2.waitKey(1) == 27:
                break

            prv_pt = cur_pt
            
        
    if count == 6:
        break
    flag[0] = False
    count = count+1
    out.release()

cap.release()
cv2.destroyAllWindows()














