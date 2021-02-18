import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


class Records:
    def __init__(self):
        self.record = []
        self.mean = []



path = r'c:\KBData\BME\Human factors\git\HumanFactors'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            files.append(file)#os.path.join(r, file))
            

measurements = []
for file in files:
    measurement = pd.read_csv(file, sep=';', header=None)
    measurements.append(measurement)

morningRecords = Records()
daytimeRecords = Records()
eveningRecords = Records()



for meas in measurements:
    for ind, rec in meas.iterrows():
        hour = int(rec[0])
        print(hour)
        if hour < 10:
            morningRecords.record.append(rec)
            morningRecords.mean.append(rec[6])
        elif hour > 9 and hour < 20:
            daytimeRecords.record.append(rec)
            daytimeRecords.mean.append(rec[6])
        elif hour > 19:
            eveningRecords.record.append(rec)
            eveningRecords.mean.append(rec[6])
            
print(daytimeRecords.mean) 
plt.subplot(1,3,1)
plt.hist(morningRecords.mean, color='r')
plt.axvline(np.array(morningRecords.mean).mean(), color='k', linestyle='dashed', linewidth=1)
plt.xlabel('Reaction time [s]')
plt.title('Morning')


plt.subplot(1,3,2)
plt.hist(daytimeRecords.mean, color='c')
plt.axvline(np.array(daytimeRecords.mean).mean(), color='k', linestyle='dashed', linewidth=1)
plt.xlabel('Reaction time [s]')
plt.title('Daytime')

plt.subplot(1,3,3)
plt.hist(eveningRecords.mean, color='y')
plt.axvline(np.array(eveningRecords.mean).mean(), color='k', linestyle='dashed', linewidth=1)
plt.xlabel('Reaction time [s]')
plt.title('Evening')

