import sys
import pyrealsense2 as rs
import numpy as np
import cv2


rate = int(sys.argv[1])
filename = sys.argv[2]
outfolder = sys.argv[3]

try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()
    # Tell config that we will use a recorded device from filem to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, filename)
    # Configure the pipeline to stream the depth stream
    config.enable_stream(rs.stream.color)

    # Start streaming from file
    pipeline.start(config)

    # Create opencv window to render image in
    cv2.namedWindow("Color Stream", cv2.WINDOW_AUTOSIZE)
    # cv2.resizeWindow("Depth Stream", 640*2, 480)
    
    # Create colorizer object
    colorizer = rs.colorizer()
    profile = rs.stream_profile()

    i = 0
    while True:
        frames = pipeline.wait_for_frames()

        color_frame = frames.get_color_frame()

        color_image = np.asanyarray(color_frame.get_data())
        color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        if i % rate == 0:
            outfile = f'{outfolder}/{filename[0:-4]}_{i}.png'
            cv2.imwrite(outfile, color_image)


        color_fps = color_frame.get_frame_metadata(rs.frame_metadata_value.actual_fps)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(color_image, f'FPS: {color_fps}', (10, 35), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow("Color Stream", color_image)
        key = cv2.waitKey(1)

        if key == 27 or key == 113:
            cv2.destroyAllWindows()
            break

        i += 1

finally:
    pass
