#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import time
from operator import itemgetter
from matplotlib import pyplot as plt
import os

def text_size(total):
    return 13 + total / 200 * 20

def depurarPaginas():
    f = open("top-1m.csv", "r")
    w=open("paginas.txt","w")
    i=0
    while (i<500):
        for line in f:
            pagina = re.search(r'\.ar$', line)
            if pagina:
                separacionLinea = line.split(",")
                w.write("http://www."+separacionLinea[1])
        i = i + 1
    w.close()
    f.close()

def mostrarPalabras(diccionario, nombre2, nombre3):
    salidaOcurrencias = open (nombre3, "w")
    tuplaVIP = tuple()
    data = list()

    max1 = 0
    max2 = 0
    count = 0
    print ("\n")
    for k,v in diccionario:
        count = count + 1
        if (count >= len(diccionario)-9):
            salidaOcurrencias.write("Palabra: ")
            salidaOcurrencias.write(k)
            salidaOcurrencias.write(" - ")
            salidaOcurrencias.write("Ocurrencia: ")
            salidaOcurrencias.write(str(v))
            salidaOcurrencias.write("\n")
            k = k.decode('utf-8') #esto sirve para version 2.7
            tuplaVIP = (k,v, len(k))
            data.append(tuplaVIP)
            if (v > max1):
                max1 = v
            if (len(k) > max2):
                max2 = len(k)
    print ("\n")
    salidaOcurrencias.close()
    
    for word, job_popularity, resume_popularity in data:
        plt.text(job_popularity, resume_popularity, word, ha='center', va='center', size=text_size(job_popularity + resume_popularity))
    plt.xlabel("Ocurrencias")
    plt.ylabel("Longitud de la palabra")
    plt.axis([0, max1*1.2, 0, max2*1.2])
    plt.xticks([])
    plt.yticks([])
    fig1 = plt.gcf()
    plt.show()
    fig1.savefig(nombre2)
    plt.close()

def lecturaPaginas():
    archivocastellano = open ("listado-general.txt", "r") # en versiones nuevas de python poner ("listado-general.txt", "r", encoding = "utf8") y sacar los encode y decode
    archivoprohibido = open ("palabrasProhibidas.txt", "r")
    listaPalabrasCastellano = {}
    listaPalabrasProhibidas = list()
    
    if (not os.path.exists("palabras")): #si no esta creado el directorio donde se encuentra este archivo, se crea. Alli se almacenaran los txt y las word cloud
        os.mkdir("palabras")
    
    for linea in archivocastellano:
            if (linea[-1] == '\n'):
                linea = linea[:-1]
                listaPalabrasCastellano[linea] = 1

    archivocastellano.close()

    for lineas in archivoprohibido:
        palabrasProhibidas = lineas.split()
        for palabra2 in palabrasProhibidas:
            if palabra2 not in listaPalabrasProhibidas:
                listaPalabrasProhibidas.append(palabra2)

    archivoprohibido.close()

    for each in listaPalabrasProhibidas:
            listaPalabrasCastellano[each] = 0


    f = open ("paginas.txt", "r")
    for line in f:
            if (line[-1] == '\n'):
                line = line[:-1]
                try:
                    print ("Pagina: " + line + "\n")
                    html = requests.get(line).text
                    soup = BeautifulSoup(html, 'html5lib')
                    text = soup.get_text()
                    text = re.sub(r'\t',r'', text)
                    text = re.sub(r'\n',r'', text)
                    text = text.lower()
                    #print(text) #MUESTRA LA PAGINA
                    print ("\n")
                    listaABC = text.split(" ")
                    for i in range(0,len(listaABC)):
                        palabra = listaABC[i]
                        palabra = palabra.encode('utf-8') #esto sirve para version 2.7
                        if (palabra in listaPalabrasCastellano and palabra not in listaPalabrasProhibidas):
                            listaPalabrasCastellano[palabra] += 1
                            
                    diccionario = sorted(listaPalabrasCastellano.items(), key=itemgetter(1))
                    
                    name = re.sub(r'http://www.',r'',line)
                    nombre = "palabras/" + name + "Palabras" + ".txt" 
                    nombre2 = "palabras/"+ name + "Palabras" + ".png"
                    nombre3 = "palabras/" + name + "MasOcurrencias" + ".txt"
                    
                    mostrarPalabras(diccionario, nombre2, nombre3)

                    salidaPalabras = open (nombre, "w")

                    for each in listaPalabrasCastellano:
                        if (listaPalabrasCastellano[each] > 1):
                            salidaPalabras.write(each)
                            salidaPalabras.write("\n")
                            listaPalabrasCastellano[each] = 1
                    salidaPalabras.close()

                except requests.exceptions.ConnectionError as e:
                    print ("Problema en la pagina: " + line)
                    print (e)
                    print ("\n")
            else:
                print ("Pagina: " + line + "\n")
                html = requests.get(line).text
                soup = BeautifulSoup(html, 'html5lib')
                text = soup.get_text()
                text = re.sub(r'\t',r'', text)
                text = re.sub(r'\n',r'', text)
                text = text.lower()
                #print(text) #MUESTRA LA PAGINA
                print ("\n")
                listaABC = text.split(" ")
                for i in range(0,len(listaABC)):
                    palabra = listaABC[i]
                    palabra = palabra.encode('utf-8') #esto sirve para version 2.7
                    if (palabra in listaPalabrasCastellano and palabra not in listaPalabrasProhibidas):
                        listaPalabrasCastellano[palabra] += 1
                        
                diccionario = sorted(listaPalabrasCastellano.items(), key=itemgetter(1))
                
                name = re.sub(r'http://www.',r'',line)
                nombre = "palabras/" + name + "Palabras" + ".txt"
                nombre2 = "palabras/" + name + "Palabras" + ".png"
                nombre3 = "palabras/" + name + "MasOcurrencias" + ".txt"
                    
                mostrarPalabras(diccionario, nombre2, nombre3)
                
                salidaPalabras = open (nombre, "w")

                for each in listaPalabrasCastellano:
                    if (listaPalabrasCastellano[each] > 1):
                        salidaPalabras.write(each)
                        salidaPalabras.write("\n")
                        listaPalabrasCastellano[each] = 1
                salidaPalabras.close()           

#depurarPaginas()
lecturaPaginas()

