# import the necessary packages
from keyClipWriter import KeyClipWriter
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import glob
import random
import math
import sys
import os

 

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default=".//",
	help=".//output_test.avi")
ap.add_argument("-b", "--buffer-size", type=int, default=50,
	help="buffer size of video clip writer")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to
# warmup
print("[INFO] warming up camera...")
#vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
timestamp = datetime.datetime.now()
file_name = "..//{}.mp4".format(timestamp.strftime("%Y%m%d-%H%M"))

path = ""
path_dir = path + "//{}".format(timestamp.strftime("%Y%m%d"))
file_list = os.listdir(path_dir)
for i in range(len(file_list)):
    name = path_dir + str(file_list[i])
    cap = cv2.VideoCapture(name)
    
    kcw = KeyClipWriter(bufSize=args["buffer_size"])
    consecFrames = 0

    # Load Yolo
    net = cv2.dnn.readNet(".//1102//yolov3_custom_last.weights", ".//1102//yolov3_custom.cfg")

    # Name custom object 
    classes = ["HIT","SHOVE","KICK"]

    # Images path


    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    fourcc = cv2.VideoWriter_fourcc(*"DIVX")
    width = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    f = None


    while True:
        
        ret,frame = cap.read()
        
        if not ret:
            break
        
        updateConsecFrames = True
        blob = cv2.dnn.blobFromImage(frame, 0.00392,(416,416), (0, 0, 0), True, crop=False)
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


                
                updateConsecFrames = confidence <= 0.98
                
                
                
                if confidence > 0.98:
                    print(confidence)
                    
                    consecFrames = 0
                    
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
                    
                    if not kcw.recording:
                        timestamp = datetime.datetime.now()
                        p = ".//test_video//{}.avi".format(
                        timestamp.strftime("%Y%m%d-%H%M%S"))
                        kcw.start(p,cv2.VideoWriter_fourcc(*"DIVX"),fps, height,width)
                        f = open(".//test_video//{}.txt".format(timestamp.strftime("%Y%m%d-%H%M%S")),"w")
                        
        
        if updateConsecFrames:
            consecFrames += 1
        # update the key frame clip buffer
        kcw.update(frame)
        # if we are recording and reached a threshold on consecutive
        # number of frames with no action, stop recording the clip
        # 
        if kcw.recording and consecFrames == args["buffer_size"]:
            kcw.finish()
            
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        font = cv2.FONT_HERSHEY_PLAIN
        
        #확인용 
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y + 30), font, 3, color, 2)
                f.write("{},{},{},{} \n".format(x,y,w,h))
                

            
        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        # if the `q` key was pressed, break from the loop
        # 
        if key == ord("q"):
            break


    cv2.destroyAllWindows()
    #vs.stop()
    cap.release()
    f.close()		
