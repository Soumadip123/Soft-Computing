def makespanNi(M, S):
    delay_array = [0]*(m)
    for i in range(1, m):
        x = M[S[0]][i-1]
        y = 0
        for k in range(1,j):
            y = y + M[S[k]][i-1] - M[S[k-1]][i]
            #print(y)
            if(y>0):
                x = x + y
                y = 0    
        delay_array[i] = delay_array[i-1] + x
    x=0
    print(delay_array)
    for i in range (j):
        x = x + M[i][m-1]
    mkspn = delay_array[m-1] + x
    return mkspn

j = int(input("Enter no. of jobs:"))
m = int(input("Enter no. of machines:"))
M = []                                      # M represents job matrix with all time entries

for i1 in range(j):                         # The time taken by each job at each machine is taken input
    S = []      
    for i2 in range(m):
        print("Enter time of Job", (i1+1), "in machine", (i2+1), ":", end="")
        S.append(int(input()))
    M.append(S)
print("The job matrix is:")
for i1 in range(len(M)):
    for i2 in range(len(M[0])):
        print(M[i1][i2], "\t", end="")
    print()
print("Enter the job numbers in sequence it needs to run: ")        # The job sequence is taken input
S = []
for i in range(j):
    S.append(int(input())-1)
res = makespanNi(M, S)

print("Makespan =", res)                            # Makespan is the time taken to complete the given sequence of jobs
