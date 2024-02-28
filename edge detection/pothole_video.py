# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 02:46:03 2024

@author: maris
"""

import cv2
import numpy as np


# Load the video
cap = cv2.VideoCapture('tested.mp4')

# Create a VideoWriter object to save the processed video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_video.mp4', fourcc, 20.0, (640, 480))  # Adjust size accordingly

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the frame to grayscale
    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold the grayscale image
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Process each contour
    for contour in contours:
        # Calculate contour area
        area = cv2.contourArea(contour)

        # Skip small contours (noise)
        if area < 100 or area > 300000:
            continue

        # Calculate the bounding rectangle for the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Draw rectangle around the contour
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, 'Pothole Detected', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Draw contour on potholes detected image
        cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)

    # Write the frame to the output video
    out.write(frame)

    # Display the frame
    cv2.imshow('Potholes Detected', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release VideoCapture and VideoWriter objects
cap.release()
out.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
