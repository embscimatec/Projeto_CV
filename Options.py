from Vision import *
from File import *

class Options:

  def __init__(self, vision, csv):
    self.__vision = vision
    self.__csv = csv


  def registerPatient(self):
    while True:
      self.__vision.detectFace()

      for index, face_loc in enumerate(self.__vision.faces_cur_frame):
        self.__vision.drawRectangle(face_loc, color=(255,0,0), 
                                    text="Paciente "+str(index+1))

      cv2.imshow('Webcam', self.__vision.detected)

      if cv2.waitKey(1) == 10:
        if self.__vision.faces_cur_frame:
          for index, face_loc in enumerate(self.__vision.faces_cur_frame):
            name = input("Nome do paciente " + str(index+1) + ": ")
            if name.upper() not in self.__vision.names:
              self.__csv.addRow(name.upper())
              self.__vision.saveFace(face_loc, name.upper())
              self.__vision.names.append(name.upper())
            
            else:
              print("Paciente ja cadastrado. ")
          break
        else:
          print("Nenhum rosto foi detectado. ")
      
      if cv2.waitKey(1) == 27:
        break
