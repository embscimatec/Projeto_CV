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

      k = cv2.waitKey(1)
      if k == 10:
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
      
      if k == 27:
        break


  def showPatientInfo(self):
    self.__vision.findEncodings()
    while True:
      self.__vision.detectFace()
      self.__vision.recognizeFace()
      cv2.imshow('Webcam', self.__vision.detected)

      k = cv2.waitKey(1)
      if k == 10:
        for n in self.__vision.recognized:
          self.__csv.showInfo(n)
          print("--")
        break
      if k == 27:
        break


  def changePatientInfo(self):
    self.__vision.findEncodings()
    while True:
      self.__vision.detectFace()
      self.__vision.recognizeFace()
      cv2.imshow('Webcam', self.__vision.detected)

      k = cv2.waitKey(1)
      if k == 10:
        for n in self.__vision.recognized:

          self.__csv.editData(n)
          print("--")
        break
      if k == 27:
        break


  def loop(self):
    while True:
      print("O que deseja? ")
      print("1) Registrar novo paciente ")
      print("2) Mostrar informacoes do paciente")
      print("3) Alterar informacoes do paciente")
      print("-) Sair")
      opt = int(input("-> "))
      if opt == 1:
        self.registerPatient()
      elif opt == 2:
        self.showPatientInfo()
      elif opt == 3:
        self.changePatientInfo()
      else:
        self.__vision.release()
        break
