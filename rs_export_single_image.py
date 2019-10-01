import sys
import pyrealsense2 as rs
import numpy as np
import cv2


filename = sys.argv[1]
outfile = sys.argv[2]

try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()
    # Tell config that we will use a recorded device from filem to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, filename)
    # Configure the pipeline to stream the depth stream
    config.enable_stream(rs.stream.depth)
    config.enable_stream(rs.stream.color)

    # Start streaming from file
    pipeline.start(config)

    # Create opencv window to render image in
    cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
    # cv2.resizeWindow("Depth Stream", 640*2, 480)
    
    # Create colorizer object
    colorizer = rs.colorizer()
    profile = rs.stream_profile()

    # fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    # fps = 30
    # video_filename = 'output.avi'
    # out = cv2.VideoWriter(video_filename, fourcc, fps, (2*1280, 720))
    i = 0
    # Streaming loop
    while True:
        # Get frameset of depth
        frames = pipeline.wait_for_frames()

        # Get depth frame
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        # Colorize depth frame to jet colormap
        depth_color_frame = colorizer.colorize(depth_frame)
        # depth_color_frame = depth_frame


        # Convert depth_frame to numpy array to render image in opencv
        # print(np.asanyarray(depth_color_frame.get_data()).shape)
        # print(np.asanyarray(depth_color_frame.get_data()).dtype)

        depth_color_image = np.asanyarray(depth_color_frame.get_data())
        # depth_color_image = cv2.applyColorMap(cv2.convertScaleAbs(depth_color_image, alpha=0.03), cv2.COLORMAP_JET)
        color_image = np.asanyarray(color_frame.get_data())
        color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        # print(color_image.shape)
        # print(depth_color_image.shape)

        # print(color_image.shape)
        # print(color_image.dtype)


        # print(depth_color_image.shape)
        # print(depth_color_image.shape)
        # print(depth_frame.frame_metadata_value.actual_fps)

        # combined = np.concatenate((color_image, depth_color_image), axis=1)
        # print(combined.shape)

        color_fps = color_frame.get_frame_metadata(rs.frame_metadata_value.actual_fps)
        depth_fps = depth_frame.get_frame_metadata(rs.frame_metadata_value.actual_fps)


        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(color_image, f'FPS: {color_fps}', (10, 35), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(depth_color_image, f'FPS: {depth_fps}', (10, 35), font, 1, (0, 0, 255), 2, cv2.LINE_AA)


        color_image = cv2.resize(color_image, dsize=(640, 360), interpolation = cv2.INTER_AREA)
        depth_color_image = cv2.resize(depth_color_image, dsize=(640, 360), interpolation = cv2.INTER_AREA)


        # profile = pipeline.get_active_profile()
        # depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
        # depth_intrinsics = depth_profile.get_intrinsics()
        # print(depth_intrinsics)

        # Render image in opencv window
        cv2.imshow("Depth Stream", np.hstack((color_image, depth_color_image)))
        # out.write(combined)
        # key = cv2.waitKey(1)

        # if i == 50:
        #     np.save(f'./realsense_images/color_{outfile}.npy', color_image)
        #     np.save(f'./realsense_images/depth_{outfile}.npy', depth_color_image)
        #     cv2.destroyAllWindows()
        #     break
        key = cv2.waitKey(1)

        # if pressed escape exit program
        # if key == 112: # p
            # pass
            # np.save(f'./realsense_images/color_{outfile}.npy', color_image)
            # np.save(f'./realsense_images/depth_{outfile}.npy', depth_color_image)
        if key == 27 or key == 113:
            # out.release()
            cv2.destroyAllWindows()
            break

        i += 1

finally:
    pass

# print(i)