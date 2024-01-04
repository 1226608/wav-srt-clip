import cv2
import numpy as np
cap = cv2.VideoCapture("88.mp4")
writer = cv2.VideoWriter("output3.mp4", cv2.VideoWriter_fourcc(*"mp4v"), cap.get(cv2.CAP_PROP_FPS),(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
while True:
    ret, frame = cap.read()
    if not ret:
        break
    #以下三个*15,建议每次仅用其中一个,是比较好看的
    lab_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)*15
    lab_frame[:, :, 0] = (lab_frame[:, :, 0]).astype(np.uint8)#*15
    frame = cv2.cvtColor(lab_frame, cv2.COLOR_Lab2BGR)#*15
    writer.write(frame)
cap.release()
writer.release()