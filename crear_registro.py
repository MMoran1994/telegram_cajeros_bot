import urllib.request
import csv
import json

def crear_registro():
    url = 'https://cdn.buenosaires.gob.ar/datosabiertos/datasets/cajeros-automaticos/cajeros-automaticos.csv'
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    dataset = csv.DictReader(lines)
    dic_de_regs = dict()
    for fila in dataset:
   		dic_de_regs[fila["id"]] = 0

    with open('registro_de_extracciones.json','w+') as registro:
    	registro.write(json.dumps(dic_de_regs))

crear_registro()