
import csv
import numpy as np
from scipy.special import rel_entr
import pandas as pd
from __future__ import division
import math
import random


df = pd.read_csv(r'D:\\B.Tech Project\\BB flour.csv',index_col='label')
csv_file=csv.reader (open('D:\\B.Tech Project\\BB flour.csv','r'))
n=len(df)
print(n)


de = pd.read_csv(r'D:\B.Tech Project\BB-flour-Copy.csv',index_col='label')
csv_file=csv.reader (open('D:\B.Tech Project\BB-flour-Copy.csv','r'))
n=len(df)
print(n)


dcg=[]

with open('D:\\B.Tech Project\\BB flour.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for i, row in enumerate(csv_reader, start=0):
        if(i==1):
            a=int(row[7])
            dcg.append(a)
        elif(i>1):
            a=dcg[i-2]+int(row[7])/np.log2(i)
            dcg.append(a)
        
print(dcg)


idcg=[]

with open('D:\\B.Tech Project\\BB-flour-Copy.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for i, row in enumerate(csv_reader, start=0):
        if(i==1):
            a=int(row[7])
            idcg.append(a)
        elif(i>1):
            a=idcg[i-2]+int(row[7])/np.log2(i)
            idcg.append(a)
        
print(idcg)


b=[]
for i in range(0,len(dcg)):
    b.append(idcg[i]/dcg[i])
print(b)
print(len(b))


c=0
d=0
with open('D:\\B.Tech Project\\BB flour.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for j, row in enumerate(csv_reader, start=0):
        if (1 <= j):
            if(row[0]=="BB Royal" or row[0]=="BB Popular" or row[0]=="Fresho Organic" or row[0]=="BB Home" or row[0]=="Fresho"):
                c+=b[j-1]
                d+=1
            

print(c/d)