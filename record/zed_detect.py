import sys
import numpy as np
import cv2
import pyzed.sl as sl
import time
import argparse
import tensorflow as tf

from utils.misc_utils import parse_anchors, read_class_names
from utils.nms_utils import gpu_nms
from utils.plot_utils import get_color_table, plot_one_box
from utils.data_aug import letterbox_resize

from model import yolov3

parser = argparse.ArgumentParser(description="YOLO-V3 video test procedure.")
parser.add_argument("input_video", type=str,
                    help="The path of the input video.")
parser.add_argument("--anchor_path", type=str, default="./data/yolo_anchors.txt",
                    help="The path of the anchor txt file.")
parser.add_argument("--new_size", nargs='*', type=int, default=[416, 416],
                    help="Resize the input image with `new_size`, size format: [width, height]")
parser.add_argument("--letterbox_resize", type=lambda x: (str(x).lower() == 'true'), default=True,
                    help="Whether to use the letterbox resize.")
parser.add_argument("--class_name_path", type=str, default="./data/coco.names",
                    help="The path of the class names.")
parser.add_argument("--restore_path", type=str, default="./data/darknet_weights/yolov3.ckpt",
                    help="The path of the weights to restore.")
parser.add_argument("--save_video", type=lambda x: (str(x).lower() == 'true'), default=False,
                    help="Whether to save the video detection results.")
args = parser.parse_args()

args.anchors = parse_anchors(args.anchor_path)
args.classes = read_class_names(args.class_name_path)
args.num_class = len(args.classes)

color_table = get_color_table(args.num_class)

def record():

    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.RESOLUTION_VGA
    init_params.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_NONE
    init_params.camera_fps = 30
    init_params.sdk_verbose = True
    # init_params.coordinate_units = sl.UNIT.UNIT_MILLIMETER  # Use milliliter units (for depth measurements)
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
    # depth = sl.Mat()


    config = tf.compat.v1.ConfigProto(log_device_placement=False)
    config.gpu_options.allow_growth = True
    with tf.Session(config=config) as sess:
        input_data = tf.placeholder(tf.float32, [1, args.new_size[1], args.new_size[0], 3], name='input_data')
        yolo_model = yolov3(args.num_class, args.anchors)
        with tf.variable_scope('yolov3'):
            pred_feature_maps = yolo_model.forward(input_data, False)
        pred_boxes, pred_confs, pred_probs = yolo_model.predict(pred_feature_maps)

        pred_scores = pred_confs * pred_probs

        boxes, scores, labels = gpu_nms(pred_boxes, pred_scores, args.num_class, max_boxes=200, score_thresh=0.3, nms_thresh=0.45)

        saver = tf.train.Saver()
        saver.restore(sess, args.restore_path)



        key = ''
        while key != 113 and key != 27:  # for 'q' key
            err = zed.grab(runtime)
            if err == sl.ERROR_CODE.SUCCESS:
                zed.retrieve_image(color)
                color_image = color.get_data()[:, :, :3]

                # zed.retrieve_image(depth, sl.VIEW.VIEW_DEPTH)
                # depth_image = depth.get_data()
                # depth_color_image = cv2.applyColorMap(depth_image[:, :, :3], cv2.COLORMAP_JET)


                # current_fps = round(zed.get_current_fps())
                # font = cv2.FONT_HERSHEY_SIMPLEX
                color_image = np.array(color_image, dtype=np.uint8)

                image_size = zed.get_resolution()
                width = image_size.width
                height = image_size.height

                print("A")
                # ==========================================================================

                img = cv2.resize(color_image, tuple([416, 416]))
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = np.asarray(img, np.float32)
                img = img[np.newaxis, :] / 255

                start_time = time.time()
                boxes_, scores_, labels_ = sess.run([boxes, scores, labels], feed_dict={input_data: img})
                end_time = time.time()

                # rescale the coordinates to the original image
                boxes_[:, [0, 2]] *= (width/float(416))
                boxes_[:, [1, 3]] *= (height/float(416))

                print("B")
                # time.sleep(2)

                for i in range(len(boxes_)):
                    x0, y0, x1, y1 = boxes_[i]
                    plot_one_box(color_image, [x0, y0, x1, y1], label=args.classes[labels_[i]] + ', {:.2f}%'.format(scores_[i] * 100), color=color_table[labels_[i]])
                
                cv2.putText(color_image, '{:.2f}ms'.format((end_time - start_time) * 1000), (40, 40), 0,
                            fontScale=1, color=(0, 255, 0), thickness=2)
                cv2.imshow('image', color_image)
                key = cv2.waitKey(1)

                # time.sleep(2)
                print("Still here")

                # cv2.putText(color_image, f'FPS: {current_fps}', (10, 35), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

                # cv2.imshow("ZED", np.hstack((color_image, depth_color_image)))
                # key = cv2.waitKey(1)

            else:
                key = cv2.waitKey(1)


        cv2.destroyAllWindows()


if __name__ == "__main__":
    record()