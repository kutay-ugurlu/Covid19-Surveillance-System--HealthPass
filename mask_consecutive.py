from time import sleep
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import sys
from datetime import datetime

# load our serialized face detector model from disk
print("[INFO] loading face detector model...", flush=True)
prototxtPath = "/home/pi/Desktop/Integrated_FINAL/face_detector/deploy.prototxt"
weightsPath = "/home/pi/Desktop/Integrated_FINAL/face_detector/res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
print("[INFO] loading face mask detector model...", flush=True)
maskNet = load_model("/home/pi/Desktop/Integrated_FINAL/three_class_CGI_trained_for_Raspberry.model")

def detect_and_predict_mask(frame, faceNet, maskNet):
	# grab the dimensions of the frame and then construct a blob
	# from it
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
		(104.0, 177.0, 123.0))

	# pass the blob through the network and obtain the face detections
	faceNet.setInput(blob)
	detections = faceNet.forward()

	# initialize our list of faces, their corresponding locations,
	# and the list of predictions from our face mask network
	faces = []
	locs = []
	preds = []

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the detection
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the confidence is
		# greater than the minimum confidence
		if confidence > 0.7:
			# compute the (x, y)-coordinates of the bounding box for
			# the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# ensure the bounding boxes fall within the dimensions of
			# the frame
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			# extract the face ROI, convert it from BGR to RGB channel
			# ordering, resize it to 224x224, and preprocess it
			face = frame[startY:endY, startX:endX]
			#####################################################################
			
			#face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			
			#####################################################################
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)

			# add the face and bounding boxes to their respective
			# lists
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	# only make a predictions if at least one face was detected
	if len(faces) > 0:
		# for faster inference we'll make batch predictions on *all*
		# faces at the same time rather than one-by-one predictions
		# in the above `for` loop
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	# return a 2-tuple of the face locations and their corresponding
	# locations
	return (locs, preds)

print("[INFO] starting video stream...", flush=True)
vs = VideoStream(usePiCamera=True, framerate=20).start()
print("[INFO] Waiting for camera to heat up", flush=True)
time.sleep(5.0)

def classify_n_frames(frames:int, consecutive:int):

    mask_counter = 0
    
    i = 0
    while i <frames:
        try:
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
        
            if not len(locs):
                print("NO FACE", flush=True)
                continue
            
        
            locs_sorted = sorted(locs,key=lambda item: item[0])
            idx = locs.index(locs_sorted[0])
            box = locs_sorted[0]
            pred = preds[idx]
                
            # loop over the detected face locations and their corresponding
            # locations
                
            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (improper, mask, withoutMask) = pred
            label = "Mask" if np.max(pred) == mask else "Improper" if np.max(pred) == improper else "No Mask"
            color = (0,255,0) if np.max(pred) == mask else (0,255,255) if np.max(pred) == improper else (0,0,255)

            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask, improper) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.putText(frame, label, (startX, startY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)    
            cv2.imshow("Frame",frame)
            cv2.waitKey(20)
            
            
            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Mask" if np.max(pred) == mask else "Improper" if np.max(pred) == improper else "No Mask"
            if label == "Mask":
                mask_counter += 1
            else:
                mask_counter = 0
                
            if mask_counter >= consecutive:
                
                cv2.imwrite("Faces/"+str(datetime.now())+".png",frame)
                cv2.destroyAllWindows()
                return True
    
            i += 1
        except:
            print("Unexpected error:", sys.exc_info()[0])
            sleep(0.5)
            continue
    cv2.destroyAllWindows()
    return False
        
