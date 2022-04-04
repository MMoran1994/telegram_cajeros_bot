import urllib.request
import csv
from math import radians
from staticmap import StaticMap, CircleMarker
import json
import numpy as np
import random
import threading
import time
import datetime
import sys

#Funciones auxiliares
#Obtener el dataset de cajeros automáticos y convertirlo a un formato legible
def obtener_dataset():
    url = 'https://cdn.buenosaires.gob.ar/datosabiertos/datasets/cajeros-automaticos/cajeros-automaticos.csv'
    response = urllib.request.urlopen(url)
    if response.status != 200:
        sys.exit("Error: El dataset no está disponible")
    lines = [l.decode('utf-8') for l in response.readlines()]
    dataset = csv.DictReader(lines)
    dataset_banelco = list()
    dataset_link = list()
    for fila in dataset:
    	if fila["red"].lower() == "banelco":
    		dataset_banelco.append(fila)
    	else:
    		dataset_link.append(fila)
    return dataset_link, dataset_banelco

def a_radianes(latYLong):
    return (radians(float(latYLong[0])), radians(float(latYLong[1])))

def filtrar_menores_a_500(cajeros):
    return [cajero for cajero in cajeros if cajero["dist_a_us"] < 500]

def construir_respuesta_con(cajeros_en_rango):
    respuesta = ""
    for cajero in cajeros_en_rango:
        respuesta = respuesta + ", ".join((cajero["banco"], cajero["ubicacion"]))
        if cajero != cajeros_en_rango[-1]:
            respuesta = respuesta+"\n"
    return respuesta

def construir_mapa(coords_del_usuario, cajeros_en_rango):
    m = StaticMap(400, 400, 50)
    m.add_marker(CircleMarker(coords_del_usuario, 'black', 18))
    m.add_marker(CircleMarker(coords_del_usuario, 'red', 12))
    for cajero in cajeros_en_rango:
        coordenada = (cajero["long"], cajero["lat"])
        m.add_marker(CircleMarker(coordenada, 'black', 18))
        m.add_marker(CircleMarker(coordenada, 'yellow', 12))
    mapa = m.render()
    return mapa

def filtrar_por_extraccion(cajeros, reg_de_extracciones):
    return [cajero for cajero in cajeros if reg_de_extracciones[cajero["id"]]<100]

def filtrar_cajeros(cajeros, reg_de_extracciones):
    cajeros_filtrados = filtrar_menores_a_500(cajeros)
    cajeros_filtrados = filtrar_por_extraccion(cajeros_filtrados, reg_de_extracciones)
    return cajeros_filtrados

def modificar_registro(cajeros, reg_de_extracciones):
    if len(cajeros) == 1:
        reg_de_extracciones[cajeros[0]["id"]]+=1
    else:
        distancias = np.array([cajero["dist_a_us"] for cajero in cajeros])
        decidir_cajero_e_inc_extraccion(distancias, reg_de_extracciones, cajeros)

def decidir_cajero_e_inc_extraccion(distancias, reg_de_extracciones, cajeros):
    indice_a_sumar = decidir_indice(np.argsort(distancias))
    reg_de_extracciones[cajeros[indice_a_sumar]["id"]]+=1
    actualizar_archivo_registros(reg_de_extracciones)

def decidir_indice(indices_sorteados):
    decididor = random.randint(1, 10)
    if len(indices_sorteados) == 2:
        if decididor <= 7:
            return indices_sorteados[0]
        else:
            return indices_sorteados[1]
    else:
        if decididor <= 7:
            return indices_sorteados[0]
        elif decididor <= 9:
            return indices_sorteados[1]
        else:
            return indices_sorteados[2]

def actualizar_archivo_registros(reg_de_extracciones):
    archivo_de_extracciones = open("registro_de_extracciones.json", "w")
    json.dump(reg_de_extracciones, archivo_de_extracciones)
    archivo_de_extracciones.close()

def obtener_registros_extraccion():
    archivo_de_extracciones = open("registro_de_extracciones.json", "r")
    registro_de_extracciones = json.load(archivo_de_extracciones)
    archivo_de_extracciones.close()
    return registro_de_extracciones

def reiniciar_registro():
    while 1:
        if es_momento_de_reiniciar():
            registro_de_extracciones = obtener_registros_extraccion()
            registro_de_extracciones = dict.fromkeys(registro_de_extracciones.keys(), 0)
            actualizar_archivo_registros(registro_de_extracciones)
            time.sleep(60)

def es_momento_de_reiniciar():
    return son_las_ocho_en_punto() and not es_fin_de_semana()

def son_las_ocho_en_punto():
    return str(datetime.datetime.now().strftime("%H")) == "08" and str(datetime.datetime.now().strftime("%M")) == "00"

def es_fin_de_semana():
    return datetime.datetime.now().strftime("%w") == 0 or datetime.datetime.now().strftime("%w") == 6