""" 
Animación - Curso 2021/2022

Autores:
- Álvaro Gómez-Rey Benayas
- Ignacio Pérez Folgado
- Pablo Vera Peiró
- Alex Vera Peiró
"""

#añadimos los imports
import bpy
import math

def pos_x_loop(frm):
"""
Devuelve la posicion del objeto en el eje X para cada frame mediante una equacuion que describe una circunferencia    
t --> tiempo (un frame representa 1/24 segundos, de esta manera calculamos en que segundo nos encontramos
T--> segundos que tarda en dar una vuelta
ang--> angulo sobre el cual rotaremos
posx_origen--> posicion inicial
r--> radio de la circunferencia
posx --> posicion en la que se encontrara el objeto
"""
    t = frm/24.0  
    T = 2
    ang = t*(2*math.pi)/T    
    r = 5

    posx_origen = 0
    
    posx = posx_origen + r * math.cos(ang)

    #print(ang)

    return posx

def pos_y_loop(frm):
"""
Devuelve la posicion del objeto en el eje X para cada frame mediante una equacuion que describe una circunferencia    
t --> tiempo (un frame representa 1/24 segundos, de esta manera calculamos en que segundo nos encontramos
T--> segundos que tarda en dar una vuelta
ang--> angulo sobre el cual rotaremos
posy_origen--> posicion inicial
r--> radio de la circunferencia
posy --> posicion en la que se encontrara el objeto
"""
    t = frm/24.0

    T = 2

    ang = t*(2*math.pi)/T

    r = 5

    posy_origen = 0
    
    posy = posy_origen + r * math.sin(ang)

    print(ang)

    return posy

bpy.app.driver_namespace['pos_y'] = pos_x_loop

bpy.app.driver_namespace['pos_x'] = pos_y_loop