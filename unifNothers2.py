import pandas as pd                           # pandas is a software library written for the Python programming language for data manipulation and analysis
import numpy as np
import random as rand

def unif(seed,low,high):
    m = 2147483647
    a = 16807
    b = 127773
    c = 2836
    k=int(seed[0]/b)
    seed[0] = a*(seed[0]%b)-k*c
    if seed[0]<0:
        seed[0]=seed[0]+m
    val01=seed[0]/m
    return (low + int(val01*(high-low+1)))

def random_input(a,jobs,mcs,timeseed):
    mat = [ [0]*501 for _ in range(21) ]
    seed=[]
    seed.append(timeseed)
    for j in range(mcs):
        for i in range(jobs):
            mat[j][i] = unif(seed,1,99)
    for i in range(jobs):
        for j in range(mcs):
            a[i][j] = mat[j][i]

df = pd.read_excel("Taillard.xls", usecols=range(0,5), nrows=30, skiprows=2, header=None)  # parsing the excel file and storing in a pandas dataframe
data = df.to_numpy()
ind=rand.randint(0,29)
a=[ [0]*501 for _ in range(21) ]
jobs=data[ind][0]
mcs=data[ind][1]
timeseed=data[ind][2]
random_input(a,jobs,mcs,timeseed)
for i in range(jobs,0,-1):
    for j in range(mcs,0,-1):
        a[i][j]=a[i-1][j-1]
print("\nJob matrix (Jobs="+str(jobs)+", Machines="+str(mcs)+"):\n")
for i in range(1,jobs+1):
    for j in range(1,mcs+1):
        print(a[i][j],"\t",end="")
    print()