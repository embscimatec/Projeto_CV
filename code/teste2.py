import cv2
import numpy as np

#imagem

img = cv2.imread("..\galeria\IEEE LOGOTIPO VERTICAL AZUL PNG.png")
kernel = np.ones((5,5),np.uint8)

print(img.shape)

#manipulando uma imagem

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #transformando a imagem em escala de cinza
imgBlur = cv2.GaussianBlur(imgGray, (7,7),0) #adicionando efeito blur na imagem
imgCanny = cv2.Canny(img,150,200)
imgDialation = cv2.dilate(imgCanny, kernel, iterations=1)
imgEroded = cv2.erode(imgDialation, kernel, iterations=1)

cv2.imshow("Original", img)
cv2.imshow("Gray", imgGray)
cv2.imshow("Blur", imgBlur)
cv2.imshow("Canny", imgCanny)
cv2.imshow("Dialation", imgDialation)
cv2.imshow("Eroded", imgEroded)
cv2.waitKey(0)

#mostrando um video
'''
cap = cv2.VideoCapture("galeria\my_video.mp4")

while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''

#mostarndo imgem da camera
'''
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,100) #O 10 representa uma alteração no brilho (não vi diferença)

while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''



