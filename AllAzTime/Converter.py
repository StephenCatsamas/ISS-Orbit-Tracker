import math
import csv
from datetime import *

#adds an epoch to time data

yr = 2017
mn = 11
dy = 13
hr = 20
mt = 33
sn = 52

epoch = datetime(year= yr, month = mn, day =dy, hour = hr, minute = mt, second = sn)
print(epoch)

with open('data.csv', newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        
        with open('out.csv', 'w', newline='') as csvfile:
            datawriter = csv.writer(csvfile,delimiter =',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in datareader:

                
                time = float(row[0])
                az = float(row[1])
                alt = float(row[2])

                Stime = epoch.toordinal()*86400 + epoch.hour * 3600 + epoch.minute*60 + epoch.second + time   

                datawriter.writerow([Stime,az,alt])
            
