from Options import *

if __name__ == "__main__":
  dados = ['Nome', 'RG', 'CPF']
  csv = File('data', 'Registros.csv', dados)
  vision = Vision('data')
  op = Options(vision, csv)
  op.loop()
