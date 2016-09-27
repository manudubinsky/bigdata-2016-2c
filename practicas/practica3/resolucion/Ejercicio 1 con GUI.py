from Tkinter import *
import csv
from pandas import Series, DataFrame
import pandas as pd
from matplotlib import pyplot as plt
from geopy.distance import great_circle
from geopy.geocoders import Nominatim

class App:
    def __init__(self, master):
 
        frame = Frame(master)
        frame.pack()

        global entradaU
        entradaU = StringVar()
        
        lbl = Label (text= "Promedio").place(x=10,y=40)
        txtPromedio = Entry (ventana, textvariable = entradaU).place(x=70, y = 40)
        
        self.botonPromedio = Button(frame, text="Obtener Promedio", command=self.promedio)
        self.botonPromedio.pack(side=LEFT,padx=7, pady=7)
        
        self.boton1 = Button(frame, text="Cant Ambientes", command=self.funcion1)
        self.boton1.pack(side=LEFT,padx=7, pady=7)
        
        self.boton2 = Button(frame, text="Cant Ambientes sin Outliers", command=self.funcion2)
        self.boton2.pack(side=LEFT,padx=7, pady=7)
        
        self.boton3 = Button(frame, text="10 localidades con mayor cant publicaciones depto 2 amb", command=self.funcion3)
        self.boton3.pack(side=LEFT,padx=7, pady=7)

        self.boton4 = Button(frame, text="Tipos de propiedad", command=self.funcion4)
        self.boton4.pack(side=LEFT,padx=7, pady=7)
        
        self.boton5 = Button(frame, text="Distancia al congreso", command=self.funcion5)
        self.boton5.pack(side=LEFT,padx=7, pady=7)

    def promedio(self):
        df = pd.read_csv('abc.csv')
        df2 = df[df['place_name'] == 'Mar del Plata'][df['rooms'] == 2]
        df3 = df2[df2['price'].notnull()]
        promedio = df3['price'].mean()
        entradaU.set(promedio)

    def funcion1(self):
        df = pd.read_csv('abc.csv')
        df['rooms'].hist(bins = 30)
        plt.show()

    def funcion2(self):
        df = pd.read_csv('abc.csv')
        promedio = df['rooms'].mean()
        dfOutliers = df[df['rooms'] < promedio + 4]
        dfOutliers['rooms'].hist(bins = 30)
        plt.show()

    def funcion3(self):
        df = pd.read_csv('abc.csv')
        df5 = df[df['rooms'] == 2]
        df6 = df5[df5['place_name'].notnull()]
        df7 = df6['place_name']
        df8 = DataFrame(pd.value_counts(df7.values, sort = True))
        df8 = df8[:10]
        df8.plot(kind='bar')
        plt.show()

    def funcion4(self):
        df = pd.read_csv('abc.csv')
        df6 = df[df['property_type'].notnull()]
        df7 = df6['property_type']
        df8 = DataFrame(pd.value_counts(df7.values, sort = True))
        df8.plot(kind='bar')
        plt.show()
        
    def funcion5(self):
        tupla = tuple()
        geolocator = Nominatim()
        df = pd.read_csv('abc.csv')
        df6 = df[df['lat-lon'].notnull()]
        df7 = df6['lat-lon']
        congreso = (-34.609864,-58.392692)
        
        listaLatitudes = list()
        listaLongitudes = list()
        
        for each in df7:
                tupla = each.split(',')
                print('Direccion: ', geolocator.reverse(tupla).address, 'Distancia a congreso: ', great_circle(tupla,congreso).km)
                distanciaLat = congreso[0] - float(tupla[0])
                distanciaLong = congreso[1] - float(tupla[1])

                if (abs(distanciaLat) < 0.1 and abs(distanciaLong) < 0.1):
                    listaLatitudes.append(tupla[0])
                    listaLongitudes.append(tupla[1])
        
        plt.scatter(listaLatitudes, listaLongitudes)
        plt.show()


ventana = Tk()
ventana.geometry("1200x80+300+300")
ventana.title ("Histogramas")
app = App(ventana)
ventana.mainloop()

