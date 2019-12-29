import bpy
import bmesh
import math
import csv


pressComp = -5.3#deg/day
lat = <LATITUDE> * math.pi/180
rotLong = <LONGITUDE>
elevation = .08
radEq = 6378.1
flatF = 0.0033528
sideRot = 86164.100352 

radComp = (elevation + (radEq*(radEq-radEq*flatF))/math.sqrt((radEq*math.sin(lat))**2+((radEq-radEq*flatF)* math.cos(lat))**2)/radEq
print("Observation Radius")
print(radComp)
print()


with open('data.csv', newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        
        with open('verdata.csv', 'w', newline='') as csvfile:
            datawriter = csv.writer(csvfile,delimiter =',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in datareader:

                
                time = float(row[0])
                az = (float(row[1]))* math.pi/180
                alt = float(row[2]) * math.pi/180


                long = (rotLong + (time/sideRot) * 360 +  ((time/86400) *pressComp % 360))%360 * math.pi/180



                obsPosVecI = math.cos(long) * math.cos(lat) 
                obsPosVecJ = math.sin(long) * math.cos(lat) 
                obsPosVecK = math.sin(lat)

 #               print(long * 180/math.pi)
                
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

#                print("Unit Vector Check")
#                print(obsObsInfVecI**2 + obsObsInfVecJ**2 + obsObsInfVecK**2)
#                print()
            
                datawriter.writerow([obsPosVecI,obsPosVecJ,obsPosVecK,obsObsInfVecI,obsObsInfVecJ,obsObsInfVecK])


l=.3
Odd = 20
first = 0

mesh = bpy.data.meshes.new("SegDraw")  
obj = bpy.data.objects.new("SegDraw", mesh)  
scene = bpy.context.scene
scene.objects.link(obj)  
scene.objects.active = obj  
obj.select = True 

mesh = bpy.context.object.data
bm = bmesh.new()

fp = 'verdata.csv'

with open(fp, newline='') as csvfile:
	datareader = csv.reader(csvfile, delimiter=',', quotechar='|')

	v0 = bm.verts.new((0,0,0))

	for row in datareader:
			
		obsX = float(row[0]) * radComp
		obsY = float(row[1]) * radComp
		obsZ = float(row[2]) * radComp
			
		slnX = float(row[3])
		slnY = float(row[4])
		slnZ = float(row[5])	 

		if Odd == 20:		
			v1 = ((obsX,obsY,obsZ)) #XYZ
			v2 = ((obsX+slnX*l,obsY+slnY*l,obsZ+slnZ*l)) #XYZ

			v1 = bm.verts.new(v1)
			v2 = bm.verts.new(v2)

			bm.edges.new((v1, v2))
			Odd = 0
		else:
#			v3 = ((obsX,obsY,obsZ)) #XYZ
#			v4 = ((obsX+slnX*l,obsY+slnY*l,obsZ+slnZ*l)) #XYZ

#			v3 = bm.verts.new(v3)
#			v4 = bm.verts.new(v4)

#			bm.edges.new((v3, v4))
			Odd = Odd +1
		

bm.to_mesh(mesh)  
bm.free() 