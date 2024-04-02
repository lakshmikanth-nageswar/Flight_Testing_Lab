# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 14:39:20 2024

@author: maris
"""

import cv2
import time
import geocoder
import os

def apply_mars_filter_to_frame(frame):
    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Enhance red channel
    b, g, r = cv2.split(frame)
    enhanced_r = cv2.multiply(r, 1.5)

    # Merge the enhanced red channel with the grayscale frame
    merged_frame = cv2.merge([gray_frame, gray_frame, enhanced_r])

    return merged_frame

def detectPotholeonFrame(frame, g, result_path, i, b):
    # reading label name from obj.names file
    class_name = []
    with open(os.path.join("project_files", 'obj.names'), 'r') as f:
        class_name = [cname.strip() for cname in f.readlines()]

    # importing model weights and config file
    # defining the model parameters
    net1 = cv2.dnn.readNet('project_files/yolov4_tiny.weights', 'project_files/yolov4_tiny.cfg')
    net1.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net1.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
    model1 = cv2.dnn_DetectionModel(net1)
    model1.setInputParams(size=(640, 480), scale=1 / 255, swapRB=True)

    # analysis the frame with detection model
    classes, scores, boxes = model1.detect(frame, 0.5, 0.4)
    for (classid, score, box) in zip(classes, scores, boxes):
        label = "Pothole"
        x, y, w, h = box
        recarea = w * h
        area = frame.shape[1] * frame.shape[0]
        # drawing detection boxes on frame for detected potholes and saving coordinates txt and photo
        if (len(scores) != 0 and scores[0] >= 0.7):
            if ((recarea / area) <= 0.1 and box[1] < 600):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                cv2.putText(frame, "%" + str(round(scores[0] * 100, 2)) + " " + label, (box[0], box[1] - 10),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                if (i == 0):
                    cv2.imwrite(os.path.join(result_path, 'pothole' + str(i) + '.jpg'), frame)
                    with open(os.path.join(result_path, 'pothole' + str(i) + '.txt'), 'w') as f:
                        f.write(str(g.latlng))
                        i = i + 1
                if (i != 0):
                    if ((time.time() - b) >= 2):
                        cv2.imwrite(os.path.join(result_path, 'pothole' + str(i) + '.jpg'), frame)
                        with open(os.path.join(result_path, 'pothole' + str(i) + '.txt'), 'w') as f:
                            f.write(str(g.latlng))
                            b = time.time()
                            i = i + 1
    return frame, i, b

def apply_mars_filter_to_video(video_path, output_path):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    # Get the frame width and height
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' codec for MP4 format
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height))

    # defining parameters for result saving and get coordinates
    g = geocoder.ip('me')
    result_path = "pothole_coordinates"
    i = 0
    b = 0

    # Process each frame in the video
    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if not ret:
            break

        # Apply Mars filter
        frame = apply_mars_filter_to_frame(frame)

        # Detect potholes
        frame, i, b = detectPotholeonFrame(frame, g, result_path, i, b)

        # Write the frame to the output video
        out.write(frame)

        # Display the frame (optional)
        cv2.imshow('Pothole Detection (Press Q to Close)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and writer
    video_capture.release()
    out.release()
    cv2.destroyAllWindows()

# Example usage
apply_mars_filter_to_video("WA_test_video.mp4", "color_graded_pothole_tested.mp4")
