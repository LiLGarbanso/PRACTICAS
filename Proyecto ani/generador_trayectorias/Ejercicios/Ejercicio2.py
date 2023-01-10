import bpy
import os

#limpiamos la consola (para ver de manera mas comoda los errores, en caso que aparezcan)
os.system("cls")

#definimos sobre que objeto queremos sacar la información de los keyframes
obj = bpy.data.objects['Cube.001']

cx = obj.animation_data.action.fcurves.find('location',index=0)
cy = obj.animation_data.action.fcurves.find('location',index=1)

#devolvemos los valores que hemos sacado
#Fotograma 1: x = 0.0, y = 0.0
print("Esto es x: ", cx.keyframe_points[0].co[1])
print("Esto es y: ", cy.keyframe_points[0].co[1])

#Fotograma 2: x = 5.0, y = 5.0
print("Esto es x: ", cx.keyframe_points[1].co[1])
print("Esto es y: ", cy.keyframe_points[1].co[1])

#Fotograma 3: x = 0.0, y = 2.5
print("Esto es x: ", cx.keyframe_points[2].co[1])
print("Esto es y: ", cy.keyframe_points[2].co[1])
