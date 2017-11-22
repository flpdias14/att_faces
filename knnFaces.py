#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
from math import sqrt
from matplotlib import pyplot as plt
import numpy as np
import cv2


def somaLista(lista):
    total = 0
    for num in lista:
        total += num
    return total

def media(lista):
    soma = somaLista(lista)
    media = soma / float(len(lista))
    return media

def variancia(lista):
    media1 = media(lista)
    variancia = 0
    for num in lista:
        variancia += pow((media1 - num), 2.0)
    variancia = variancia / float(len(lista))
    return variancia

def std(variancia):
    return pow(variancia, (0.5))

def moda(lista):
    repeticoes = 0
    for i in lista:
        aparicoes = lista.count(i)
        if aparicoes > repeticoes:
            repeticoes = aparicoes
    moda = []
    for i in lista:
        aparicao = lista.count(i)
        if aparicao == repeticoes and i not in moda:
            moda.append(i)
    return moda

def loadImage(file, mode=1):
    return cv2.imread (file, mode)

def randomNumList(numMax=9, lenList=5):
    lista = []
    num = 0
    for i in xrange(lenList):
        control = True
        while(control):
            num = randint(0, numMax)
            if(lista.count(num) == 0):
                lista.append(num)
                control = False
    return lista
# def equalizeHitogram(pixels, histogram, img):
    # imgSize = img.size
    # # for i in xrange(img.shape[0])):
    #     for k in xrange(img.shape[1])):

# Minkowski distance
def distancia(img1, img2, p=2):
    soma = np.float64(0)
    for i in xrange(img1.shape[0]):
        for k in xrange(img1.shape[1]):
            soma += np.float64(pow(img1[i][k]-img2[i][k], p))
    return pow(soma, 1/p)

def classificar(listaTreino, img, k=1, peso=False):
    distancias = []
    classificacao = ""
    for imgTreino in listaTreino:
        auxDist = []
        # adiciona a distancia
        auxDist.append(distancia(imgTreino[0], img[0], p=pow(2, -3.2)))
        # adiciona a classe
        auxDist.append(imgTreino[1])
        distancias.append(auxDist)
    distancias.sort(cmp=None, key=None, reverse=True)
    if k == 1:
        classificacao = distancias[0][1]
    else:
        if peso:
            listaClasses = []
            for i in xrange(1, 41):
                listaClasses.append([0, 's'+str(i)])
            for i in xrange(k):
                for classe in listaClasses:
                    if classe[1] == distancias[i][1]:

                        if distancias[i][0] != 0:
                            classe[0] += 1/distancias[i][0]
                        else:
                            classe[0] += 1/10000000.0

            rank = []
            for classe in listaClasses:
                if classe[0] != 0:
                    rank.append(classe)
            rank.sort(cmp=None, key=None, reverse=False)
            # print moda(rank)[0][1]
            classificacao = rank[-1][1]
        else:
            listaClasses = []
            for i in xrange(1, 41):
                listaClasses.append([0, 's'+str(i)])
            for i in xrange(k):
                for classe in listaClasses:
                    if classe[1] == distancias[i][1]:
                        if distancias[i][0] != 0:
                            classe[0] += 1
            rank = []
            for classe in listaClasses:
                if classe[0] != 0:
                    rank.append(classe)
            rank.sort(cmp=None, key=None, reverse=False)
            print rank
            # print moda(rank)
            # print moda(rank)[0][1]
            # classificacao = moda(rank)[0][1]
            classificacao = rank[-1][1]
    return classificacao

def prob(numPixelsR, totalPixels):
    return numPixelsR/totalPixels

# def equalizarHistograma(img, histograma):
#     l = 255
#
#     for k in xrange(l):
#         somatorio = 0
#         for j in xrange(k):
#             somatorio +=img

def loadFaces():
    listImages = []
    listFaces = []
    for i in xrange(1, 41):
        classe = 's'+str(i)
        for k in xrange(1, 11):
            img = cv2.equalizeHist(loadImage(classe+'/'+str(k)+'.pgm', 0)[12:95, 12:80])
            cv2.imshow('nomedajanela', img)
            cv2.waitKey(100)
            hist = cv2.calcHist([img],[0],None,[256],[0,256])
            listFaces.append([img, classe])
            # plt.hist(img.ravel(),256,[0,256]); plt.show()
        listImages.append(listFaces)
        # plt.hist(img.ravel(),256,[0,256]); plt.show()
        listFaces = []
    cv2.destroyAllWindows()
    return listImages
imagens = loadFaces()



