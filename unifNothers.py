import pandas as pd
import numpy as np

def unif(seed, low, high):
    m=2147483647
    a=16807
    b=127773
    c=2836
    k=seed[0]/b
    seed[0] = a*(seed[0]%b)-k*c
    if seed[0]<0:
        seed[0] =seed[0]+m
    val01 = seed[0]/m
    return low+(val01*(high-low+1))

def random_input(a):
    mat=[[]*21]*MAXCOLS
    seed=[]*1
    seed[0]=timeseed
    for j in range(0,mcs,1):
        for i in range(0,jobs,1):
            mat[j][i]=unif(seed,1,99)
    for i in range(0,jobs,1):
        for j in range(0,mcs,1):
            a[i][j]=mat[j][i]
	
for i in range(jobs,0,-1):
    for j in range(mcs,0,-1):
        a[i][j]=a[i-1][j-1]
