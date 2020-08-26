from Options import *

if __name__ == "__main__":
  csv = File('data', 'Registros.csv', ['Nome', 'RG', 'CPF'])
  vision = Vision('data')
  op = Options(vision, csv)
  op.registerPatient()
  