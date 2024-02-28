# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 13:39:04 2024

@author: Matthew
"""
import numpy as np
import time
path = r'Z:\Dropbox (UFL)\Projects\BlumenfeldUH3_START\START_Data\pDA301\SCIRun_MRtrix'

start_time = time.time()
m = np.loadtxt(path+'/whole_brain_100k.edge')
print('Edge Load:', time.time() - start_time)
start_time = time.time()
linePoints = np.loadtxt(path+'/whole_brain_100k.pts')
print('Pts Load:', time.time() - start_time,'\n')

print('\nStart Timing Original')
start_time = time.time()
lineCount = 1
EndCount = [0]
lineIndex = 0
for i in range(1,len(m)):
    if m[i,0] != m[i-1,1]:
        lineCount = lineCount + 1
        lineIndex += 1
        EndCount.append(i - 2 + lineIndex + 1)
EndCount.append(len(linePoints))
print('Elapsed Timing (s):',time.time() - start_time,'\n')


print('\nStart Timing New')
start_time = time.time()
m0 = m[1:,0]
m0 = np.append(m0,0)
m1 = m[:,1]

Ends = np.where(np.not_equal(m0,m1))[0] #Mismatch Indicates end of fiber
Ends = np.insert(Ends,0,0,axis=0)
indexer = np.arange(len(Ends))
Ends = np.add(Ends,indexer)
Ends[-1] = Ends[-1] + 1
print('Elapsed Timing (s):',time.time() - start_time,'\n')