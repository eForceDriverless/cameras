#####################################################
##               Read bag from file                ##
#####################################################


# First import library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path

try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()
    # Tell config that we will use a recorded device from filem to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, './realsense/dynamic_inside_left.bag')
    # Configure the pipeline to stream the depth stream
    config.enable_stream(rs.stream.depth)
    config.enable_stream(rs.stream.color)


    # Start streaming from file
    pipeline.start(config)

    # Create opencv window to render image in
    cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
    
    # Create colorizer object
    colorizer = rs.colorizer()
    profile = rs.stream_profile()

    # fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    # fps = 30
    # video_filename = 'output.avi'
    # out = cv2.VideoWriter(video_filename, fourcc, fps, (2*1280, 720))

    # Streaming loop
    while True:
        # Get frameset of depth
        frames = pipeline.wait_for_frames()

        # Get depth frame
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        # Colorize depth frame to jet colormap
        depth_color_frame = colorizer.colorize(depth_frame)

        # Convert depth_frame to numpy array to render image in opencv
        depth_color_image = np.asanyarray(depth_color_frame.get_data())
        color_frame = np.asanyarray(color_frame.get_data())
        # print(depth_color_image.shape)
        # print(depth_frame.frame_metadata_value.actual_fps)

        combined = np.concatenate((color_frame, depth_color_image), axis=1)
        print(combined.shape)

        # print(depth_frame.get_frame_metadata(rs.frame_metadata_value.actual_fps))

        # profile = pipeline.get_active_profile()
        # depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
        # depth_intrinsics = depth_profile.get_intrinsics()
        # print(depth_intrinsics)

        # Render image in opencv window
        cv2.imshow("Depth Stream", depth_color_image)
        # out.write(combined)
        key = cv2.waitKey(1)
        # if pressed escape exit program
        if key == 27:
            # out.release()
            cv2.destroyAllWindows()
            break

finally:
    pass