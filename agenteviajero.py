# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 11:13:46 2020

@author: WINDOWS
"""
import csv
from random import randrange, choice

#ramdon para la poblacion
def ran(cab):
    r=True
    l=[]
    while len(l)<4:
        ra=choice(cab)
        #print(ra)
        if (ra in l)== False:
            l.append(ra)
    #print(l,'\n')
    return l

#cre una candid n de poblacion
def poblacion(cab,n):
    poblacion=[]
    for r in range(0,n):
        poblacion.append(ran(cab))
    return poblacion
#costo de la ruta de a -> b
def valor(a,b,x):
    cab=x[0]
    val=0;
    for row in x:
        for i in range(0,len(row)):
            #print(row[0],"  asdf")
            if row[0]==a:
                val=cab[i-1]
                if val==b:
                    re=row[i]
            
    return re

#revivimos p que es toda la poblacion que son las rutas de cada generacion y calculamos su costo total 
def total_ruta(p,x):
    lista=[]
    menor=5000000
    for ruta in p:
        suma=sumar(ruta,x)
        lista.append([suma,ruta])
        #lista.append(ruta)
        if suma<=menor:
            menor=suma
            l_menor=ruta
                
    return menor,l_menor
def sumar(ruta,x):
    suma=0
    for i in range(0,len(ruta)-1):
        suma=int(valor(ruta[i], ruta[i+1], x))+suma
    #print(ruta[i+1]," - ",ruta[0], "final")
    suma=int(valor(ruta[i+1], ruta[0], x))+suma
    return suma

#cruzar a y b son los padres, siendo ha y hb sus hijos, los retorna
def cruzar(a,b):
    r1=randrange(4)
    r2=randrange(4)
    while r1==r2:
        r1=randrange(4)
        r2=randrange(4)
    if r1>r2:
        f=r1
        r1=r2
        r2=f
    #print(r1,r2,'         ******rangos cru a:',a,' b:',b)
    
    ha=[0,1,2,3]
    hb=[0,1,2,3]
    ha[r1:r2+1]=b[r1:r2+1]
    hb[r1:r2+1]=a[r1:r2+1]
    #print(ha,hb,"           aaa")
    ha=cruz(ha,a,r1,r2)
    hb=cruz(hb,b,r1,r2)
    return ha,hb

def cruz(ha,a,r1,r2):
    for i in range(0,len(ha)):
        if i<r1:
            #print(ha[i])
            for pa in a:
                if (pa in ha)==False:
                    ha[i]=pa
                    break
        if i>r2:
            #print(ha[i])
            for pa in a:
                if (pa in ha)==False:
                    ha[i]=pa
                    break
    return ha


#mutar: recibe una poblacion a luego saca rangos x , y para intercambiar
def mutar(a):
    #print(a,'   original')
    x=randrange(4)
    y=randrange(4)
    while x==y:
        x=randrange(4)
        y=randrange(4)
    aux=a[x]
    a[x]=a[y]
    a[y]=aux
    return a
    #print(a, '  despues',x,'  -  ',y)

#ordenar desendentemente retorna una lista ordenada
def ordenar(p,x):
    clon=p
    ordenado=[]
    
    ruta_nemor=0
    while len(clon)!=0:
        menor=50000
        if len(clon)==1:
            ordenado.append(clon.pop(0))
        else:
            for pi in range(0,len(clon)):
             #   print(pi,"             pi   ",len(clon))
                sumados=sumar(clon[pi],x)
                if sumados<=menor:
                    menor=sumados
                    ruta_nemor=pi
            mejor=clon.pop(ruta_nemor)
            #print(mejor, "           mejor", ruta_nemor)
            ordenado.append(mejor)
            
        
    return ordenado
    

#Generaciones
def generaciones(p,x,nro_generaciones):
    print("Poblacion inicial:")
    print(p,"\n")
    print("Suma se rutas de poblacion")
    print(total_ruta(p, x),"\n")
    
    mejorGeneracion=[]
    nroG=0
    totals=5000
    for i in range(nro_generaciones):
        print('GENERACION :',i+1)
        p=ordenar(p, x)
        #print("Suma se rutas de poblacion")
        #print(total_ruta(p, x),"\n")
        print(p)
        #print(int(len(p)/2),"         444444444")
        #CRUZANDO LOS ELEMENTOS
        for h in range(int(len(p)/2)):
            c1, c2=cruzar(p[h*2], p[(h*2)+1])
            p[h*2]=c1
            p[h*2+1]=c2
        #MUTANDO LOS ELEMENTOS
        
        for m in range(len(p)):
            p[m]=mutar(p[m])
        
        menor,listam=total_ruta(p, x)
        print(" \nMejor ruta\n",listam,'   TOTAL:',menor,'\n')
        if menor<totals:
            totals=menor
            mejorGeneracion=listam
            nroG=i
    return mejorGeneracion,nroG,totals
            



#main :v
x=[]
with open('datos.csv', newline='') as File:  
    reader = csv.reader(File)
    for row in reader:
        x.append(row)
        print(row)
#print(x)
cab=x[0]
cab.pop(0)
#creamos la poblacion
p=poblacion(cab, 10)

l,g,t=generaciones(p, x, 10)
print('----------------------------------------------------')
print('MEJOR RUTA:')
print(l)
print('TOTAL RUTA:')
print(t)
print('SALIO EN LA GENERACION:')
print(g)
print('----------------------------------------------------')


