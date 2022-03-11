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


a = [[0]*21 for _ in range(501)]
jobs = 20  # jobs,mcs & timeseed to be changed accordingly
mcs = 5
timeseed = 873654221
random_input(a, jobs, mcs, timeseed)

b = [[0]*(mcs+2) for _ in range(jobs)]
for i in range(0, jobs):
    for j in range(0, mcs):
        b[i][j] = a[i][j]

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
        
##########################################################################################
#                                NEH Algorithm                                           #
##########################################################################################


mks = [0]*24
seql = [[] for _ in range(24)]   # permuted sequence plus makespan generated later
z = [0]*4

z[0] = 0
z[1] = 1
z[2] = 2
z[3] = 3

p = permutations(z)

m=10
j = 0
for i in list(p):
    seql[j].extend(i)
    mks[j] = makespan(sorted_ml[:][0:-2], i)
    seql[j].append(mks[j])
    j = j+1

sorted_seql = sorted(seql, key=lambda x: x[4], reverse=True)

bestm = [[0]*4 for _ in range(m)]  # best 10 job sequence of new index
for i in range(0, m):
    for j in range(0, 4):
        bestm[i][j] = sorted_seql[i][j]

originalm = [[0]*4 for _ in range(m)]
for i in range(m):
    for j in range(4):
        originalm[i][j] = sorted_ml[bestm[i][j]][mcs+1]


for _ in range(4, jobs):
    nu_seq = [[] for _ in range((_+1)*(_+1)*(m))]  # to store the new job index 2D matrix
    org_seq = [[] for _ in range((_+1)*(_+1)*(m))] # to store the original job index 2D matrix
    ind = 0
    for i in range(m):

        for j in range(0, _+1):  # for e.g. 201, 021, 012
            bs_copy = bestm[i][:]
            bs_copy.insert(j, _)
            org_copy = originalm[i][:]
            org_copy.insert(j, sorted_ml[_][mcs+1])
            org_seq[ind] = org_copy[:]# to store the 2d matrix of original job indices
            nu_seq[ind] = bs_copy[:]# to store the 2d matrix of new job indices
            org_seq[ind].append(makespan(nu_sorted, bs_copy))
            nu_seq[ind].append(makespan(nu_sorted, bs_copy))
            ind = ind+1
            
    
    #####################################################################################
    #                                Whale Algorithm                                    #
    #####################################################################################
    
    
    for a in range(m*(_+1)): # Loop runs for (m * job) times
        
        Copy_org_seq = org_seq[a][0:-1] # org_seq is copied avoiding the last column containing mkspn................Eg. [10, 12, 15, 8, 20]
        Copy_nu_seq = nu_seq[a][0:-1]   # nu_seq is copied avoiding the last column containing mkspn.................Eg. [1, 2, 3, 4, 5]
        
        random_index1 = random.randint(0, len(Copy_org_seq)-1) # 1st random index taken from copy org_seq............Eg. random_index1 = 1
        
        j_org_1 = Copy_org_seq[random_index1] # job of the 1strandom index of copied org_seq saved in j_org_1........Eg. j_org_1 = 12
        j_nu_1 = Copy_nu_seq[random_index1] # Same job of 1st random index from copied nu_seq is saved in j_nu_1.....Eg. j_nu_1 = 2
        
        Copy_org_seq.pop(random_index1) # 1st random index popped from copied org_seq................................Eg. Copy_org_seq = [10, 15, 8, 20]
        Copy_nu_seq.pop(random_index1) # 1st random index popped from copied nu_seq..................................Eg. Copy_nu_seq = [1, 3, 4, 5]
        
        random_index2 = random.randint(0, len(Copy_org_seq)-1) # 2nd random index taken from copy org_seq............Eg. random_index = 3
        
        j_org_2 = Copy_org_seq[random_index2] # job of the 2nd random index of copied org_seq saved in j_org_2.......Eg. j_org_2 = 8
        j_nu_2 = Copy_nu_seq[random_index2] # Same job of 2nd random index from copied nu_seq is saved in j_nu_1.....Eg. j_nu_2 = 4
        
        Copy_org_seq.pop(random_index2) # 2nd random index popped from copied org_seq................................Eg. Copy_org_seq = [10, 15, 20]
        Copy_nu_seq.pop(random_index2) # 2nd random index popped from copied nu_seq..................................Eg. Copy_nu_seq = [1, 3, 5]
        
        for b in range(0, _):
            
            nu_copy = Copy_nu_seq # nu_copy stores the sequence with new job indies..........................Eg. nu_copy = [1, 3, 5] {for b = 0}
            nu_copy.insert(b, j_nu_1) # 1st random job inserted..............................................Eg. nu_copy = [2, 1, 3, 5] {for b = 0}
            nu_copy.insert(b, j_nu_2) # 2nd random job inserted..............................................Eg. nu_copy = [4, 2, 1, 3, 5] {for b = 0}
            
            org_copy = Copy_org_seq # org_copy stores the sequence with original job indices.................Eg. org_copy = [10, 15, 20] {for b = 0}
            org_copy.insert(b, sorted_ml[j_nu_1][mcs+1]) # 1st random job inserted...........................Eg. org_copy = [12, 10, 15, 20] {for b = 0}
            org_copy.insert(b, sorted_ml[j_nu_2][mcs+1]) # 2nd random job inserted...........................Eg. org_copy = [8, 12, 10, 15, 20] {for b = 0}
            
            org_seq[ind] = org_copy[:] # in a new row of org_seq, org_copy is taken..........................Eg. org_seq = [[...],[...],...,[8, 12, 10, 15, 20]] {for b = 0}
            nu_seq[ind] = nu_copy[:] # in a new row of nu_seq, nu_copy is taken..............................Eg. nu_seq = [[...],[...],...,[4, 2, 1, 3, 5] {for b = 0}
            
            org_seq[ind].append(makespan(nu_sorted, nu_copy)) # makespan appended at the last column of og_seq
            nu_seq[ind].append(makespan(nu_sorted, nu_copy)) # makespan appended at the last column of nu_seq
            
            ind = ind + 1 # ind value updated for inserting the new org_copy & new nu_copy inside a new row of org_seq and nu_seq respectively
            
            
    #####################################################################################
    #                              NEH Continues                                        #
    #####################################################################################
    
    
    sorted_org = sorted(org_seq, key=lambda x: x[-1])  # sorted 2d matrix after adding another job (original index)
    sorted_nu = sorted(nu_seq, key=lambda x: x[-1])  # sorted 2d matrix after adding another job (new index)

    bestm = [[0]*(_+1) for y in range(m)]      # best10 2d matrix is made null
    originalm = [[0]*(_+1) for y in range(m)]    # original10 2d matrix is made null

    for z in range(0, m):
        for k in range(0, _+1):
            bestm[z][k] = sorted_nu[z][k]
            originalm[z][k] = sorted_org[z][k]


for a in range(0, m):
    print("Best Job Sequence obtained: ", originalm[a])
    print("Least Makespan = ", sorted_nu[a][-1])
