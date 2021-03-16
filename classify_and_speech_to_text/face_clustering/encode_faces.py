# USAGE
	# python encode_faces.py --dataset dataset --encodings encodings.pickle

# import the necessary packages
from imutils import paths
# face_recognition library by @ageitgey
import face_recognition
# argument parser
import argparse
# pickle to save the encodings
import pickle
# openCV
import cv2
# operating system
import os
from constants import ENCODINGS_PATH

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized database of facial encodings")
ap.add_argument("-d", "--detection_method", type=str, default="cnn",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

# grab the paths to the input images in our dataset, then initialize
# out data list (which we'll soon populate)
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))
data = []

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# load the input image and convert it from RGB (OpenCV ordering)
	# to dlib ordering (RGB)
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	print(imagePath)

	# loading image to BGR
	image = cv2.imread(imagePath)

	# converting image to RGB format
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	boxes = face_recognition.face_locations(image,
		model=args["detection_method"])

	# compute the facial embedding for the face
	encodings = face_recognition.face_encodings(image, boxes)

	# build a dictionary of the image path, bounding box location,
	# and facial encodings for the current image
	d = [{"imagePath": imagePath, "loc": box, "encoding": enc}
		for (box, enc) in zip(boxes, encodings)]
	data.extend(d)

# dump the facial encodings data to disk
print("[INFO] serializing encodings...")
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()
print("Encodings of images saved in {}".format(ENCODINGS_PATH))

# Arguments:
#
#     -i --dataset : The path to the input directory of faces and images.
#     -e --encodings : The path to our output serialized pickle file containing the facial encodings.
#     -d --detection_method : Face detection method to be used. Can be "hog" or "cnn" (Default: cnn)
#
# What it does
#
#     create a list of all imagePaths in our dataset using the dataset path provided in our command line argument.
#     we compute the 128-d face encodings for each detected face in the rgb image
#     For each of the detected faces + encodings, we build a dictionary that includes:
#         The path to the input image
#         The location of the face in the image (i.e., the bounding box)
#         The 128-d encoding itself
#     Can be reused. write the data list to disk as a serialized encodings.pickle file
#
# Usage - To run $python encode_faces.py --dataset dataset --encodings encodings.pickle --detection_method "cnn"