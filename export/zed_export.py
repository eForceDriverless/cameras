import sys
import pyzed.sl as sl
import numpy as np
import cv2
from pathlib import Path
import enum

rate = int(sys.argv[1])
filename = sys.argv[2]
outfolder = sys.argv[3]

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
    # print(width, height)
    # print(zed.get_camera_fps())
    runtime = sl.RuntimeParameters()
    color = sl.Mat()
    depth = sl.Mat()

    i = 0
    key = ''
    while key != 113 and key != 27:
        err = zed.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(color)
            color_image = color.get_data()[:, :, :3]
            color_image = np.array(color_image, dtype=np.uint8)

            if i % rate == 0:
                outfile = f'{outfolder}/{filename[0:-4]}_{i}.png'
                cv2.imwrite(outfile, color_image)

            current_fps = round(zed.get_current_fps())
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(color_image, f'FPS: {current_fps}', (10, 35), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

            cv2.imshow("ZED", color_image)
            key = cv2.waitKey(1)

        else:
            key = cv2.waitKey(1)


        i += 1
    cv2.destroyAllWindows()
    zed.close()

if __name__ == "__main__":
    main()