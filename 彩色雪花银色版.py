import cv2
import numpy as np
cap = cv2.VideoCapture('123.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
writer = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
colors = np.array([[0, 0, 0],[255, 255, 255],[255, 0, 0],[0, 255, 0],[0, 0, 255],[255, 255, 0],[128, 0, 128],[192, 192, 192],], dtype=np.uint8)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    expanded_colors = np.expand_dims(colors, axis=(1, 2))
    distances = np.sum((frame - expanded_colors) ** 2, axis=3)
    indices = np.argmin(distances, axis=0)
    compressed_frame = colors[indices]

    writer.write(compressed_frame)

cap.release()
writer.release()