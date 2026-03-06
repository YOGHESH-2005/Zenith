import cv2
import os
import numpy as np

path = "faces/yoghesh"

images = []

labels = []

for file in os.listdir(path):

    img = cv2.imread(f"{path}/{file}",0)

    img = cv2.resize(img,(200,200))

    images.append(img)

    labels.append(0)

recognizer = cv2.face.LBPHFaceRecognizer_create(
    radius=1,
    neighbors=8,
    grid_x=8,
    grid_y=8
)

recognizer.train(images,np.array(labels))

recognizer.save("face_model.yml")

print("Model trained successfully")