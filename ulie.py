import cv2
import sys
import serial
import time
import pygame
import threading
import random

pygame.mixer.init()

global instList
global basicPatrolLoop
instList = ['2','2','3','3','2','2','3','3','2','2','3','3','2','2','3']
basicPatrolLoop = ['2', '2', '3', '3']
global bplCount
bplCount = 0

ser = serial.Serial('/dev/ttyUSB0', 9600)
ser.write('2')
pygame.mixer.music.load("Gengar.mp3")
pygame.mixer.music.play()

##cascPath = sys.argv[1]
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
ret = video_capture.set(3, 360)
ret = video_capture.set(4, 240)

time.sleep(2)


global loopCount
loopCount= 0

def faceDetect():
    print "fd-began"
    global loopCount
    loopCount = loopCount + 1
    # Capture frame-by-frame
    video_capture = cv2.VideoCapture(0)
    ##ret = video_capture.set(3, 360)
    ##ret = video_capture.set(4, 240)
    
    ret, frame = video_capture.read()
    
    if (ret):
        print "fd-read successful"
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=8,
            minSize=(50, 50),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        if len(faces) > 0 and loopCount > 5:
            loopCount = 0
            rdm = random.randint(0,4)
            if rdm == 0:
                pygame.mixer.music.load("Gengar.mp3")
            if rdm == 1:
                pygame.mixer.music.load("297-mewto.mp3")
            if rdm == 2:
                pygame.mixer.music.load("Marowak.mp3")
            if rdm == 3:
                pygame.mixer.music.load("Raichu.mp3")
            if rdm == 4:
                pygame.mixer.music.load("Dragonite.mp3")
            pygame.mixer.music.play()
            print "fd-face detected"
            print "fd-adding instructions"
            global instList
            instList.pop()
            instList.pop()
            instList.pop()
            instList.pop()
            instList.pop()
            instList.insert(14, '4')
            instList.insert(14, '4')
            instList.insert(14, '4')
            instList.insert(14, '4')
            instList.insert(14, '4')
    ##        pygame.mixer.music.load("297-mewto.mp3")
    ##        pygame.mixer.music.play()
    ##        while pygame.mixer.music.get_busy() == True:
    ##           continue

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)
    print "fd-complete"

def faceDetectLoop():
    while True:
        faceDetect()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def writeInstructions():
    while True:
        print "wi-began"
        global bplCount
        global instList
        bplCount = bplCount + 1
        if bplCount == 4 :
            bplCount = 0
        ser.write(instList.pop())
        print "wi-adding item:" + basicPatrolLoop[bplCount]
        instList.insert(0, basicPatrolLoop[bplCount])
        time.sleep(0.8)
        print "wi-complete"
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

try:
    fdThread = threading.Thread(target=faceDetectLoop, args=(), kwargs={})
    wiThread = threading.Thread(target=writeInstructions, args=(), kwargs={})
    fdThread.start()
    wiThread.start()
except:
    print "Threading Error :'("

    
# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()