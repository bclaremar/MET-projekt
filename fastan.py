import pandas as pd
import re
import datetime
import matplotlib.pyplot as plt
import numpy as np

from os import listdir, system
import os
import sys
import subprocess

def openImage(path):
    imageViewerFromCommandLine = {'linux':'xdg-open',
                                  'win32':'explorer',
                                  'darwin':'open'}[sys.platform]
    subprocess.Popen([imageViewerFromCommandLine, path])


# files

import glob

filenames = glob.glob('data/*')
print(filenames)
L=len(filenames)
#stations=np.empty(L)
j=0
#for files in os.walk("data/"):
for files in filenames:
    print(files,'\n')
    sts = pd.read_csv(files, sep = ";", index_col=False, skiprows=lambda x: x > 1)
    if j==0:
        stations=sts
        j+=1
    else:
        stations=pd.concat([stations,sts])

stss=stations.loc[:, 'Stationsnamn':'Stationsnummer']
print(stss.to_string(header=True, index=False))
 

file="data/smhi-opendata_1_97510_20250224_124527.csv"    
#file="data/smhi-opendata_1_97530_20250224_081022.csv"
#file="data/smhi-opendata_1_191910_20250224_081049.csv"

df = pd.read_csv(file, sep = ";", index_col=False, skiprows=lambda x: x < 9,low_memory=False)

#print(df)

# meta data
st = pd.read_csv(file, sep = ";", index_col=False, skiprows=lambda x: x > 1)
station=st['Stationsnamn'].astype('string')
print(station)

rowstokeep=[6,7]
info = pd.read_csv(file, sep = ";", index_col=False, skiprows = lambda x: x not in rowstokeep)
print(info)
lat=info["Latitud (decimalgrader)"]
lon=info["Longitud (decimalgrader)"]
alt=info["Höjd (meter över havet)"]

#df = pd.read_csv(file, sep = ";", index_col=False, skiprows = lambda x: x<9)

# timedata

df['datetime'] = pd.to_datetime(df['Datum'] + ' ' + df['Tid (UTC)'])
#print(df)

# plot
plt.figure(1)
df.plot.line(x='datetime',y='Lufttemperatur')
plt.grid()
plt.title(label=station[0])
plt.savefig("test.png")
openImage('test.png')

# statistics
yy = pd.to_datetime(df['datetime']).dt.year
#print(yy)
mm = pd.to_datetime(df['datetime']).dt.month
#print(mm)
hr = pd.to_datetime(df['datetime']).dt.hour
print(hr)

T=df["Lufttemperatur"]
#print(T)
#print(df[yy==2015])

# annual averages

# print(np.mean(T[yy==2016])) #  test

yyyy=np.unique(yy[yy>yy[0]])
L=len(yyyy)
TMyy=np.empty(L)
TXyy=np.empty(L)
TNyy=np.empty(L)
j=0
for i in yyyy:
    TMyy[j]=np.mean(T[yy==i])
    TXyy[j]=np.max(T[yy==i])
    TNyy[j]=np.min(T[yy==i])
    j+=1

plt.close()

plt.figure(2)
plt.plot(yyyy,TMyy)
plt.plot(yyyy,TXyy)
plt.plot(yyyy,TNyy)
plt.grid()
plt.title(label=station[0])
plt.savefig("year.png")
openImage('year.png')

plt.close()


# hourly averages

hru=np.unique(hr)
L=len(hru)
TMhr=np.empty(L)
j=0
for i in hru:
    TMhr[j]=np.mean(T[hr==i])
    j+=1

plt.close()

plt.figure(3)
plt.plot(hru,TMhr,'.')
plt.grid()
plt.title(label=station[0])
plt.savefig("hour.png")
openImage('hour.png')

plt.close()

