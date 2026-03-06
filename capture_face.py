import cv2
import os

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

count = 0

save_path = "faces/yoghesh"

os.makedirs(save_path, exist_ok=True)

while True:

    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:

        face = gray[y:y+h,x:x+w]

        face = cv2.resize(face,(200,200))

        cv2.imwrite(f"{save_path}/{count}.jpg",face)

        count += 1

        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.imshow("Capture Face",frame)

    if count >= 100:
        break

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()