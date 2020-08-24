import face_recognition as fr
import numpy as np
import cv2
import os
import csv
import shutil
from tempfile import NamedTemporaryFile

img_path = 'data'
csv_file = 'Registros.csv'
images = list()
names = list()
dataset = os.listdir(img_path)
scale = 0.25

for img in dataset:
    images.append(cv2.imread(img_path+'/'+img))
    names.append(os.path.splitext(img)[0])

def edit_data(name):
    filename = 'Registros.csv'
    temp_file = NamedTemporaryFile(mode='w', delete=False)

    with open(filename , "r") as csvfile, temp_file:

        reader = csv.DictReader(csvfile)
        fieldnames = ['Nome', 'Plano', 'CPF', 'Tel']
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            if str(row["Nome"]).upper() == name.upper():
                row["Nome"] = input("Qual o nome? ")
                row["Plano"] = input("Qual o Plano de Saude? ")
                row["CPF"] = int(input("Qual o CPF? "))
                row["Tel"] = int(input("Qual o Telefone? "))
                old = '{}/{}.jpg'.format(img_path, name)
                new = '{}/{}.jpg'.format(img_path, row["Nome"])
                os.rename(old, new)
            writer.writerow(row)
        
        shutil.move(temp_file.name, filename)
        return True
    return False


def findEncodings(images):
    encodes = list()
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes.append(fr.face_encodings(img)[0])
    return encodes

encode_list = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    img_small = cv2.resize(frame, (0,0), None, scale, scale)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

    faces_cur_frame = fr.face_locations(img_small)
    encodes_cur_frame = fr.face_encodings(img_small, faces_cur_frame)

    detected = frame.copy()
    for encode_face, face_loc in zip(encodes_cur_frame, faces_cur_frame):
        matches = fr.compare_faces(encode_list, encode_face)
        face_dist = fr.face_distance(encode_list, encode_face)
        match_index = np.argmin(face_dist)

        y1, x2, y2, x1 = face_loc
        x1, x2 = int(x1/scale), int(x2/scale)
        y1, y2 = int(y1/scale), int(y2/scale)
        if matches[match_index]:
            name = names[match_index].upper()
            color = (0,255,0)
        else:
            name = 'UNKNOWN'
            color = (0,0,255)

        cv2.rectangle(detected, (x1, y1), (x2, y2), color, 2)
        cv2.rectangle(detected, (x1, y2-28), (x2, y2), color, cv2.FILLED)
        cv2.putText(detected, name, (x1+6, y2-6), cv2.FONT_HERSHEY_PLAIN, 1.2, (255,255,255), 2)
        
    cv2.imshow('Webcam', detected)
    k = cv2.waitKey(1)
    if k == 10:
        if faces_cur_frame:
            with open(csv_file, 'r') as registros_csv:
                csv_dict_reader = csv.DictReader(registros_csv)
                for encode_face, face_loc in zip(encodes_cur_frame, faces_cur_frame):
                    matches = fr.compare_faces(encode_list, encode_face)
                    face_dist = fr.face_distance(encode_list, encode_face)
                    match_index = np.argmin(face_dist)

                    y1, x2, y2, x1 = face_loc
                    x1, x2 = int(x1/scale), int(x2/scale)
                    y1, y2 = int(y1/scale), int(y2/scale)
                    
                    delta_x = abs(int(0.2*(x2 - x1)))   # caso das bordas
                    delta_y = abs(int(0.2*(y2 - y1)))
                    face = detected[y1-delta_y:y2+delta_y , x1-delta_x:x2+delta_x]
                    cv2.imshow('Rosto', frame)

                    if matches[match_index]:
                        name = names[match_index]
                        edit_data(name)

            break
        
        else:
            print("Nenhum rosto foi detectado")

    if k == 27:
        break
        
cap.release()
cv2.destroyAllWindows()
