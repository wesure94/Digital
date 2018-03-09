# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 14:35:25 2018

@author: Administrator
"""
"""
    把502的距离除以2，在208找到距离最近的一个点，提取该点
"""

import matplotlib.pyplot as plt
 
line502 = open('E:\BaoSight/Codes/Digital_codes/version1/zscore502.txt').readlines()
line208 = open('E:\BaoSight/Codes/Digital_codes/version1/zscore208.txt').readlines()
l502 = len(line502)
l208 = len(line208)
len502 = []
thick502 = []
for i in range(l502):
    len502.append(float(line502[i].split('\t')[0]))
    thick502.append(line502[i].split('\t')[1])
len208 = []
thick208 = []
for i in range(l208):
    len208.append(float(line208[i].split('\t')[0]))
    thick208.append(line208[i].split('\t')[1])

wri = open('zscore-Cut208.txt','w')
k208 = 0 #开始搜索的起点下标
kth = k208 #每次找到的最短距离的208项的下标
x = []
y = []
for i in range(l502):
    length = len502[i] / 2
    dist = abs(len208[k208] - length)
    kth = k208
    #find the smallest distance
    for j in range(k208+1, l208):#min(k208+20,l208)):
        t = abs(len208[j]-length)
        if t < dist:
            dist = t
            kth = j
            if len208[j]-length > 0:
                #print('ok')
                break
        #if (j-k208)%100 == 0:
        #    print(i,j)
    k208 = kth+1
    if i % 100 == 0:
        print('ith:',i)
    wri.writelines([str(len208[kth]),'\t',thick208[kth]])
    x.append(len208[kth])
    y.append(thick208[kth])
    
wri.close()
            
plt.figure()
plt.plot(len208,thick208,x,y)
plt.show()

