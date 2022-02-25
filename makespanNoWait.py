def makespanNw(M,S):
    L=len(M)                            #no. of jobs
    delay=[[0]*L for _ in range(L)]      #An LxL zero matrix for extra delay count
    for i in range(L):
        for j in range(L):              #jth job follows ith job
            w = 0
            if i!=j:                    #no delay for a single job
                for mac in range(1,len(M[0])):
                    #delay[j][i] = delay[j][i] + M[i][mac] - M[j][mac-1]        
                    w = w + M[i][mac] - M[j][mac-1]   #(kth mac time of prev job) - ((k-1)th mac time of current job)
                    if w>0:
                        delay[j][i] = delay[j][i] + w
                        w=0             #-ve delay values gets carry forwarded; +ve gets added to delay[][]
    mksp=0                  #makespan
    ind = S[0]              #stores previous job in sequence
    for job in S:
        mksp = mksp + M[job][0] + delay[job][ind]   #adds machine(mac) 1 running time & delay time for each job
        ind = job                                  #(delay time is 0 for 1st job)
    for mac in range(1,len(M[0])):
        mksp = mksp + M[ind][mac]                  #adding running time in remaining macs of last job
    return mksp


j=int(input("Enter no. of jobs:"))
m=int(input("Enter no. of machines:"))
M=[]                                          #M represents job matrix with all time entries
for i1 in range(j):                       #The time taken by each job at each machine is taken input
    S=[]
    for i2 in range(m):
        print("Enter time of Job",(i1+1),"in machine",(i2+1),":",end="")
        S.append(int(input()))
    M.append(S)
print("The job matrix is:")
for i1 in range(len(M)):
    for i2 in range(len(M[0])):
        print(M[i1][i2],"\t",end="")
    print()
print("Enter the job numbers in sequence it needs to run: ")    #The job sequence is taken input
S=[]
for i in range(j):
    S.append(int(input())-1)
res = makespanNw(M, S)
print("Makespan =",res)                 #Makespan is the time taken to complete the given sequence of jobs