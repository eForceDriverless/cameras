import sys
import pyzed.sl as sl
import numpy as np
import cv2
from pathlib import Path
import enum


filename = sys.argv[1]
outfile = sys.argv[2]

def main():
    init_params = sl.InitParameters()
    init_params.svo_input_filename = filename
    init_params.svo_real_time_mode = False  # Don't convert in realtime
    init_params.coordinate_units = sl.UNIT.UNIT_MILLIMETER  # Use milliliter units (for depth measurements)

    # Create ZED objects
    zed = sl.Camera()

    # Open the SVO file specified as a parameter
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        sys.stdout.write(repr(err))
        zed.close()
        exit()
    
    # Get image size
    image_size = zed.get_resolution()
    width = image_size.width
    height = image_size.height
    # width_sbs = width * 2
    print(width, height)
    # print(zed.get_camera_fps())
    runtime = sl.RuntimeParameters()
    color = sl.Mat()
    depth = sl.Mat()

    i = 0
    key = ''
    while key != 113 and key != 27:  # for 'q' key
        err = zed.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(color)
            color_image = color.get_data()[:, :, :3]

            zed.retrieve_image(depth, sl.VIEW.VIEW_DEPTH)
            depth_image = depth.get_data()
            # depth_color_image = cv2.applyColorMap(depth_image[:, :, :3], cv2.COLORMAP_JET)

            # zed.retrieve_measure(depth, sl.MEASURE.MEASURE_DEPTH)
            # depth_image = depth.get_data()
            # print(depth_image.shape)
            # print(depth_image.dtype)

            # depth_image = np.zeros((720, 1280), dtype=float)
            # for y in range(720):
            #     for x in range(1280):
            #         # print(depth.get_value(y, x))
            #         depth_image[y, x] = depth.get_value(y, x)[1]

            # depth_color_image = cv2.applyColorMap(cv2.convertScaleAbs(depth_image), cv2.COLORMAP_JET)
            
            # print(depth_image.shape)

            gray = cv2.cvtColor(depth_image[:, :, :3], cv2.COLOR_RGB2GRAY)
            # gray = cv2.cvtColor(depth_image[:, :, :3], cv2.COLOR_RGB2HSV)[:, :, 2]


            # print(gray.dtype)
            # depth_color_image = cv2.applyColorMap(cv2.convertScaleAbs(gray, alpha=1), cv2.COLORMAP_JET)
            depth_color_image = cv2.applyColorMap(gray, cv2.COLORMAP_JET)


            # print(img_gray.shape)

            current_fps = round(zed.get_current_fps())
            font = cv2.FONT_HERSHEY_SIMPLEX
            # print(color_image.shape)
            color_image = np.array(color_image, dtype=np.uint8)
            cv2.putText(color_image, f'FPS: {current_fps}', (10, 35), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

            cv2.imshow("ZED", np.hstack((color_image, depth_color_image)))
            key = cv2.waitKey(1)

            # if i == 500:
            #     np.save(f'./zed_images/color_{outfile}.npy', color_image)
            #     np.save(f'./zed_images/depth_{outfile}.npy', depth_color_image)
            #     break
        else:
            key = cv2.waitKey(1)


        i += 1
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()