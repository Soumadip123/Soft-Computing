# pandas is a software library written for the Python programming language for data manipulation and analysis
import random
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

'''
def makespan(M, S):  # To calculate and return makespan where M=matrix, S=sequence
    # prev stores the time taken by previous job after each stage
    prev = [0 for i in range(len(M[0]))]
    add = 0  # add sums up time taken by a job at every stage
    # print(S)
    for job in S:  # job represents a job in the given sequence
        L = []  # L stores cumulative time taken after each stage
        for mac in range(0, len(M[0])):  # mac represents a machine
            if mac == 0:  # For machine 1, time is added to previous job's time stamp at same stage
                add = prev[0] + M[job][0]
                L.append(add)
            else:  # For remaining machines, it is checked whether the job's previous stage
                # time or the previous job's same stage time is greater. The greater value
                if add > prev[mac]:
                    # is taken so that machine availability is guaranteed.
                    add = add + M[job][mac]
                else:
                    add = prev[mac] + M[job][mac]
                L.append(add)
        prev = L[:]  # This job's L will become next job's prev
    return add
'''

def makespan(M, S):
    delay_array = [0]*(mcs)
    for i in range(1, mcs):
        x = M[S[0]][i-1]
        y = 0
        for k in range(1, len(S)):
            y = y + M[S[k]][i-1] - M[S[k-1]][i]
            #print(y)
            if(y > 0):
                x = x + y
                y = 0
        delay_array[i] = delay_array[i-1] + x
    x = 0
    #print(delay_array)
    for i in range(len(S)):
        x = x + M[i][mcs-1]
    mkspn = delay_array[mcs-1] + x
    return mkspn


a = [[0]*21 for _ in range(501)]
jobs = 20  # jobs,mcs & timeseed to be changed accordingly
mcs = 10
timeseed = 2065119309
random_input(a, jobs, mcs, timeseed)
# for i in range(jobs,0,-1):
#     for j in range(mcs,0,-1):
#         a[i][j]=a[i-1][j-1]
b = [[0]*(mcs+2) for _ in range(jobs)]
for i in range(0, jobs):
    for j in range(0, mcs):
        b[i][j] = a[i][j]

#print("\nJob matrix (Jobs="+str(jobs)+", Machines="+str(mcs)+"):\n")
#for i in range(0, jobs):
#    for j in range(0, mcs):
#        print(a[i][j], "\t", end="")
#    print()


add = 0  # For calculating total processing time of each job
for i in range(jobs):  # mcs column stores processing time, mcs+1 stores job no. from 1
    add = 0
    b[i][mcs+1] = i+1
    for j in range(mcs):
        add = add+b[i][j]
    b[i][mcs] = add

sorted_ml = sorted(b, key=lambda x: x[mcs], reverse=True)  # sorted 2d array

nu_sorted = [[0]*mcs for _ in range(jobs)]
for i in range(jobs):
    for j in range(mcs):
        nu_sorted[i][j] = sorted_ml[i][j]  # copy of sorted_ml


mks = [0]*24
seql = [[] for _ in range(24)] # permuted sequence plus makespan generated later 
z = [0]*4
#print(z)
z[0] = 0
z[1] = 1
z[2] = 2
z[3] = 3
#print(z)
p=permutations(z)
#for i in list(p):
#   print(i)


j=0
for i in list(p):
    seql[j].extend(i)
    mks[j]=makespan(sorted_ml[:][:-2],i)
    seql[j].append(mks[j])
    #print(mks[j])
    j=j+1
 
sorted_seql = sorted(seql, key=lambda x: x[4])

#print(sorted_seql)
   
best10 = [[0]*4 for _ in range(10)] #best 10 job sequence of new index
for i in range(0,10):
    for j in range(0,4):
        best10[i][j]=sorted_seql[i][j]
#print(best10)
    
original10 = [[0]*4 for _ in range(10)] #
for i in range(10):
    for j in range(4):
        original10[i][j]=sorted_ml[best10[i][j]][mcs+1]
#print(original10)

m=10
for _ in range(4, jobs):
    
    nu_seq = [[] for _ in range((_+1)*m)]   # to store the new job index 2D matrix
    org_seq = [[] for _ in range((_+1)*m)]  # to store the original job index 2D matrix
    
    #mk_list = [0]*500                       # to store makeaspan of each list at each step
    ind = 0
    for i in range(m):
        
        for j in range(0, _+1):                               #for e.g. 201, 021, 012
            bs_copy = best10[i][:]
            bs_copy.insert(j, _)
            org_copy = original10[i][:]    
            org_copy.insert(j, sorted_ml[_][mcs+1])
            #mk_list[ind] = makespan(nu_sorted, bs_copy)
            org_seq[ind] = org_copy[:]                      # to store the 2d matrix of original job indices
            nu_seq[ind] = bs_copy[:]                        # to store the 2d matrix of new job indices

            org_seq[ind].append(makespan(nu_sorted, bs_copy))
            nu_seq[ind].append(makespan(nu_sorted, bs_copy))
            ind=ind+1
            #print(org_seq)
            #print("\n\n")
            #print(nu_seq)
            #print("\n\n")

             
    sorted_org = sorted(org_seq, key=lambda x: x[-1]) # sorted 2d matrix after adding another job (original index)
    sorted_nu = sorted(nu_seq, key=lambda x: x[-1])   # sorted 2d matrix after adding another job (new index)
    
    best10 = [[0]*(_+1) for y in range(m)]      # best10 2d matrix is made null
    original10 = [[0]*(_+1) for y in range(m)]   # original10 2d matrix is made null
    
    for z in range(0,10):
        for k in range(0,_+1):
            best10[z][k]=sorted_nu[z][k]
            original10[z][k]=sorted_org[z][k]
    
    '''best10 = sorted_nu[0:10][0:-1]    # best 10 seq is inserted(new index)
    original10 = sorted_org[0:10][0:-1]  # best 10 seq is inserted(original index)'''
    #print(best10,"\n\n")
    #print(sorted_nu,"\n\n")  
  
for a in range(0,m):
    #print("Best Job Sequence obtained: ", sorted_org[a][:-1])
    print("Least Makespan = ",sorted_nu[a][-1])
#print("Least makespan value:", min)


