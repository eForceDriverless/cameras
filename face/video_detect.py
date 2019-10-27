import sys
import numpy as np
import cv2
import time
import tensorflow as tf
from mtcnn.mtcnn import MTCNN


def draw_image_with_boxes(image, result_list):
    for result in result_list:
        # get coordinates
        x, y, width, height = result['box']
        # draw the box
        cv2.rectangle(image, (x, y), (x+width, y+height), (255, 0, 0), 2)

        # draw the dots
        # for key, value in result['keypoints'].items():
        # 	# create and draw dot
        # 	dot = Circle(value, radius=2, color='red')
        # 	ax.add_patch(dot)




vid = cv2.VideoCapture('../export/export_1080.avi')
video_frame_cnt = int(vid.get(7))
video_width = int(vid.get(3))
video_height = int(vid.get(4))
video_fps = int(vid.get(5))

print(video_fps)

detector = MTCNN()

for i in range(video_frame_cnt):
    ret, img = vid.read()
    # height_ori, width_ori = img_ori.shape[:2]
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    start_time = time.time()
    # detect faces in the image
    faces = detector.detect_faces(img)
    draw_image_with_boxes(img, faces)
    took = round((time.time() - start_time) * 1000)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, f'Time: {took} ms', (10, 35), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow("ZED", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()