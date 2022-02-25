import pandas as pd                           # pandas is a software library written for the Python programming language for data manipulation and analysis
import numpy as np                            # numpy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices

def calcMkspanTft(data,job_seq):                    # Funtion to calculate the makespan time and Total Flow Time of 4 jobs on 5 machines
    exit_time = [ [0]*5 for _ in range(4) ]         # Matrix for the execution times for every job on each machines
    exec_time = [ [0]*5 for _ in range(4) ]         # Matrix for the exit times of each job on every machine

    for i in range(0,4):                            # Storing the execution times in the exec_time matrix
        for j in range(0,5):
            exec_time[i][j]=data[(job_seq[i]-1)][j]

    ini=0
    for i in range(0,5):                            # Calculating and storing the first row of the exit_time matrix
        exit_time[0][i]=exec_time[0][i]+ini
        ini=exit_time[0][i]

    tft=exit_time[0][4]                             # Declaring and initializing the tft variable to the last coloumn of the first row
    for i in range(1,4):                            # Calculating and storing the rest of the exit_time matrix
        for j in range(0,5):
            if j==0:                                
                exit_time[i][j]=exit_time[i-1][j]+exec_time[i][j]
            else:
                exit_time[i][j]=max(exit_time[i][j-1],exit_time[i-1][j])+exec_time[i][j]
            if j==4:
                tft=tft+exit_time[i][j]

    return exit_time[i][j],tft                      # returning both makespan time and tft as a tuple


# driver code below
# parsing the excel file and storing in a pandas dataframe
df = pd.read_excel("C:\Users\mail2\Documents\Soft Computing\mkspan_tft.xlsx", usecols=range(1, 6), nrows=4, skiprows=1, header=None)
data = df.to_numpy()                                                                                                    # converting the dataframe to a 2d numpy array

print("Enter Job Sequence: ")                                                                                           # taking job sequence as user input
job_seq = []
for i in range(0,4):
    job_seq.append(int(input()))

mkspan, tft = calcMkspanTft(data,job_seq)                                                                               # calling the calcMkspanTft() function

print(mkspan)                                                                                                           # displaying the results
print(tft)
