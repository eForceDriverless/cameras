import sys
import pyrealsense2 as rs
import numpy as np
import cv2


RS = 'realsense_images/'
ZED = 'zed_images/'

color_image_rs = np.load(RS + 'color_6.npy')
depth_image_rs = np.load(RS + 'depth_6.npy')

color_image_rs = cv2.resize(color_image_rs, dsize=(640, 360), interpolation = cv2.INTER_AREA)
depth_image_rs = cv2.resize(depth_image_rs, dsize=(640, 360), interpolation = cv2.INTER_AREA)

color_image_zed = np.load(ZED + 'color_6.npy')[:, :, :3]
depth_image_zed = np.load(ZED + 'depth_6.npy')

color_image_zed = cv2.resize(color_image_zed, dsize=(640, 360), interpolation = cv2.INTER_AREA)
depth_image_zed = cv2.resize(depth_image_zed, dsize=(640, 360), interpolation = cv2.INTER_AREA)

print(color_image_zed.shape)
print(depth_image_zed.shape)
cv2.namedWindow("Depth Stream", cv2.WINDOW_NORMAL)

while True:
    combined_rs = np.hstack((color_image_rs, depth_image_rs))
    combined_zed = np.hstack((color_image_zed, depth_image_zed))

    combined = np.vstack((combined_rs, combined_zed))

    cv2.imshow("Depth Stream", combined)
    cv2.resizeWindow("Depth Stream", 1280, 720)

    key = cv2.waitKey(1)
    if key == 27 or key == 113:
        cv2.destroyAllWindows()
        break