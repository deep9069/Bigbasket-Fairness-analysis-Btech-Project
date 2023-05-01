
import csv
import numpy as np
from scipy.special import rel_entr
import pandas as pd
from __future__ import division
import math
import random


df = pd.read_csv(r'D:\\B.Tech Project\\cookies.csv',index_col='sponsored')
csv_file=csv.reader (open('D:\\B.Tech Project\\cookies.csv','r'))
n=len(df)
print(n)


ps=[]
pn=[]
for i in range(6,n+1,10):
    p1=p2=0
    start_row = 2
    end_row = i
    #print(i)
    with open('D:\\B.Tech Project\\cookies.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        for j, row in enumerate(csv_reader, start=1):
            if (start_row <= j <= end_row):
                #print(j)
                if(row[0]=="Sponsored" or row[1]=="BB Royal" or row[1]=="BB Popular" or row[1]=="Fresho Organic" or row[1]=="BB Home" or row[1]=="Fresho"):
                    p1+=1
                    #print(p1)
                else:
                    p2+=1
            elif j > end_row:
                break        
    
    ps.append(p1)
    pn.append(p2)
        
print(ps)
print(pn)


csv_file=csv.reader (open('D:\\B.Tech Project\\cookies.csv','r'))
m=0
for row in csv_file:
    if(row[0]=="Sponsored" or row[1]=="BB Royal" or row[1]=="BB Popular" or row[1]=="Fresho Organic" or row[1]=="BB Home"):
        m+=1
print(m)        


KL_DIVERGENCE="rKL" # represent kl-divergence group fairness measure
ND_DIFFERENCE="rND" # represent normalized difference group fairness measure
RD_DIFFERENCE="rRD" # represent ratio difference group fairness measure
LOG_BASE=2 # log base used in logorithm function

NORM_CUTPOINT=5 # cut-off point used in normalizer computation
NORM_ITERATION=5 # max iterations used in normalizer computation
_user_N=n
_pro_N=m


def calculaterKL(_ranking_k,_pro_k,_user_N,_pro_N):
    """
        Calculate the KL-divergence difference of input ranking        
        :param _ranking_k: A permutation of k numbers that represents a ranking of k individuals, 
                                e.g., [0, 3, 5, 2, 1, 4].  Each number is an identifier of an individual.
                                Stored as a python array.
                                Can be a total ranking of input data or a partial ranking of input data.
        :param _pro_k: A set of identifiers from _ranking_k that represent members of the protected group
                                e.g., [0, 2, 3].  Stored as a python array for convenience, order does not matter.
        :param _user_N: The size of input items 
        :param _pro_N: The size of input protected group                
        :return: returns the value of KL-divergence difference of this input ranking
    """
    px=_pro_k/(_ranking_k)
    qx=_pro_N/_user_N
    if px==0 or px ==1: # manually set the value of extreme case to avoid error of math.log function 
        px=0.001
    if qx == 0 or qx ==1:
        qx=0.001
    return (px*math.log(px/qx,LOG_BASE)+(1-px)*math.log((1-px)/(1-qx),LOG_BASE))

def calculaterND(_ranking_k,_pro_k,_user_N,_pro_N):
    """
        Calculate the normalized difference of input ranking        
        :param _ranking_k: A permutation of k numbers that represents a ranking of k individuals, 
                                e.g., [0, 3, 5, 2, 1, 4].  Each number is an identifier of an individual.
                                Stored as a python array.
                                Can be a total ranking of input data or a partial ranking of input data.
        :param _pro_k: A set of identifiers from _ranking_k that represent members of the protected group
                                e.g., [0, 2, 3].  Stored as a python array for convenience, order does not matter.
        :param _user_N: The size of input items 
        :param _pro_N: The size of input protected group                
        :return: returns the value of normalized difference of this input ranking
    """
    return abs(_pro_k/_ranking_k-_pro_N/_user_N)

def calculaterRD(_ranking_k,_pro_k,_user_N,_pro_N):
    """
        Calculate the ratio difference of input ranking        
        :param _ranking_k: A permutation of k numbers that represents a ranking of k individuals, 
                                e.g., [0, 3, 5, 2, 1, 4].  Each number is an identifier of an individual.
                                Stored as a python array.
                                Can be a total ranking of input data or a partial ranking of input data.
        :param _pro_k: A set of identifiers from _ranking_k that represent members of the protected group
                                e.g., [0, 2, 3].  Stored as a python array for convenience, order does not matter.
        :param _user_N: The size of input items 
        :param _pro_N: The size of input protected group                
        :return: returns the value of ratio difference of this input ranking
        # This version of rRD is consistent with poster of FATML instead of arXiv submission.
    """
    input_ratio=_pro_N/(_user_N-_pro_N)
    unpro_k=_ranking_k-_pro_k
    
    if unpro_k==0: # manually set the case of denominator equals zero
        current_ratio=0
    else:
        current_ratio=_pro_k/unpro_k

    min_ratio=min(input_ratio,current_ratio)
       
    return abs(min_ratio-input_ratio)


def calculateFairness(_ranking,_protected_group,_user_N,_pro_N,_gf_measure):
    """
        Calculate the group fairness value of input ranking.
        Called by function 'calculateNDFairness'.
        :param _ranking: A permutation of N numbers (0..N-1) that represents a ranking of N individuals, 
                                e.g., [0, 3, 5, 2, 1, 4].  Each number is an identifier of an individual.
                                Stored as a python array.
                                Can be a total ranking of input data or a partial ranking of input data.
        :param _protected_group: A set of identifiers from _ranking that represent members of the protected group
                                e.g., [0, 2, 3].  Stored as a python array for convenience, order does not matter.
        :param _user_N: The size of input items 
        :param _pro_N: The size of input protected group
        :param _gf_measure: The group fairness measure to be used in calculation        
        :return: returns the value of selected group fairness measure of this input ranking
    """
      
    ranking_k=_ranking
    pro_k=_protected_group
    if _gf_measure==KL_DIVERGENCE: #for KL-divergence difference
        gf=calculaterKL(ranking_k,pro_k,_user_N,_pro_N)        
        
    elif _gf_measure==ND_DIFFERENCE:#for normalized difference
        gf=calculaterND(ranking_k,pro_k,_user_N,_pro_N)

    elif _gf_measure==RD_DIFFERENCE: #for ratio difference
        gf=calculaterRD(ranking_k,pro_k,_user_N,_pro_N)     

    return gf 


def calculateNDFairness(_ranking,_protected_group,_cut_point,_gf_measure,_normalizer):
    """
        Calculate group fairness value of the whole ranking.
        Calls function 'calculateFairness' in the calculation.
        :param _ranking: A permutation of N numbers (0..N-1) that represents a ranking of N individuals, 
                                e.g., [0, 3, 5, 2, 1, 4].  Each number is an identifier of an individual.
                                Stored as a python array.
        :param _protected_group: A set of identifiers from _ranking that represent members of the protected group
                                e.g., [0, 2, 3].  Stored as a python array for convenience, order does not matter.
        :param _cut_point: Cut range for the calculation of group fairness, e.g., 10, 20, 30,...
        :param _gf_measure:  Group fairness measure to be used in the calculation, 
                            one of 'rKL', 'rND', 'rRD'.
        :param _normalizer: The normalizer of the input _gf_measure that is computed externally for efficiency.
        :return: returns  fairness value of _ranking, a float, normalized to [0, 1]
    """
    
    user_N=_ranking
    pro_N=_protected_group

    # error handling for input value
    if NORM_CUTPOINT > user_N:
        raise ValueError("Batch size should be less than input ranking's length")
    
    discounted_gf=0 #initialize the returned gf value
    for i in range(len(ps)):
        ranking_cutpoint=NORM_CUTPOINT*(i+1)
        pro_cutpoint=ps[i]
        gf=calculateFairness(ranking_cutpoint,pro_cutpoint,user_N,pro_N,_gf_measure)
        discounted_gf+=gf/math.log(ranking_cutpoint+1,LOG_BASE) # log base -> global variable
        
    if _normalizer==0:
        raise ValueError("Normalizer equals to zero")
    return discounted_gf/_normalizer



fair_rKL = calculateNDFairness(_user_N,_pro_N,NORM_CUTPOINT,KL_DIVERGENCE,1)
fair_rND = calculateNDFairness(_user_N,_pro_N,NORM_CUTPOINT,ND_DIFFERENCE,1)
fair_rRD = calculateNDFairness(_user_N,_pro_N,NORM_CUTPOINT,RD_DIFFERENCE,1)

print(fair_rKL)
print(fair_rND)
print(fair_rRD)