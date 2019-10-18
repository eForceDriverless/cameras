import time
import numpy as np
import cv2
import pyrealsense2 as rs
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

# create face detector
detector = MTCNN()


# Create a pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
profile = pipeline.start(config)
# cv2.namedWindow("Stream", cv2.WINDOW_AUTOSIZE)

try:
    # Create opencv window to render image in
    # cv2.resizeWindow("Depth Stream", 640*2, 480)
    
    # Create colorizer object
    colorizer = rs.colorizer()
    profile = rs.stream_profile()

    counter = 0
    start = time.time()
    prev_fps = 0
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
        print(color_image.dtype)


        # print(depth_color_image.shape)
        # print(depth_color_image.shape)
        # print(depth_frame.frame_metadata_value.actual_fps)

        # combined = np.concatenate((color_image, depth_color_image), axis=1)
        # print(combined.shape)

        color_fps = color_frame.get_frame_metadata(rs.frame_metadata_value.actual_fps)
        depth_fps = depth_frame.get_frame_metadata(rs.frame_metadata_value.actual_fps)


        # detect faces in the image
        faces = detector.detect_faces(color_image)
        draw_image_with_boxes(color_image, faces)


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
        cv2.putText(color_image, f'FPS: {color_fps}', (10, 35), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(depth_color_image, f'FPS: {depth_fps}', (10, 35), font, 1, (0, 0, 255), 2, cv2.LINE_AA)


        # color_image = cv2.resize(color_image, dsize=(640, 360), interpolation = cv2.INTER_AREA)
        # depth_color_image = cv2.resize(depth_color_image, dsize=(640, 360), interpolation = cv2.INTER_AREA)


        # profile = pipeline.get_active_profile()
        # depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
        # depth_intrinsics = depth_profile.get_intrinsics()
        # print(depth_intrinsics)

        # Render image in opencv window
        cv2.imshow("Stream", np.hstack((color_image, depth_color_image)))
        # out.write(combined)
        # key = cv2.waitKey(1)

        key = cv2.waitKey(1)

        if key == 27 or key == 113:
            # out.release()
            cv2.destroyAllWindows()
            break

finally:
    pass