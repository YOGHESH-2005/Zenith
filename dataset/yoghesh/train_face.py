import cv2
import os
import numpy as np

dataset_path = "dataset/yogesh"

faces = []
labels = []

for image in os.listdir(dataset_path):

    img_path = os.path.join(dataset_path, image)

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    faces.append(img)

    labels.append(0)

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.train(faces, np.array(labels))

recognizer.save("face_model.yml")

print("Training complete")