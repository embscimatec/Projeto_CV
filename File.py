import os
import csv
import shutil
from tempfile import NamedTemporaryFile

class File:
  
  def __init__(self, img_path, csv_path, fieldnames):
    self.__img_path = img_path
    self.__csv_file = csv_path
    self.__fieldnames = fieldnames
  

  def initCSV(self):
    # Melhorar esse método
    with open(self.__csv_file, 'a') as csvfile:
      self.writer = csv.DictWriter(csvfile, fieldnames=self.__fieldnames)
      self.writer.writeheader()


  def showInfo(self, name):
    with open(self.__csv_file, 'r') as csvfile:
      self.reader = csv.DictReader(csvfile)
      for row in self.reader:
        if name.upper() == row['Nome'].upper():
          for key in row:
            print(f"{key}: {row[key]}")
            
  
  def addRow(self, name):
    with open(self.__csv_file, 'a') as csvfile:
      self.writer = csv.DictWriter(csvfile, fieldnames=self.__fieldnames)
      infos = dict()
      infos['Nome'] = name
      for fn in self.__fieldnames:
        if fn == 'Nome':
          pass
        else:
          infos[fn] = input(f"Digite o {fn}: ")

      self.writer.writerow(infos)


  def editData(self, name):
    temp_file = NamedTemporaryFile(mode='w', delete=False)
    with open(self.__csv_file, 'r') as csvfile, temp_file:
      self.reader = csv.DictReader(csvfile)
      temp_writer = csv.DictWriter(temp_file, fieldnames=self.__fieldnames)
      temp_writer.writeheader()
      for row in self.reader:
        if row['Nome'].upper() == name.upper():
          print(f"Alterando os dados de {row['Nome']}...")
          for k in row:
            row[k] = input(f"Digite o novo {k}: ").upper()
          old_name = '{}/{}.jpg'.format(self.__img_path, name)
          new_name = '{}/{}.jpg'.format(self.__img_path, row['Nome'])
          os.rename(old_name, new_name)
        temp_writer.writerow(row)
      shutil.move(temp_file.name, self.__csv_file)
      return True
    return False
