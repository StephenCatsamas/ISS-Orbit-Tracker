import math
import csv
from datetime import *


#converts site alt az information to a line of sight segment

pressComp = 4 #deg/day
yr = 2017
mn = 11
dy = 13
hr = 20
mt = 33
sn = 52
lat = <OBSERVATION LATITUDE> * math.pi/180
rotLong = <OBSERVATION LONGITUDE>
elevation = .08
radEq = 6378.1
flatF = 0.0033528
sideRot = 86164.100352 

radComp = elevation + (radEq*(radEq-radEq*flatF))/math.sqrt((radEq*math.sin(lat))**2+((radEq-radEq*flatF)* math.cos(lat))**2)
print("Observation Radius")
print(radComp)
print()


epoch = datetime(year= yr, month = mn, day =dy, hour = hr, minute = mt, second = sn)
print(epoch)

with open('data.csv', newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        
        with open('out.csv', 'w', newline='') as csvfile:
            datawriter = csv.writer(csvfile,delimiter =',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in datareader:

                
                time = float(row[0])
                az = float(row[1]) * math.pi/180
                alt = float(row[2]) * math.pi/180

##                time = 0
##                az = 138.3394018 * math.pi/180
##                alt = 41.95994478 * math.pi/180
                

                frameT = epoch.toordinal()*86400 + time


                long = (rotLong + frameT/sideRot * 360 + (frameT/86400 * pressComp)%360)%360 * math.pi/180

##                long = 318.0520882 * math.pi/180
    

                obsPosVecI = math.cos(long) * math.cos(lat) 
                obsPosVecJ = math.sin(long) * math.cos(lat) 
                obsPosVecK = math.sin(lat)

                
##                print("Unit Vector Check")
##                print((obsPosVecI**2 + obsPosVecJ**2 + obsPosVecK**2))
##                print()


                obsObsVecI = math.sin(az) * math.cos(alt)
                obsObsVecJ = math.cos(az) * math.cos(alt)
                obsObsVecK = math.sin(alt)

##                print(obsObsVecI)
##                print(obsObsVecJ)
##                print(obsObsVecK)

##                print("Unit Vector Check")
##                print(obsObsVecI**2 + obsObsVecJ**2 + obsObsVecK**2)
##                print()

                obsTransII = -math.sin(long)
                obsTransIJ = math.cos(long)
                obsTransIK = 0
                obsTransJI = -math.sin(lat)*math.cos(long)
                obsTransJJ = -math.sin(lat)*math.sin(long)
                obsTransJK = math.cos(lat)
                obsTransKI = obsPosVecI
                obsTransKJ = obsPosVecJ
                obsTransKK = obsPosVecK

##                print()
##                print(obsTransII)
##                print(obsTransIJ)
##                print(obsTransIK)
##                print(obsTransJI)
##                print(obsTransJJ)
##                print(obsTransJK)
##                print(obsTransKI)
##                print(obsTransKJ)
##                print(obsTransKK)

##                print("Unit Vector Check")
##                print(obsTransII**2 + obsTransIJ**2 + obsTransIK**2)
##                print(obsTransJI**2 + obsTransJJ**2 + obsTransJK**2)
##                print(obsTransKI**2 + obsTransKJ**2 + obsTransKK**2)
##                print()


                obsObsInfVecI = (obsObsVecI * obsTransII) + (obsObsVecJ * obsTransJI) + (obsObsVecK * obsTransKI)
                obsObsInfVecJ = (obsObsVecI * obsTransIJ) + (obsObsVecJ * obsTransJJ) + (obsObsVecK * obsTransKJ)
                obsObsInfVecK = (obsObsVecI * obsTransIK) + (obsObsVecJ * obsTransJK) + (obsObsVecK * obsTransKK)

##                print("Unit Vector Check")
##                print(obsObsInfVecI**2 + obsObsInfVecJ**2 + obsObsInfVecK**2)
##                print()
            
                datawriter.writerow([obsPosVecI,obsPosVecJ,obsPosVecK,obsObsInfVecI,obsObsInfVecJ,obsObsInfVecK])
            
