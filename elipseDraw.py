import bpy
import bmesh
import math
import csv

mjAng = 293.927348902
a = 1.06280207723
b = 1.062794

mjAng = mjAng * math.pi/180

axr = math.cos(mjAng)
ayr = math.sin(mjAng)

bxr = -math.sin(mjAng)
byr = math.cos(mjAng)

xx = 0.68018
xy = -.36332
xz = -.63669
yx = 0.71913
yy = 0.50455
yz = 0.47778
zx = 0.14761
zy = -0.78281
zz = 0.60450


ax = (axr * xx + ayr * yx)*a
ay = (axr * xy + ayr * yy)*a
az = (axr * xz + ayr * yz)*a

bx = (bxr * xx + byr * yx)*b
by = (bxr * xy + byr * yy)*b
bz = (bxr * xz + byr * yz)*b


focDis = (a**2 - b**2)**(1/2)

#ax = r * ax/(ax**2 + ay**2 + az**2)
#ay = r * ay/(ax**2 + ay**2 + az**2)
#az = r * az/(ax**2 + ay**2 + az**2)
#bx = r * bx/(bx**2 + by**2 + bz**2)
#by = r * by/(bx**2 + by**2 + bz**2)
#bz = r * bz/(bx**2 + by**2 + bz**2)

Jn = 0
mesh = bpy.data.meshes.new("Orbit")  
obj = bpy.data.objects.new("Orbit", mesh)  
scene = bpy.context.scene
scene.objects.link(obj)  
scene.objects.active = obj  
obj.select = True 

mesh = bpy.context.object.data
bm = bmesh.new()

for i in range(0,10001):
	
    t = i * 2*math.pi/10000

    if Jn == 0:

        v1 = ((ax*math.sin(t)+bx*math.cos(t) + (ax/a)*focDis,ay*math.sin(t)+by*math.cos(t)+ (ay/a)*focDis ,az*math.sin(t)+bz*math.cos(t) + (az/a)*focDis))

        v1 = bm.verts.new(v1)
        
        Jn = 1
    else:
        v2 = ((ax*math.sin(t)+bx*math.cos(t) + (ax/a)*focDis,ay*math.sin(t)+by*math.cos(t)+ (ay/a)*focDis ,az*math.sin(t)+bz*math.cos(t) + (az/a)*focDis))

        v2 = bm.verts.new(v2)
        
        Jn = 0
    
    if i != 0:    
        bm.edges.new((v1,v2))

bm.to_mesh(mesh)  
bm.free() 