listaTreinos = []
listaTreino = []
# print listaTreino
listaTestes = []
listaTeste = []
numTestes = 30
for i in xrange(numTestes):
    numSorteados = randomNumList()
    for j in numSorteados:
        # popula conjunto de terino
        for k in xrange(40):
            listaTreino.append(imagens[k][j])
    # popula o conjunto de teste
    for j in xrange(10):
        for k in xrange(40):
            if numSorteados.count(j) == 0:
                listaTeste.append(imagens[k][j])
    # print 'Lista Treino: '+str(len(listaTreino))
    # print 'Lista Teste: '+str(len(listaTeste))
    listaTreinos.append(listaTreino)
    listaTestes.append(listaTeste)
    listaTeste = []
    listaTreino = []

# declaração da lista de imagens classificadas
listaClassificada = []
listaClassificados = []
acertos = 0
erros = 0
listaAcertos = []
listaErros = []
arq = open('log-3knn.txt', 'w')
text = []
for i in xrange(numTestes):
    print 'Treino '+str(i)
    arq.write('Treino '+str(i))
    arq.write('\n------------------------------------------')
    for teste in listaTestes[i]:
        classe = classificar(listaTreinos[i], teste, k=3, peso=True)
        if len(teste) == 2:
            teste.insert(2, classe)
            print 'real: '+teste[1]+' | classificado: '+teste[2]+'\t'
            #arq.write('real: '+teste[1]+' | classificado: '+teste[2])
        listaClassificada.append(teste)

    print '-----------------------------------------'
    for img in listaClassificada:
        # print individuo
        if img[1] == img[2]:
            acertos += 1
        else:
            erros += 1
    print '\nAcertos: ' + str(acertos)
    arq.write('Acertos: ' + str(acertos))
    print '\nErros: ' + str(erros)
    arq.write('\nErros: ' + str(erros))
    arq.write('\n-----------------------------------------------------')
    listaClassificados.append(listaClassificada)
    listaClassificada = []
# print classificar(listaTreino, lista[0][1], k=3, peso=False)



# contadores de acertos e erros gerais
acertos = 0
erros = 0
listaAcertos = []
listaErros = []
for i in xrange(numTestes):
    for img in listaClassificados[i]:
        # print individuo
        if img[1] == img[2]:
            acertos += 1
        else:
            erros += 1
    listaAcertos.append(acertos)
    listaErros.append(erros)
    acertos = 0
    erros = 0

listaTaxasErro = []
listaTaxasAcerto = []
for i in xrange(numTestes):
    listaTaxasErro.append((listaErros[i]/float((listaErros[i]+listaAcertos[i]))))

for i in xrange(numTestes):
    listaTaxasAcerto.append(1-listaTaxasErro[i])
arq.write("\nLista Acertos | Taxa Acerto")
arq.write('\n--------------------')
for i in xrange(numTestes):
    arq.write(str(listaAcertos[i])+' | '+str(listaTaxasAcerto[i])+'\n')
arq.write('\n----------------fim--------------')
arq.write("\nLista Erros | taxa Ettos")
arq.write('\n--------------------')
for i in xrange(numTestes):
    arq.write(str(listaErros[i])+' | '+str(listaTaxasErro[i])+'\n')
arq.write('\n----------------fim--------------')

print "\nMedia Acertos: " + str(media(listaAcertos))
arq.write("\nMedia Acertos: " + str(media(listaAcertos)))
print "Media Erros: "+str(media(listaErros))
arq.write("\nMedia Erros: "+str(media(listaErros)))
print "Variancia Acertos: "+str(variancia(listaAcertos))
arq.write("\nVariancia Acertos: "+str(variancia(listaAcertos)))
print "Variancia Erros: "+str(variancia(listaErros))
arq.write("\nVariancia Erros: "+str(variancia(listaErros)))
print "Desvio Padrão Acertos: "+ str(std(variancia(listaAcertos)))
arq.write("\nDesvio Padrão Acertos: "+ str(std(variancia(listaAcertos))))
print "Desvio Padrão Erros: "+ str(std(variancia(listaErros)))
arq.write("\nDesvio Padrão Erros: "+ str(std(variancia(listaErros))))
print "-----------------------------------------------------------"
print "Média taxas Acerto: "+str(media(listaTaxasAcerto)*100)+"%"
arq.write("\nMédia taxas Acerto: "+str(media(listaTaxasAcerto)*100)+"%")
print "Média taxas Erro: "+str(media(listaTaxasErro)*100)+"%"
arq.write("\nMédia taxas Erro: "+str(media(listaTaxasErro)*100)+"%")
arq.writelines(text)
arq.close()
