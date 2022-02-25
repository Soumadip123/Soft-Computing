# pandas is a software library written for the Python programming language for data manipulation and analysis
import pandas as pd
import numpy as np
import random as rand
import csv
from itertools import permutations


def unif(seed, low, high):
    m = 2147483647
    a = 16807
    b = 127773
    c = 2836
    k = int(seed[0]/b)
    seed[0] = a*(seed[0] % b)-k*c
    if seed[0] < 0:
        seed[0] = seed[0]+m
    val01 = seed[0]/m
    return (low + int(val01*(high-low+1)))


def random_input(a, jobs, mcs, timeseed):
    mat = [[0]*501 for _ in range(21)]
    seed = []
    seed.append(timeseed)
    for j in range(mcs):
        for i in range(jobs):
            mat[j][i] = unif(seed, 1, 99)
    for i in range(jobs):
        for j in range(mcs):
            a[i][j] = mat[j][i]


a = [[0]*21 for _ in range(501)]
jobs = 20  # jobs,mcs & timeseed to be changed accordingly
mcs = 5
timeseed = 873654221
random_input(a, jobs, mcs, timeseed)
# for i in range(jobs,0,-1):
#     for j in range(mcs,0,-1):
#         a[i][j]=a[i-1][j-1]
b = [[0]*(mcs+2) for _ in range(jobs)]
for i in range(0, jobs):
    for j in range(0, mcs):
        b[i][j] = a[i][j]

delay_array = [0]*(mcs)

def delay_array_Generator():
    for i in range(0, jobs+1):
        for j in range(0, jobs+1):
            if(i==j):
                delay_matrix[i][j]=-1
                continue
            else:
                
