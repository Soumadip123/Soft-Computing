import pandas as pd                           # pandas is a software library written for the Python programming language for data manipulation and analysis
import numpy as np
import random as rand
import csv

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

def makespan(M,S):     #To calculate and return makespan where M=matrix, S=sequence   
    prev=[0 for i in range(len(M[0]))]   #prev stores the time taken by previous job after each stage
    add = 0                                  #add sums up time taken by a job at every stage
    # print(S)
    for job in S:                            #job represents a job in the given sequence
        L=[]                                #L stores cumulative time taken after each stage     
        for mac in range(0,len(M[0])):     #mac represents a machine
            if mac==0:                 #For machine 1, time is added to previous job's time stamp at same stage
                add = prev[0] + M[job][0]
                L.append(add)
            else:                     #For remaining machines, it is checked whether the job's previous stage
                if add > prev[mac]:   #time or the previous job's same stage time is greater. The greater value
                    add = add + M[job][mac]   #is taken so that machine availability is guaranteed.
                else:
                    add = prev[mac] + M[job][mac]
                L.append(add)
        prev = L[:]                    #This job's L will become next job's prev
    return add


a=[ [0]*21 for _ in range(501) ]
jobs=500                                              #jobs,mcs & timeseed to be changed accordingly
mcs=20
timeseed = 28837162
random_input(a,jobs,mcs,timeseed)
# for i in range(jobs,0,-1):
#     for j in range(mcs,0,-1):
#         a[i][j]=a[i-1][j-1]
b=[ [0]*(mcs+2) for _ in range(jobs)]
for i in range(0,jobs):
    for j in range(0,mcs):
        b[i][j] = a[i][j]

print("\nJob matrix (Jobs="+str(jobs)+", Machines="+str(mcs)+"):\n")
for i in range(0,jobs):
    for j in range(0,mcs):
        print(a[i][j],"\t",end="")
    print()


add=0                                               #For calculating total processing time of each job
for i in range(jobs):                               #mcs column stores processing time, mcs+1 stores job no. from 1
    add=0
    b[i][mcs+1]=i+1
    for j in range(mcs):
        add=add+b[i][j]
    b[i][mcs]=add

sorted_ml = sorted(b, key=lambda x: x[mcs],reverse=True)        #sorted 2d array

nu_sorted=[[0]*mcs for _ in range(jobs)]
for i in range(jobs):
    for j in range(mcs):
        nu_sorted[i][j]=sorted_ml[i][j]                         #copy of sorted_ml
# print(sorted_ml)
# print(nu_sorted)
mksp1 = makespan(nu_sorted,[0,1])
mksp2 = makespan(nu_sorted,[1,0])
best_seq=[]                                                     #For original seq
nu_seq=[]                                                       #Seq for calculation of sorted matrix
if mksp1< mksp2:
    best_seq=[sorted_ml[0][mcs+1],sorted_ml[1][mcs+1]]
    nu_seq=[0,1]
else:
    best_seq=[sorted_ml[1][mcs+1],sorted_ml[0][mcs+1]]
    nu_seq=[1,0]
for i in range(2,jobs):
    mk_list=[]
    for j in range(0,i+1):                               # for e.g. 201, 021, 012
        bs_copy=nu_seq[:]
        bs_copy.insert(j,i)                              #inserting i at jth position
        mk_list.append(makespan(nu_sorted,bs_copy))
    min=mk_list[0]
    ind=0
    for i in range(1,len(mk_list)):
        if mk_list[i]<min:
            min=mk_list[i]
            ind=i                                        #best position
    best_seq.insert(ind,sorted_ml[i][mcs+1])
    nu_seq.insert(ind,i)
print("Best Job Sequence obtained: ",best_seq)
print("Least makespan value:",min)

#df1 = pd.DataFrame(b)
#df1.to_csv('D:\Project IT\output.csv', index=False, header=False)
