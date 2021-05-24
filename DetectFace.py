import cv2

def findFace(path):
    img = cv2.imread(path)
    face_cascade = cv2.CascadeClassifier('config/face_detector.xml')
    faces = face_cascade.detectMultiScale(img, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imwrite("face_detected.png", img)
    print('Successfully saved')