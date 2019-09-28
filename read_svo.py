import sys
import pyzed.sl as sl
import numpy as np
import cv2
from pathlib import Path
import enum



def main():

    # Get input parameters
    svo_input_path = 'zed/12_0_y.svo'

    # Specify SVO path parameter
    init_params = sl.InitParameters()
    init_params.svo_input_filename = str(svo_input_path)
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
    width_sbs = width * 2

    print(image_size.width)
    print(image_size.height)

    
    print(zed.get_camera_fps())

if __name__ == "__main__":
    main()