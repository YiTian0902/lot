# Train multiple images per person
# Find and recognize faces in an image using a SVC with scikit-learn

"""
Structure:
        <test_image>.jpg
        <train_dir>/
            <person_1>/
                <person_1_face-1>.jpg
                <person_1_face-2>.jpg
                .
                .
                <person_1_face-n>.jpg
           <person_2>/
                <person_2_face-1>.jpg
                <person_2_face-2>.jpg
                .
                .
                <person_2_face-n>.jpg
            .
            .
            <person_n>/
                <person_n_face-1>.jpg
                <person_n_face-2>.jpg
                .
                .
                <person_n_face-n>.jpg
"""
import cv2
import face_recognition
from sklearn import svm
import os
import numpy as np

# Training the SVC classifier

# The training data would be all the face encodings from all the known images and the labels are their names
encodings = []
names = []

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Training directory
train_dir = os.listdir('train_dir')

# Loop through each person in the training directory
for person in train_dir:
    pix = os.listdir("train_dir/" + person)

    # Loop through each training image for the current person
    for person_img in pix:
        # Get the face encodings for the face in each image file
        face = face_recognition.load_image_file("train_dir/" + person + "/" + person_img)
        face_bounding_boxes = face_recognition.face_locations(face)

        #If training image contains none or more than faces, print an error message and exit
        if len(face_bounding_boxes) != 1:
            print(person + "/" + person_img + " contains none or more than one faces and can't be used for training.")
            exit()
        else:
            face_enc = face_recognition.face_encodings(face)[0]
            # Add face encoding for current image with corresponding label (name) to the training data
            encodings.append(face_enc)
            names.append(person)

# Create and train the SVC classifier
clf = svm.SVC(gamma='scale',class_weight='balanced')

# print(len(encodings[1]))
clf.fit(encodings, names)

# # Load the test image with unknown faces into a numpy array
# test_image = face_recognition.load_image_file('obama2.jpg')#'obama2.jpg'
#
# # Find all the faces in the test image using the default HOG-based model
# face_locations = face_recognition.face_locations(test_image)
# no = len(face_locations)
# print("Number of faces detected: ", no)
#
# # Predict all the faces in the test image using the trained classifier
# print("Found:")
# for i in range(no):
#     test_image_enc = face_recognition.face_encodings(test_image)[i]
#     # name = clf.predict([test_image_enc])
#     # print(*name)
#     print(clf.predict([test_image_enc]))

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face enqcodings in the frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    print(face_encodings)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        no = len(face_locations)
        print("Number of faces detected: ", no)

        # Predict all the faces in the test image using the trained classifier
        print("Found:")

        name=clf.predict(face_encodings)
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name[0], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

