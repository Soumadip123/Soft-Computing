##########################################################################################
#                                Imports                                                 #
##########################################################################################


import random
from itertools import permutations
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)


##########################################################################################
#                            Job Matrix Generation                                       #
##########################################################################################


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


##########################################################################################
#                        Makespan Calculation Function                                   #
##########################################################################################


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


##########################################################################################
#                     Jobs, Machines and Timeseed input                                  #
##########################################################################################


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


m = 10

# ----- Exhaustive Permutation of 1st 4 jobs to form 4! job sequences ----- #

# permuted sequence and the makespan for each sequence will be stored here
seql = [[] for _ in range(24)]
p = list(permutations(range(0, 4)))  # p stores the list of permutations

j = 0
for i in list(p):
    seql[j].extend(i)
    mks = makespan(sorted_ml[:][0:-2], i)
    seql[j].append(mks)
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

    # to store the new job index 2D matrix
    nu_seq = [[] for _ in range((_+1)*(_+1)*(m))]
    # to store the original job index 2D matrix
    org_seq = [[] for _ in range((_+1)*(_+1)*(m))]

    ind = 0

    for i in range(m):  # will run for best m sequences

        # for e.g. [4, 0, 1, 2, 3], [0, 4, 1, 2, 3], [0, 1, 4, 2, 3], [0, 1, 2, 4, 3], [0, 1, 2, 3, 4], 4 at different positions
        for j in range(0, _+1):

            # nu_copy stores the sequence with new job indies from the bestm 2d list.............Eg. [0, 1, 2, 3]
            nu_copy = bestm[i][:]
            # Next job index added at the j-th poition............................................Eg. [4, 0, 1, 2, 3]
            nu_copy.insert(j, _)

            # org_copy stores the sequence with original job indices........................Eg. [10, 7, 18, 21]
            org_copy = originalm[i][:]
            # Original job corresponding to the new job index is inserted......Eg. [2, 10, 7, 18, 21]
            org_copy.insert(j, sorted_ml[_][mcs+1])

            # in a new row of org_seq, org_copy is taken
            org_seq[ind] = org_copy[:]
            # in a new row of nu_seq, nu_copy is taken
            nu_seq[ind] = nu_copy[:]

            # makespan appended at the last column of og_seq
            org_seq[ind].append(makespan(nu_sorted, nu_copy))
            # makespan appended at the last column of nu_seq
            nu_seq[ind].append(makespan(nu_sorted, nu_copy))

            ind = ind+1  # ind value updated for inserting the new org_copy & new nu_copy inside a new row of org_seq and nu_seq respectively

    #####################################################################################
    #                                Whale Algorithm                                    #
    #####################################################################################

    for a in range(m*(_+1)):  # Loop runs for (m * job) times

        # org_seq is copied avoiding the last column containing mkspn................Eg. [10, 12, 15, 8, 20]
        Copy_org_seq = org_seq[a][0:-1]
        # nu_seq is copied avoiding the last column containing mkspn.................Eg. [1, 2, 3, 4, 5]
        Copy_nu_seq = nu_seq[a][0:-1]

        # 1st random index taken from copy org_seq............Eg. random_index1 = 1
        random_index1 = random.randint(0, len(Copy_org_seq)-2)
        # 2nd random index taken from copy org_seq............Eg. random_index = 3
        random_index2 = random.randint(random_index1+1, len(Copy_org_seq)-1)

        r = random_index2 - random_index1

        reverse_Copy_Org = Copy_org_seq[random_index2:random_index1-1:-1]
        reverse_Copy_Nu = Copy_nu_seq[random_index2:random_index1-1:-1]

        Copy_org_seq = list(set(Copy_org_seq) - set(reverse_Copy_Org))
        Copy_nu_seq = list(set(Copy_nu_seq) - set(reverse_Copy_Nu))

        for b in range(0, _+1-r):

            # nu_copy stores the sequence with new job indies..........................Eg. nu_copy = [1, 3, 5] {for b = 0}
            nu_copy = Copy_nu_seq
            nu_copy[b:b] = reverse_Copy_Nu

            # org_copy stores the sequence with original job indices.................Eg. org_copy = [10, 15, 20] {for b = 0}
            org_copy = Copy_org_seq
            org_copy[b:b] = reverse_Copy_Org

            # in a new row of org_seq, org_copy is taken..........................Eg. org_seq = [[...],[...],...,[8, 12, 10, 15, 20]] {for b = 0}
            org_seq[ind] = org_copy[:]
            # in a new row of nu_seq, nu_copy is taken..............................Eg. nu_seq = [[...],[...],...,[4, 2, 1, 3, 5] {for b = 0}
            nu_seq[ind] = nu_copy[:]

            # makespan appended at the last column of og_seq
            org_seq[ind].append(makespan(nu_sorted, nu_copy))
            # makespan appended at the last column of nu_seq
            nu_seq[ind].append(makespan(nu_sorted, nu_copy))

            ind = ind + 1  # ind value updated for inserting the new org_copy & new nu_copy inside a new row of org_seq and nu_seq respectively

    #####################################################################################
    #                              NEH Continues                                        #
    #####################################################################################

    org_seq = list(filter(None, org_seq))
    nu_seq = list(filter(None, nu_seq))

    # sorted 2d matrix after adding another job (original index)
    sorted_org = sorted(org_seq, key=lambda x: x[-1])
    # sorted 2d matrix after adding another job (new index)
    sorted_nu = sorted(nu_seq, key=lambda x: x[-1])

    bestm = [[0]*(_+1) for y in range(m)]  # bestm 2d matrix is made null
    # originalm 2d matrix is made null
    originalm = [[0]*(_+1) for y in range(m)]

    for z in range(0, m):
        for k in range(0, _+1):
            bestm[z][k] = sorted_nu[z][k]
            originalm[z][k] = sorted_org[z][k]


#for a in range(0, m):
    #print("Best Job Sequence obtained: ", originalm[a])
#    print("Least Makespan = ", sorted_nu[a][-1])

print(sorted_nu[0][-1])
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
