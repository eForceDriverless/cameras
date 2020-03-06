import sys
import time
import numpy as np
import cv2
import pyrealsense2 as rs
import pyzed.sl as sl
# TODO: Split this enormous while loop into functions

# Create a pipeline
ctx = rs.context()

# Get devices and their SN
devices = ctx.devices
devices_sn = [x.get_info(rs.camera_info.serial_number) for x in devices]

# Hack in action
[x.hardware_reset() for x in devices]

# Now sleep and wait for startup, TODO: think of better way isn't working 100%
time.sleep(5)

# Start Realsense and set incoming streams
pipeline1 = rs.pipeline()
config1 = rs.config()
# Another hack if i put here devices_sn[0] it isn't working.
# Only know fact is that devices_sn[1] has lower sn number than devices_sn TODO: Fix not in hacky way
config1.enable_device(devices_sn[1])
config1.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 15)
config1.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
profile1 = pipeline1.start(config1)

# Same as before
pipeline2 = rs.pipeline()
config2 = rs.config()
config2.enable_device(devices_sn[0])
config2.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 15)
config2.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
profile2 = pipeline2.start(config2)

try:
    # Init ZED with 1920x1080 and 30FPS, no depth data
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.RESOLUTION_HD1080
    init_params.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_NONE
    init_params.camera_fps = 30
    init_params.sdk_verbose = True
    # init_params.coordinate_units = sl.UNIT.UNIT_MILLIMETER  # Use milliliter units (for depth measurements)

    # Create colorizer object fro Realsense
    colorizer = rs.colorizer()
    profile = rs.stream_profile()

    # TODO: Remove FPS for Realsese, or at least redo
    counter = 0
    start = time.time()
    prev_fps = 0

    # Create ZED objects
    zed = sl.Camera()

    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        sys.stdout.write(repr(err))
        zed.close()
        exit()
    runtime = sl.RuntimeParameters()
    color = sl.Mat()

    # Streaming loop
    while True:
        # Realsense
        # Get frameset of depth
        frames1 = pipeline1.wait_for_frames()
        frames2 = pipeline2.wait_for_frames()
        # Get color frame
        color_frame1 = frames1.get_color_frame()
        color_frame2 = frames2.get_color_frame()

        # Get depth frame
        depth_frame1 = frames1.get_depth_frame()
        depth_frame2 = frames2.get_depth_frame()

        # Colorize depth frame to jet colormap
        depth_color_frame1 = colorizer.colorize(depth_frame1)
        depth_color_frame2 = colorizer.colorize(depth_frame2)

        # Convert Realsense data to NP data (compatible with OpenCV)
        depth_color_image1 = np.asanyarray(depth_color_frame1.get_data())
        depth_color_image2 = np.asanyarray(depth_color_frame2.get_data())

        color_image1 = np.asanyarray(color_frame1.get_data())
        color_image1 = cv2.cvtColor(color_image1, cv2.COLOR_BGR2RGB)

        color_image2 = np.asanyarray(color_frame2.get_data())
        color_image2 = cv2.cvtColor(color_image2, cv2.COLOR_BGR2RGB)

        color1_fps = color_frame1.get_frame_metadata(rs.frame_metadata_value.actual_fps)
        color2_fps = color_frame2.get_frame_metadata(rs.frame_metadata_value.actual_fps)

        # More FPS things
        curr = time.time()
        if curr - start > 1:
            prev_fps = counter
            color_fps = counter
            start = curr
            counter = 0
        else:
            color_fps = prev_fps

        counter += 1

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(color_image1, f'FPS: {color_fps}', (10, 35), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(color_image2, f'FPS: {color_fps}', (10, 35), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

        """Zed"""
        color_image = []
        err = zed.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(color)
            color_image = color.get_data()[:, :, :3]

        color_image = np.array(color_image, dtype=np.uint8)

        """Render"""
        cv2.imshow("Realsense", np.vstack((np.hstack((color_image1, color_image2)),
                                           (np.hstack((depth_color_image1, depth_color_image2))))))
        cv2.imshow("ZED", color_image)
        # out.write(combined)
        # key = cv2.waitKey(1)

        key = cv2.waitKey(1)

        if key == 27 or key == 113:
            # out.release()
            cv2.destroyAllWindows()
            break
except Exception as e:
    print(e)
finally:
    pass
