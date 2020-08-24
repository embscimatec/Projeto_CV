import os
import csv
import cv2
import numpy as np
import face_recognition as fr

cap = cv2.VideoCapture(0)
csv_list = 'Registros.csv'
path = 'data'
scale = 0.25
images = list()
names = list()

data_base = os.listdir(path)
print(data_base)
for img in data_base:
    images.append(cv2.imread(path+'/'+img))
    names.append(os.path.splitext(img)[0])


while True:
    ret, frame = cap.read()

    img_small = cv2.resize(frame, (0,0), None, scale, scale)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

    faces_cur_frame = fr.face_locations(img_small)
    encodes_cur_frame = fr.face_encodings(img_small, faces_cur_frame)

    k = cv2.waitKey(1)

    detected = frame.copy()

    #for face_loc in faces_cur_frame:
    for index, face_loc in enumerate(faces_cur_frame):
        y1, x2, y2, x1 = face_loc
        x1, x2 = int(x1/scale), int(x2/scale)
        y1, y2 = int(y1/scale), int(y2/scale)

        cv2.rectangle(detected, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.rectangle(detected, (x1, y2-28), (x2, y2), (0,255,0), cv2.FILLED)
        cv2.putText(detected, "Paciente "+str(index+1), (x1+6, y2-6), 
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.2, (255,255,255), 2)
    
    cv2.imshow('Webcam', detected)

    if k == 10:
        if faces_cur_frame:
            with open(csv_list, 'a') as csvfile:
                fieldnames = ["Nome", "Plano", "CPF", "Tel"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for index, face_loc in enumerate(faces_cur_frame):
                
                    name = input("Nome do paciente " + str(index+1) + ": ")
                    if name not in names:
                        #plan = input("Plano de saude: ")
                        #cpf = int(input("CPF: "))
                        #tel = int(input("Telefone: "))
                        plan = "PlanoX"
                        cpf = 12345
                        tel = 23456
                        infos = {"Nome":name, 
                                 "Plano":plan, 
                                 "CPF":cpf, 
                                 "Tel":tel}

                        writer.writerow(infos)

                        y1, x2, y2, x1 = face_loc
                        x1, x2 = int(x1/scale), int(x2/scale)
                        y1, y2 = int(y1/scale), int(y2/scale)
                        delta_x = abs(int(0.2*(x2 - x1)))   # caso das bordas
                        delta_y = abs(int(0.2*(y2 - y1)))
                        face = frame[y1-delta_y:y2+delta_y , x1-delta_x:x2+delta_x]
                        cv2.imwrite(path+'/'+name+'.jpg', face)
                    else:
                        print("Paciente ja cadastrado")
            break

        else:
            print("Nenhum rosto foi detectado")

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
