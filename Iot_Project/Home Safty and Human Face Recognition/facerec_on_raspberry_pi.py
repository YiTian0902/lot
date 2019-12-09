# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

import face_recognition
import cv2
import numpy as np
from rpi_spreadsheet import send_to_googleSheets

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
# camera = picamera.PiCamera()
# camera.resolution = (320, 240)

cam = cv2.VideoCapture(0)
cam.set(3, 240) # set video width
cam.set(4, 320) # set video height

# output = np.empty((240, 320, 3), dtype=np.uint8)

# Load a sample picture and learn how to recognize it.
print("Loading known face image(s)")
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

YI_image = face_recognition.load_image_file("YI.jpg")
YI_face_encoding = face_recognition.face_encodings(YI_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    YI_face_encoding,
]
known_face_names = [
    "Barack Obama",
    "Joe Biden",
    "YI",
]
count=0

print("Capturing image.")
while True:

    # Grab a single frame of video from the RPi camera as a numpy array
    ret, img = cam.read()
    count+=1
    #skip frame
    if count%10==0:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(img)
        # print("Found {} faces in image.".format(len(face_locations)))
        #检测到人脸才会进一步识别
        if(len(face_locations)>0):
            print('---------------------')
            face_encodings = face_recognition.face_encodings(img, face_locations)

            # Loop over each face found in the frame to see if it's someone we know.
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                match = face_recognition.compare_faces(known_face_encodings, face_encoding)

                names=[]

                if match[0]:
                    # name = "Barack Obama"
                    names.append('obama')
                elif match[1]:
                    names.append('binden')
                elif match[2]:
                    names.append('YI')
                else:
                    names.append("Unknown_Person")
                # print("I see someone named {}!".format(name))

                # for i in names:
                #     print(i)
                #     print('\n')
                print(len(names))
                #send name to google sheet
                send_to_googleSheets(names)
                
                
                
                
