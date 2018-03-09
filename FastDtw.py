# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 09:27:42 2018

@author: Administrator
"""

import copy
import sys
import matplotlib.pyplot as plt
from fastdtw import fastdtw
#from dtw import dtw
#from numpy.linalg import norm

#from scipy.spatial.distance import euclidean
import csv
from datetime import datetime

def DTW():
    file_208 = './Reduce/zscore-Cut208.txt'
    file_502 = './zscore502.txt'
    
    #file_208 = 'E:\BaoSight/Digtal/Signal_process/new_208.txt'
    #file_502 = 'E:\BaoSight/Digtal/Signal_process/new_502.txt''
    list_208 = open(file_208).readlines()
    list_502 = open(file_502).readlines()
    
    write_file = open('result.csv','w',newline = '')
    fieldnames = ['point_2','dis2x','dis2y','point_5','point_5r','dis5x','dis5y','dtw']
    csv_write= csv.DictWriter(write_file,fieldnames= fieldnames)
    csv_write.writeheader()

    thick208 = []
    thick502 = []
    dist208 = []
    dist502 = []
    aver208 = 0
    aver502 = 0
    for line in list_208:
        k = line.split('\t')
        dist208.append(float(k[0]))
        thick208.append(float(k[1]))
        aver208 += float(k[1])
    for line in list_502:
        k = line.split('\t')
        dist502.append(float(k[0]))
        thick502.append(float(k[1]))
        aver502 += float(k[1])
        
    
    aver502 /= len(dist502)
    aver208 /= len(dist208)
    #for i in range(len(dist208)):
    #    thick208[i] = thick208[i] - (aver208-aver502)#(thick208[0]-thick502[0])#
        
    print('============cal============')
    loc_208 = 200
    loc_502 = 100
    
    #thick502 = thick502[len(dist502)-len(dist208):]
    #dist502 = dist502[len(dist502)-len(dist208):]
    #start = loc_208*4
    print(datetime.now())
    for start in range(20020,20021):#0, len(dist208)-loc_208,loc_208):
        X = copy.deepcopy(thick208[start:start+loc_208])
        Minest = sys.maxsize
        for k in range(0,len(dist502)-loc_502,10):
            for i in range(k,len(dist502)):
                if (dist502[i]-dist502[k] > (dist208[start+loc_208]-dist208[start])*1.2):
                    break
            Y = copy.deepcopy(thick502[k:i])
            #dtw
            l1=len(X)
            l2=len(Y) 
            M=[[abs(X[i1]-Y[j1]) for i1 in range(l1)] for j1 in range(l2)]
            D=[[0 for i1 in range(l1+1)] for i1 in range(l2+1)]
            D[0][0]=0 
            Path = [[0 for i1 in range(l1+1)] for i1 in range(l2+1)]
            for i1 in range(1,l1+1):
                D[0][i1]=sys.maxsize
            for j1 in range(1,l2+1):
                D[j1][0]=sys.maxsize
            for i1 in range(1,l2+1):
                for j1 in range(1,l1+1):
                    if i1 > j1-6 and i1 < j1+6:
                        Min = D[i1-1][j1-1]
                        Path[i1][j1] = 3 #1:横向 2：纵向 3:斜方向
                        if Min > D[i1-1][j1]:
                            Min = D[i1-1][j1]
                            Path[i1][j1] = 1
                        if Min > D[i1][j1-1]:
                            Min = D[i1][j1-1]
                            Path[i1][j1] = 2
                        D[i1][j1]=M[i1-1][j1-1]+Min
                    else:
                        D[i1][j1] = sys.maxsize
            distance = D[-1][-1]
            
            #distance,path = fastdtw(X,Y,dist = lambda x,y:abs(x-y))
            #distance,cost, acc,path = dtw(X,Y,dist=lambda X, Y: norm(X - Y))
            if distance < Minest:
                Minest = distance
                print('distance:',Minest)
                Minest_p = copy.deepcopy(Path)
                ith = i  #502的终点
                kth = k #502的起点
            
            if k % 100 == 0:
                print('locate 502:',k,i)
                csv_write.writerow({'point_2':start,'dis2x':dist208[start],'dis2y':dist208[start+loc_208],'point_5':k,'point_5r':i,'dis5x':dist502[k],'dis5y':dist502[i],'dtw':distance})
        #print(Minest)
        print(k)
        print('502:',kth,ith)
        print(datetime.now())
        print('208 start:',start)
        
    Pth = []
    x_f = ith-kth+1
    y_f = l1
    print('Minest_p:',len(Minest_p))
    print(x_f-1)
    while (x_f != 0 and y_f != 0):
        t = Minest_p[x_f-1][y_f-1]
        Pth.append([x_f-1,y_f-1])
        #print('(',start+x_f,',',y_f,')')
        if t == 1:
            x_f -= 1
        elif t == 2:
            y_f -= 1
        else:
            x_f -= 1
            y_f -= 1
    
    
    plt.figure(1)
    X1 = [0 for i in range(ith-kth+1)]
    #print(Pth)
    for i in range(len(Pth)):
        X1[Pth[i][0]] = dist208[start+Pth[i][1]]
    plt.plot(X1[1:],thick502[kth:ith],marker = 'x',label = '502')
    plt.plot(dist208[start:start+loc_208],X,marker = 'x', label = '208')
    
    plt.figure(2)
    plt.plot(dist502[kth:ith],thick502[kth:ith],marker = 'x',label = '502')
    plt.plot(dist208[start:start+loc_208],X,marker = 'x', label = '208')
    plt.legend(loc = 'upper right')
    plt.show()
    
DTW()