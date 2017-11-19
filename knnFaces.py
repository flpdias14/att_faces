#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
from math import sqrt
import cv2


def loadImage(file, mode=1):
    return cv2.imread (file, mode)

def randomNumList(numMax=9, lenList=10):
    lista = []
    num = 0
    for i in range(lenList):
        control = True
        while(control):
            num = randint(0, numMax)
            if(lista.count(num) == 0):
                lista.append(num)
                control = False
    return lista

def loadFaces():
    listImages = []
    listFaces = []
    for i in range(1, 41):
        classe = 's'+str(i)
        for k in range(1, 11):
            img = loadImage(classe+'/'+str(k)+'.pgm', 0)[12:95, 12:80]
            listFaces.append([img, classe])
        listImages.append(listFaces)
        listFaces = []
    return listImages


listaTreinos = []
listaTreino = []
listaTestes = []
listaTeste = []
