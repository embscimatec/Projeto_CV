import os
import cv2
import numpy as np
import face_recognition as fr

class Vision:
  
  def __init__(self, img_path):
    self.__img_path = img_path
    self.__data_base = os.listdir(self.__img_path)

    self.__cap = cv2.VideoCapture(0)
    self.__scale = 0.25

    self.images = list()
    self.names = list()
    for img in self.__data_base:
      self.images.append(cv2.imread(self.__img_path+'/'+img))
      self.names.append(os.path.splitext(img)[0].upper())


  def detectFace(self):
    _, self.frame = self.__cap.read()
    img_small = cv2.resize(self.frame, (0,0), None, self.__scale, self.__scale)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

    self.faces_cur_frame = fr.face_locations(img_small)
    self.encodes_cur_frame = fr.face_encodings(img_small, self.faces_cur_frame)

    self.detected = self.frame.copy()

  
  def saveFace(self, face_loc, name):
    y1, x2, y2, x1 = face_loc
    x1, x2 = int(x1/self.__scale), int(x2/self.__scale)
    y1, y2 = int(y1/self.__scale), int(y2/self.__scale)
    delta_x = abs(int(0.2*(x2 - x1)))   # adicionar o caso das bordas
    delta_y = abs(int(0.2*(y2 - y1)))
    face = self.frame[y1-delta_y:y2+delta_y , x1-delta_x:x2+delta_x]
    cv2.imwrite(self.__img_path+'/'+name.upper()+'.jpg', face)

  
  def drawRectangle(self, face_loc, color=(0,0,255), text="UNKNOWN"):
    y1, x2, y2, x1 = face_loc
    x1, x2 = int(x1/self.__scale), int(x2/self.__scale)
    y1, y2 = int(y1/self.__scale), int(y2/self.__scale)
    cv2.rectangle(self.detected, (x1, y1), (x2, y2), color, 2)
    cv2.rectangle(self.detected, (x1, y2-28), (x2, y2), color, cv2.FILLED)     
    cv2.putText(self.detected, text, (x1+6, y2-6),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0,0,0), 1)


  def findEncodings(self):
    self.encode_list = list()
    print("Encoding in progres...")
    for img in self.images:
      self.encode_list.append(fr.face_encodings(img)[0])
    print("Encoding complete!")

  
  def recognizeFace(self):
    self.detectFace()
    self.recognized = list()

    for encode_face, face_loc in zip(self.encodes_cur_frame, self.faces_cur_frame):
      matches = fr.compare_faces(self.encode_list, encode_face)
      face_dist = fr.face_distance(self.encode_list, encode_face)
      match_index = np.argmin(face_dist)

      if matches[match_index]:
        name = self.names[match_index].upper()
        self.drawRectangle(face_loc, color=(0,255,0), text=name)
        self.recognized.append(name)
      else:
        self.drawRectangle(face_loc)
      

  def release(self):
    self.__cap.release()
    cv2.destroyAllWindows()
