import cv2
from time import sleep

cap = cv2.VideoCapture(0)
k =7

widht = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#   WINDOWS     -> *'DIVX'
#   LINUX/MACOS -> 'XVID'

writer = cv2.VideoWriter('my_video.mp4', cv2.VideoWriter_fourcc('D','I','V','X'), k, (widht, height)) 
while True:

    ret, frame = cap.read()

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', frame)

    writer.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
writer.release()
cv2.destroyAllWindows()


cap = cv2.VideoCapture('my_video.mp4')

if cap.isOpened() == False:
    print('ERROR: FILE NOT FOUND OR WRONG CODEC USED. ')

while cap.isOpened():

    ret, frame = cap.read()

    if ret == True:

        sleep(1/k) # writer 25 fps
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()