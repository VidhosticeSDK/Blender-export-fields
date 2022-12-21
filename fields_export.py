import bpy
import sys

print()
print("*****************************************************************")
print("    START")
print("*****************************************************************")
print()

file = open("C:/Users/xxxxxxxxxxxxx/Downloads/_fields_.i3d", "w")
sys.stdout = file

start_nodeId = 1
nodeId = start_nodeId
pole_Ids = []

print("""<?xml version="1.0" encoding="iso-8859-1"?>
<i3D name="VidhosticeSDK" version="1.6" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://i3d.giants.ch/schema/i3d-1.6.xsd">
 <Asset><Export program="GIANTS Editor 64bit" version="9.0.3"/></Asset>
 <Files></Files>
 <Materials></Materials>
 <Shapes></Shapes>
 <Dynamics></Dynamics>
 <Scene>""")
print("\t", '<TransformGroup name="fields" nodeId="{}">'.format(nodeId))
nodeId += 1

# obj = bpy.data.objects['Cube']  <-- depending how you want to access it.
# obj = bpy.context.active_object
if bpy.context.selected_objects != []:
    objs = bpy.context.selected_objects
    objs.sort(key = lambda o: o.name)
    for obj in objs:
        if obj.type == 'MESH':
            print("\t\t"+'<TransformGroup name="field_{}" nodeId="{}">'.format(obj.name.split()[0], nodeId))
            pole_Ids.append([nodeId, obj.name])
            nodeId += 1

            print("\t\t\t"+'<TransformGroup name="fieldDimensions" nodeId="{}">'.format(nodeId))
            nodeId += 1
            maxX = obj.data.vertices[0].co.x
            maxY = obj.data.vertices[0].co.y
            maxZ = obj.data.vertices[0].co.z
            minX = obj.data.vertices[0].co.x
            minY = obj.data.vertices[0].co.y
            minZ = obj.data.vertices[0].co.z
            for f in obj.data.polygons:
                i = 0
                for idx in f.vertices:
                    maxX = max(maxX, obj.data.vertices[idx].co.x)
                    maxY = max(maxY, obj.data.vertices[idx].co.y)
                    maxZ = max(maxZ, obj.data.vertices[idx].co.z)
                    minX = min(minX, obj.data.vertices[idx].co.x)
                    minY = min(minY, obj.data.vertices[idx].co.y)
                    minZ = min(minZ, obj.data.vertices[idx].co.z)
                    if i == 0:
                        corner1X = obj.data.vertices[idx].co.x
                        corner1Y = obj.data.vertices[idx].co.y
                        corner1Z = obj.data.vertices[idx].co.z
                        print("\t\t\t\t"+'<TransformGroup name="c1" translation="{:.3f} {:.3f} {:.3f}" nodeId="{}">'.format(corner1X, corner1Z, -corner1Y, nodeId))
                        nodeId += 1
                    elif i == 1:
                        corner2X = obj.data.vertices[idx].co.x - corner1X
                        corner2Y = obj.data.vertices[idx].co.y - corner1Y
                        corner2Z = obj.data.vertices[idx].co.z - corner1Z
                        print("\t\t\t\t\t"+'<TransformGroup name="c2" translation="{:.3f} {:.3f} {:.3f}" nodeId="{}"/>'.format(corner2X, corner2Z, -corner2Y, nodeId))
                        nodeId += 1
                    elif i == 2:
                        corner3X = obj.data.vertices[idx].co.x - corner1X
                        corner3Y = obj.data.vertices[idx].co.y - corner1Y
                        corner3Z = obj.data.vertices[idx].co.z - corner1Z
                        print("\t\t\t\t\t"+'<TransformGroup name="c3" translation="{:.3f} {:.3f} {:.3f}" nodeId="{}"/>'.format(corner3X, corner3Z, -corner3Y, nodeId))
                        nodeId += 1
                        print("\t\t\t\t"+'</TransformGroup>')
                    i += 1
            print("\t\t\t"+'</TransformGroup>')

            print("\t\t\t"+'<TransformGroup name="fieldMapIndicator" translation="{:.3f} {:.3f} {:.3f}" nodeId="{}"/>'.format(minX+(maxX-minX)/2, minZ+(maxZ-minZ)/2, -(minY+(maxY-minY)/2), nodeId))
            nodeId += 1
            print("\t\t"+'</TransformGroup>')

print("\t"+'</TransformGroup>')
print(' </Scene>')
print(' <UserAttributes>')
print("\t"+'<UserAttribute nodeId="1">'.format(start_nodeId))
print("\t\t"+'<Attribute name="nameIndicatorIndex" type="integer" value="1"/>')
print("\t\t"+'<Attribute name="onCreate" type="scriptCallback" value="FieldUtil.onCreate"/>')
print("\t"+'</UserAttribute>')

for x in pole_Ids:
    print("\t"+'<UserAttribute nodeId="{}">'.format(x[0]))
    print("\t\t"+'<Attribute name="fieldAngle" type="integer" value="0"/>')
#    print("\t\t"+'<Attribute name="name" type="string" value="test_name"/>')
    if x[1].find("nomission") != -1:
        print("\t\t"+'<Attribute name="fieldMissionAllowed" type="boolean" value="false"/>')
    if x[1].find("grass") != -1:
        print("\t\t"+'<Attribute name="fieldGrassMission" type="boolean" value="true"/>')
    print("\t\t"+'<Attribute name="fieldDimensionIndex" type="integer" value="0"/>')
    print("\t\t"+'<Attribute name="nameIndicatorIndex" type="integer" value="1"/>')
    print("\t"+'</UserAttribute>')

print(" </UserAttributes>\n"+"</i3D>")

sys.stdout = sys.__stdout__ #reset
file.close()

print()
print("*****************************************************************")
print("    END")
print("*****************************************************************")
print()

#obdata = bpy.context.object.data
#
#print('Vertices:')
#for v in obdata.vertices:
#    print('{}. {} {} {}'.format(v.index, v.co.x, v.co.y, v.co.z))
#
#print('Edges:')
#for e in obdata.edges:
#    print('{}. {} {}'.format(e.index, e.vertices[0], e.vertices[1]))
#
#print('Faces:')
#for f in obdata.polygons:
#    print('{}. '.format(f.index), end='')
#    for v in f.vertices:
#        print('{} '.format(v), end='')
#    print() # for newline
