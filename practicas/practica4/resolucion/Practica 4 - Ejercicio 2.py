#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import time
import pandas as pd
from operator import itemgetter
from matplotlib import pyplot as plt
import os

def crearLista(df, expresion):
    dom = list()
    for each in df['web']:
        a = re.search(expresion,each)
        if (a):
            dom.append(a.group(1))
    return dom

def crearHistograma(dominios, nombre, nombreHistograma):
    diccionario = {}
    diccionario2 = {}
    listaDominios = list()
    listaOcurrencias = list()

    if (not os.path.exists("dominios")):
        os.mkdir("dominios")

    salidaDominios = open(nombre,"w")
    
    for each in dominios:
        if (each not in diccionario) and (each != 'com') and (each != 'net') and (each != 'org'):
            diccionario[each] = 1
        else:
            if (each != 'com' and each != 'net' and each != 'org'):
                diccionario[each] += 1
        
    diccionario2 = sorted(diccionario.items(), key=itemgetter(1))

    count = 0
    for k,v in diccionario2:
        count = count + 1
        if (count >= len(diccionario2)-9):
            listaDominios.append(k)
            listaOcurrencias.append(v)
            salidaDominios.write("Dominio: ")
            salidaDominios.write(k)
            salidaDominios.write(" | Ocurrencia: ")
            salidaDominios.write(str(v))
            salidaDominios.write("\n")

    salidaDominios.close()

    xs = [i + 0.1 for i, _ in enumerate(listaDominios)]
    plt.bar(xs, listaOcurrencias)
    plt.ylabel("Repeticiones")
    plt.title("Dominio")
    plt.xticks([i + 0.5 for i, _ in enumerate(listaDominios)], listaDominios)
    fig1 = plt.gcf()
    plt.show()
    fig1.savefig(nombreHistograma)
    plt.close()

def dataFrame():
    df = pd.read_csv ('top-1m.csv')

    nombre1 = "dominios\dominios.txt"
    nombreHistograma1 = "dominios\histograma.png"
    nombre2 = "dominios\dominiosEdu.txt"
    nombreHistograma2 = "dominios\histogramaEdu.png"
    
    expresion = r'([a-z]*)$'
    dominios = crearLista(df, expresion)
    crearHistograma(dominios, nombre1, nombreHistograma1)

    expresion2 = r'edu\.([a-z]*)$'
    dominios2 = crearLista(df, expresion2)
    crearHistograma(dominios2, nombre2, nombreHistograma2)
    

dataFrame()
    
