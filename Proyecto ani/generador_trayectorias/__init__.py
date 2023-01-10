bl_info = {
    "name": "Generador de trayectorias y orientacion",
    "description" : "Generador de trayectorias interpoladas para la animación y orientacion de elementos en Blender",
    "author" : "Álvaro Gómez, Ignacio Pérez, Pablo Vera, Alex Vera",
    "version" : (1, 2),
    "blender" : (2, 90, 0),
    "category" : "Object",
}

import bpy
from importlib import reload
import math
import mathutils
import os
import sys
import random

if __name__ == "generador_trayectorias":
    from . import InterpolaValores
    from . import Interpolaciones
    from . import crea_copias
    from . import movrandom
else:
    print("Cargando como script")
    import InterpolaValores
    import Interpolaciones
    import crea_copias
    import movrandom


reload(movrandom)
reload(crea_copias)
reload(Interpolaciones)
reload(InterpolaValores)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

cls()

#_______________________________________________________
# AsignaDriverOperator
# 
# Parametros:
#
# Descripción: Operador para la asignación de drivers
#_______________________________________________________
class AsignaDriverOperator(bpy.types.Operator):
    """Asignar Driver"""
    bl_idname = "object.asig_driver"
    bl_label = "Aplicar y Calcular Tabla"
    @classmethod
    def poll(cls, context):
        return context.active_object.animation_data.action.fcurves[0].keyframe_points[0] is not None

    def invoke(self, context, event):
        print("Asignando driver...")
        obj = bpy.context.active_object
        obj.driver_on = True

        bpy.app.driver_namespace['get_pos'] = custom_pos
        
        asigna_driver_posicion(obj,0,obj.metodo)
        asigna_driver_posicion(obj,1,obj.metodo)
        asigna_driver_posicion(obj,2,obj.metodo)
        
        
        obj.rotation_mode = 'QUATERNION'
        asigna_driver_rotacion(obj,0)
        asigna_driver_rotacion(obj,1)
        asigna_driver_rotacion(obj,2)
        asigna_driver_rotacion(obj,3)
        

        print("Calculando...")
        cambio_param = False
        cambio_reparam = False

        #Si está aplicada la parametrización por arco, la quitamos
        if context.active_object.par_arco == True:
            cambio_param = True
            context.active_object.par_arco = False 
        if context.active_object.aplicar_repar == True:
            cambio_reparam = True
            context.active_object.aplicar_repar = False 


        integra_longitud(context.active_object)

        #Si estaba aplicada la parametrización por arco, la volvemos a activar
        if cambio_param == True:
            context.active_object.par_arco = True
        
        #Si estaba aplicada la reparametrización por arco, la volvemos a activar
        if cambio_reparam == True:
            context.active_object.aplicar_repar = True        


        return {"FINISHED"}


#_______________________________________________________
# AsignaCopiasOperator
# 
# Parametros:
#
# Descripción: Operador para la generación de copias
#_______________________________________________________    
class AsignaCopiasOperator(bpy.types.Operator):
    """Asignar Driver"""
    bl_idname = "object.asig_copias"
    bl_label = "Generar copias"

    #obj = bpy.context.object
    #obj_act = bpy.context.active_object


    def invoke(self, context, event):
        print("Asignando copias...")
        obj_a_copiar = bpy.context.object
        crea_copias.crea_copias(obj_a_copiar,bpy.context, bpy.context.scene.EnlazarMovimiento)
        return {"FINISHED"}


#_______________________________________________________
# DesasignaDriverOperator
# 
# Parametros:
#
# Descripción: Operador para el borrado de drivers
#_______________________________________________________ 
class DesasignaDriverOperator(bpy.types.Operator):
    """Desasignar Driver"""
    bl_idname = "object.desasig_driver"
    bl_label = "Borrar drivers"

    @classmethod
    def poll(cls, context):
        return context.active_object.driver_on == True

    def invoke(self, context, event):
        if(context.active_object.driver_on == True):
           
            context.active_object.driver_remove('location',0)
            context.active_object.driver_remove('location',1)
            context.active_object.driver_remove('location',2)

            context.active_object.driver_on = False


        print("Desasignando driver...")
        return {"FINISHED"}


#_______________________________________________________
# CalculaTablaOperador
# 
# Parametros:
#
# Descripción: Operador para el cálculo de tabla de valores
#_______________________________________________________ 
class CalculaTablaOperador(bpy.types.Operator):
    """Calcula Tabla"""
    bl_idname = "object.calcula_tabla"
    bl_label = "Calcular tabla"

    @classmethod
    def poll(cls, context):
        return context.active_object.animation_data.action.fcurves[0].keyframe_points[0] is not None

    def invoke(self, context, event):
        print("Calculando...")
        cambio = False
        
        #Si está aplicada la parametrización por arco, la quitamos
        if context.active_object.par_arco == True:
            cambio = True
            context.active_object.par_arco = False 
        
        integra_longitud(context.active_object)

        #Si estaba aplicada la parametrización por arco, la volvemos a activar
        if cambio == True:
            context.active_object.par_arco = True

        

        return {"FINISHED"}
 
#_______________________________________________________
# InsertarKeyframeLon
# 
# Parametros:
#
# Descripción: Operador para insertar Keyframes de distancia recorrida
#_______________________________________________________ 
class InsertarKeyframeLon(bpy.types.Operator):
    """Insertar keyframe"""
    bl_idname = "object.insertar_kf_lon"
    bl_label = "Insertar Keyframe"

    @classmethod
    def poll(cls, context):
        return context.active_object.animation_data.action.fcurves[0].keyframe_points[0] is not None

    def invoke(self, context, event):
        print("Insertando...")
        
        f = bpy.data.scenes[0].frame_current
        print(f)
        context.active_object.keyframe_insert("distancia_recorrida",frame=f)


        return {"FINISHED"}
 
#_______________________________________________________
# InsertarKeyframeAla
# 
# Parametros:
#
# Descripción: Operador para insertar Keyframes de alabeo
#_______________________________________________________ 
class InsertarKeyframeAla(bpy.types.Operator):
    """Insertar keyframe"""
    bl_idname = "object.insertar_kf_ala"
    bl_label = "Insertar Keyframe"

    @classmethod
    def poll(cls, context):
        return context.active_object.animation_data.action.fcurves[0].keyframe_points[0] is not None

    def invoke(self, context, event):
        print("Insertando...")
        
        f = bpy.data.scenes[0].frame_current
        print(f)
        context.active_object.keyframe_insert("alabeo",frame=f)


        return {"FINISHED"}
  
 

#_______________________________________________________
# GeneradorTrayectoriasPanel
#
# Descripción: Clase para la generación del panel que 
# funcionará como interfaz de usuario
#_______________________________________________________ 
class GeneradorTrayectoriasPanel(bpy.types.Panel):

    bl_label = "Generador Trayectorias"
    bl_idname = "OBJECT_PT_GeneradorTrayectorias"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GeneradorTrayectorias"


    def draw(self, context): 
        layout = self.layout

        
        obj = bpy.context.active_object

        scene = context.scene

        #Si el objeto selecionado es una mesh y tiene animación, imprimimos la interfaz
        if obj.type == 'MESH' and obj.animation_data:
            #row = layout.row()
            #row.label(text="Desasignación de drivers", icon='WORLD_DATA')
            #row = layout.row()
            #row.operator("object.desasig_driver")
            box = layout.box()
            col = box.column()
            row = col.row()

            row = col.row()
            #___________________INTERPOLACIÓN_______________________________________________
            row.label(text="TRAYECTORIA", icon='WORLD_DATA')
            row = col.row()
            row.prop(obj, "metodo")

            #___________________INTERPOLACIÓN --> HERMITE __________________________________
            if obj.metodo == "Hermite":
                row = col.row()
                row.label(text="Velocidades", icon='WORLD_DATA')
            
                if not scene.show_velocidad:
                    row.prop(scene, "show_velocidad", icon="RIGHTARROW", text="", emboss=False)
                else:
                    row.prop(scene, "show_velocidad", icon="DOWNARROW_HLT", text="", emboss=False)
                    row = col.row()
                if scene.show_velocidad:
                    i = 0
                    
                    row.label(text="Cada fila representa las velocidades")
                    row = col.row()
                    row.label(text="(x,y,z) para cada keyframe del objeto")
                    row = col.row()
                    row.label(text="seleccionado.")
                     
                    
                    row = col.row()
                    row.label(text="X")
                    row.label(text="Y")
                    row.label(text="Z")
                    row = col.row()



                    for kf in obj.animation_data.action.fcurves[0].keyframe_points:

                        row.prop(obj, "velocidadesx", index = i) 
                        row.prop(obj, "velocidadesy", index = i) 
                        row.prop(obj, "velocidadesz", index = i) 
                        row = col.row()
                        i = i+1
        
            #___________________INTERPOLACIÓN-->CATMULL-ROM_________________________________
            if obj.metodo == "Catmull-Rom":
                row = col.row()
                row.prop(obj, "tau", slider = True)
        
            #___________________OPERADORES__________________________________________________
            row = col.row()
            row.operator("object.asig_driver")
            row = col.row()
            if(obj.driver_on == False):
                row.enabled = False
            
            row.operator("object.desasig_driver")
            
            box = layout.box()
            col = box.column()
            row = col.row()
            
            row.label(text="REPARAMETRIZACIÓN", icon='WORLD_DATA')
            row = col.row()
            row.label(text="Frec. muestreo")
            row.prop(obj, "frec_muestreo")
            
            
            #row = col.row()
            #row.operator("object.calcula_tabla")
            

            row = col.row()
            if (obj.aplicar_repar == True):
                #obj.par_arco = True
                row.enabled = False
            row.prop(obj, "par_arco")
            row = col.row()
            row.prop(obj, "aplicar_repar")
          

            if (obj.par_arco == True and obj.aplicar_repar == False):
                row = col.row()
                row.label(text="Velocidad")
                row.prop(obj, "velparametrizacion", slider = True)
            
            if (obj.par_arco == True and obj.aplicar_repar == True):
                row = col.row()
                row.label(text="Distancia recorrida")
                row.prop(obj, "distancia_recorrida")
                row = col.row()
                row.operator("object.insertar_kf_lon")


            box = layout.box()
            col = box.column()
            row = col.row()
            
            #___________________CONTROL ORIENTACIÓN__________________________________________________
            row.label(text="CONTROL ORIENTACIÓN", icon='WORLD_DATA')
            row = col.row()
            
            row.prop(obj, "ctrl_orientacion") 
            if (obj.ctrl_orientacion == True):
                row = col.row()
                row.label(text="Eje frontal")
                row = col.row()
                row.prop(obj, "eje_front")
               
                row = col.row()
                row.label(text="Eje lateral")
                row = col.row()
                row.prop(obj, "eje_lat",index=1)

                    
                row = col.row()
                row.label(text="Alabeo")
                row = col.row()
                row.prop(obj, "alabeo", slider = True)
                
                row = col.row()
                row.operator("object.insertar_kf_ala")


            row = col.row()
            box = layout.box()
            col = box.column()
            
            #___________________COPIAS_______________________________________________________
            row = col.row()
            row.label(text="COPIAS", icon='WORLD_DATA')

            if (obj.name.rfind('.') == -1):
                row = col.row()
                row.prop(scene, "EnlazarMovimiento")
                row = col.row()
                row.prop(obj, "n_copias")
                row.operator("object.asig_copias")

            box = layout.box()
            col = box.column()
            row = col.row()
            
            #___________________ALEATORIEDAD___________________________________________________
            row = col.row()
            row.label(text="ALEATORIEDAD", icon='WORLD_DATA')
            
            row = col.row()
            row.prop(obj, "amplitud", slider = True)
            row.prop(obj, "frecuencia", slider = True)
    




def ChangeEjeLateral(obj,eje):
    obj.eje_lat = eje

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

        def draw(self, context):
            self.layout.label(text=message)

        bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
#_______________________________________________________
# asigna_driver_posicion(obj,coord,method)
#
# Parámetros
#   - obj: Variable objeto a la que se aplicarán los drivers
#   - method: Método utilizado para la interpolación
#   - coord: Eje sobre el que se aplica la interpolación (x,y,z)
#
# Descripción: Función para la signación de drivers
#_______________________________________________________ 
def asigna_driver_posicion(obj,coord,method):
    # Creamos el driver en la coordenada elegida. El driver se queda
    # guardado en la variable drv
    drv = obj.driver_add('location',coord).driver
    # Habilitamos la posibilidad de que reciba el propio objeto, que
    # necesitaremos para acceder a los fotogramas clave.
    drv.use_self = True
    # Asignamos la expresión que queremos que se utilice.
    # Se está utilizando una "f-string" para constuir una cadena
    # a partir del valor de las variables coord y method
    drv.expression = f"get_pos(frame, self, {coord}, '{method}')"

    

#_______________________________________________________
# asigna_driver_posicion(obj,coord,method)
#
# Parámetros
#   - obj: Variable objeto a la que se aplicarán los drivers
#   - method: Método utilizado para la interpolación
#   - coord: Eje sobre el que se aplica la interpolación (x,y,z)
#
# Descripción: Función para la signación de drivers
#_______________________________________________________ 
def asigna_driver_rotacion(obj,elemento):
    # Creamos el driver en la coordenada elegida. El driver se queda
    # guardado en la variable drv
    drv = obj.driver_add('rotation_quaternion',elemento).driver
    # Habilitamos la posibilidad de que reciba el propio objeto, que
    # necesitaremos para acceder a los fotogramas clave.
    drv.use_self = True
    # Asignamos la expresión que queremos que se utilice.
    # Se está utilizando una "f-string" para constuir una cadena
    # a partir del valor de las variables coord y method
    drv.expression = f"get_rot(frame, self, {elemento})"



#_______________________________________________________
# integra_longitud
#
# Parámetros
#   - obj: Variable objeto de la que se desea calcular la tabla de valores
#
# Descripción: Función para la obtención de la tabla de valores
#_______________________________________________________ 
def integra_longitud(obj):
    #Limpiamos la colección
    obj.colec.clear()

    #Variable auxiliar de la distancia previa recorrida
    last_length = 0

    #Variable para determinar la frecuencia de muestreo
    muestreo = obj.frec_muestreo

    #Comprobaciones del objeto activo (pese a que no entra aquí si no existe animación en el objeto)
    print("El objeto impreso es: ", obj.name)
    
    #Frame del kf 0 y del último kf
    min = obj.animation_data.action.fcurves[0].keyframe_points[0].co[0] #kf inicial
    print("Mínimo: ", min)

    max = obj.animation_data.action.fcurves[0].keyframe_points[-1].co[0] #kf final
    print("Fotogramas necesarios: ", max-min)

    #Variable auxiliar para calcular la duración de al animación
    ftg_totales = max-min
    #i = min, pero convertido a entero
    i = int(min)

    #booleano que decide si es la primera iteración, para dejar las variables distancia de arco (en x,y,z) como 0 (Porque todavía no se ha avanzado)
    primero = True

    #Bucle para cada fotograma de la animación
    #Ej.: Si el primer kf está en el frame 10 y el último en el 50, se ejecutará 40 veces (50-10)
    while(i <= int(max)):

        #Variables usadas
            # - pos_f_eje = diferencia de posiciones p(i-1) y p(i)
            # - poseje = posición actual en cada eje
            # - pos_eje_old = posición anterior en cada eje
            # - last_length = distancia de arco recorrida en t = i-1



        #Calculamos las posiciones según el método para obtener cada uno de los puntos por cada frame.
        posx = custom_pos(i,obj,0,obj.metodo)
        posy = custom_pos(i,obj,1,obj.metodo)
        posz = custom_pos(i,obj,2,obj.metodo)
        
        #Si no es la primera iteración, calculamos la diferencia de posición
        if (primero == False):
            pos_f_x = posx - pos_x_old
            pos_f_y = posy - pos_y_old
            pos_f_z = posz - pos_z_old

        #Si sí lo es, la diferencia de posición es 0
        else:
            pos_f_x = 0
            pos_f_y = 0
            pos_f_z = 0
            primero = False

        #Calculamos el módulo
        distancia = math.sqrt((pos_f_x**2)+(pos_f_y**2)+(pos_f_z**2)) + last_length
        
        #Guardamos el punto actual como el próximo anterior
        pos_x_old = posx
        pos_y_old = posy
        pos_z_old = posz

        #Añadimos el elemento a la lista
        elemento = obj.colec.add()
        elemento.fotograma = i
        elemento.distancia = distancia

        #Guardamos la distancia actual como la recorrida para la siguiente iteración
        last_length = distancia

        print("Fotograma: ", elemento.fotograma)
        print("Distancia: ", elemento.distancia)
        print(" ")
        
        #Siguiente iteración --> i++ (Si muestreamos con frecuencia 1)
        i = i + muestreo    #Determina los pasos para muestrear
    
    #Llamada de prueba a parametro_de_longitud
    #parametro_de_longitud(obj,31)
    


#_______________________________________________________
# parametro_de_longitud
#
# Parámetros
#   - obj: Variable objeto de la que se desea calcular la posición
#   - lon: Longitud que se desea alcanzar
# Descripción: Función para la obtención de la tabla de valores
#_______________________________________________________ 
def parametro_de_longitud(obj,lon):
   
    #Frame del kf 0 y del último kf
    min = obj.animation_data.action.fcurves[0].keyframe_points[0].co[0] #kf inicial
    max = obj.animation_data.action.fcurves[0].keyframe_points[-1].co[0] #kf final
    

    #Iterador
    i = min

    #Bucle for para recorrer la tabla
    for elemento in obj.colec:
        
        
        if (i == max or lon <= elemento.distancia):
            #Si se encuentra el frame en el que la longitud deseada ha sido sobrepasada, se guarda  y salimos del bucle
            break

        else:
            #Si no, seguimos iterando
            #print("Fotograma vector:", elemento.fotograma)
            #print("Distancia vector:", elemento.distancia)
            #print(" ")
            i = i + 1
    
    #Comprobación de resultados
    #print("Se alcanza en: ", obj.colec[int(i-min)].fotograma, ", que tiene valor: ", obj.colec[int(i-min)].distancia)




    if (lon == obj.colec[int(i-min)].distancia):
        #Si la longitud se alcanza en el un frame concreto, se devuelve la distancia en ese frame
        return obj.colec[int(i-min)].fotograma

    elif (i-min >= max):
        return obj.colec[-1].fotograma

    else:
        #Si no, interpolamos los valores de los dos frames necesarios y sus distancias para calcular el valor necesario donde 
        #la distancia en t = lon (donde t se mide en fotogramas)
        u = (lon - obj.colec[int(i-min-1)].distancia)/(obj.colec[int(i-min)].distancia-obj.colec[int(i-min-1)].distancia)
        
        valor = Interpolaciones.InterpLineal(u, obj.colec[int(i-min-1)].fotograma, obj.colec[int(i-min)].fotograma)

        #print("Valor: ",valor)

        return valor

      



#_______________________________________________________
# custom_pos(frame, obj, coord, method):
#
# Parámetros
#   - frame: Frame actual
#   - obj: Variable objeto a la que se aplicarán los drivers
#   - method: Método utilizado para la interpolación
#   - coord: Eje sobre el que se aplica la interpolación (x,y,z)
#
# Descripción: Función para la obtención de la posición
#_______________________________________________________ 
def custom_pos(frame, obj, coord, method):
   
    

    velocidad = obj.velparametrizacion #metros por segundo de arco

    #Obtenemos el fotograma en el que empieza la animación
    min = obj.animation_data.action.fcurves[0].keyframe_points[0].co[0] #kf inicial

    #Obtenemos el fotograma en el que acaba la animación
    max = len(obj.animation_data.action.fcurves[0].keyframe_points) #numero de kf del objeto
    
    #Reseteamos la variable pos
    pos = 0

    #Calculamos t respecto a los frames/s
    t = frame/24.0
    #t = frame/bpy.context.scene.render.fps #para estandarizar en caso de que se modificasen los fps

    #Obtenemos el booleano que decide si hay parametrización por arco
    param = obj.par_arco

    #Si queremos parametrización por arco, calculamos el frame en el que nos encontraríamos, si no, usamos el actual
    if param == True and obj.aplicar_repar == False:
        pos_deseada = velocidad * t
        f = parametro_de_longitud(obj,pos_deseada) #Llamada a parametro_de_longitud
   
    elif obj.aplicar_repar == True:

        #pos_kf = obj.animation_data.action.fcurves.find('distancia_recorrida',index=0)
        #print("Prueba: ", pos_kf.keyframe_points[0].co[0], ", ", pos_kf.keyframe_points[0].co[1])
        
        """Con esta implementación, blender interpola nuestros valores de distancia_recorrida"""
        #f = parametro_de_longitud(obj,obj.distancia_recorrida)
        
        aux = obj.animation_data.action.fcurves.find('distancia_recorrida',index=0)
        
        i = 0
        
        if (aux is not None):
        
        #    print("Tam:", len(aux.keyframe_points))

            while (i < len(aux.keyframe_points)-1) and (frame > aux.keyframe_points[i].co[0]):
                i = i+1
            
            #print("i:", i)
            if (frame >= aux.keyframe_points[-1].co[0]):
                f = parametro_de_longitud(obj,aux.keyframe_points[-1].co[1])
                print("Hola")
            if (aux.keyframe_points[i-1].co[0] == frame):
                f = parametro_de_longitud(obj,aux.keyframe_points[i-1].co[1])
            
            else:
                u = (frame - aux.keyframe_points[i-1].co[0])/(aux.keyframe_points[i].co[0]-aux.keyframe_points[i-1].co[0])
                valor = Interpolaciones.InterpLineal(u, aux.keyframe_points[i-1].co[1], aux.keyframe_points[i].co[1])
                f = parametro_de_longitud(obj,valor) #Llamada a parametro_de_longitud
        else:
            f = 0

    else:
        f=frame

    if obj.frecuencia > 0:
        T = 1.0/obj.frecuencia
        ang = t*(2*math.pi)/T
    else:
        T = 0
        ang = 0
        

    #Si el kf actual no supera el numero maximo de kf y el frame actual es mayor que el frame del kf en el que nos
    #encontramos, pasa al siguente kf

    i = 0  #esta variable indica en que kf nos encontramos siendo 0 en primero y n-1 el ultimo

    #Bucle para encontrar el segmento de kf en el que se encuentra el frame 
    while (i < max) and (f > obj.animation_data.action.fcurves[0].keyframe_points[i].co[0]):
        i = i+1
    
    #Obtenemos el vector de velocidades para la interpolación de Hermite
    if coord == 0:
        v_aux = obj.velocidadesx
    elif coord == 1:
        v_aux = obj.velocidadesy
    else:
        v_aux = obj.velocidadesz


    #Almacenamos información sobre los keyframes
    pos_kf = obj.animation_data.action.fcurves.find('location',index=coord)

    #Calculamos la posicion del objeto
    if (i == 0):
        pos = pos_kf.keyframe_points[0].co[1]
    elif (i == 1):
        pos = InterpolaValores.Interpola(f, pos_kf.keyframe_points[i-1].co[0], pos_kf.keyframe_points[i].co[0], pos_kf.keyframe_points[i-1].co[1], pos_kf.keyframe_points[i].co[1], 0, pos_kf.keyframe_points[i+1].co[1], v_aux[i-1], v_aux[i], method, obj.tau)
    elif (i == max-1):
        pos = InterpolaValores.Interpola(f, pos_kf.keyframe_points[i-1].co[0], pos_kf.keyframe_points[i].co[0], pos_kf.keyframe_points[i-1].co[1], pos_kf.keyframe_points[i].co[1], pos_kf.keyframe_points[i-2].co[1], 0, v_aux[i-1], v_aux[i], method, obj.tau)
    elif (i >= max):
        pos = 0
    else:
        pos = InterpolaValores.Interpola(f, pos_kf.keyframe_points[i-1].co[0], pos_kf.keyframe_points[i].co[0], pos_kf.keyframe_points[i-1].co[1], pos_kf.keyframe_points[i].co[1], pos_kf.keyframe_points[i-2].co[1], pos_kf.keyframe_points[i+1].co[1], v_aux[i-1], v_aux[i], method, obj.tau)


    #Calculamos el ruido

    # - Amplitud aleatoria
    if (obj.amplitud > 0 and ang > 0):
        ampx = movrandom.movrand(obj.amplitud)
        ampy = movrandom.movrand(obj.amplitud)
    else:
        ampx = 0
        ampy = 0   
    
    # - Desfase aleatorio
    if (obj.desfase0 == 0):
        obj.desfase0 = random.uniform(0.01, 3.14)
    if (obj.desfase1 == 0):
        obj.desfase1 = random.uniform(0.01, 3.14)

    # - Ruido para x e y (no para z, por elección propia, perosería perfectamente aplicable)
    
    if(coord == 0):
        if (ang > 0):
            return (pos + ampx*math.sin(ang + obj.desfase0))                # X CON RUIDO
        else:
            return pos                                                      # X SIN RUIDO

    
    if(coord == 1):
        if (ang > 0):
            return (pos + ampy*math.sin(ang + obj.desfase1))                # Y CON RUIDO
        else:
            return pos                                                      # Y SIN RUIDO
    
    else:
        return (pos)                                                        #Z



def get_quat_from_vecs(u,v):
    
    u.normalize()
    v.normalize()
    
    #Hacemos el producto vectorial
    perpendicular = u.cross(v)
    
    #Normalizamos
    perpendicular.normalize()
    
    #Producto escalar
    angulo = math.acos(u.dot(v))
    
    #Calculamos y devolvemos el quaternion
    q = mathutils.Quaternion(perpendicular,angulo)
    
    return q


def get_quat_rot(arriba,tangente,lateral,alabeo):
    #Hacemos el producto vectorial
    perpendicular = arriba.cross(tangente)
    
    #Normalizamos
    perpendicular.normalize()
    lateral.normalize()
    
    #Calculamos el ángulo
    producto = lateral.dot(perpendicular)

    #Corregimos el error
    if (producto < -1 and producto > -1.1):
        producto = -1
    elif (producto > 1 and producto < 1.1):
        producto = 1

    angulo = alabeo + math.acos(producto)
    
    #Calculamos y devolvemos el quaternion
    q = mathutils.Quaternion(tangente,angulo)
    
    return q
  

def obtener_quaternion(obj, tangente):
    
    #Establecemos las variables según la rotación a aplicar
       

    if(obj.eje_front == 'x'):
        frontal = mathutils.Vector((1.0, 0.0, 0.0))
    elif(obj.eje_front == '-x'):
        frontal = mathutils.Vector((-1.0, 0.0, 0.0))
    elif(obj.eje_front == 'y'):
        frontal = mathutils.Vector((0.0, 1.0, 0.0))
    elif(obj.eje_front == '-y'):
        frontal = mathutils.Vector((0.0, -1.0, 0.0))
    elif(obj.eje_front == 'z'):
        frontal = mathutils.Vector((0.0, 0.0, 1.0))    
    else:
        frontal = mathutils.Vector((0.0, 0.0, -1.0))
        
    
    if(obj.eje_lat == 'x'):
        lateral = mathutils.Vector((1.0, 0.0, 0.0))
    elif(obj.eje_lat == '-x'):
        lateral = mathutils.Vector((-1.0, 0.0, 0.0))
    elif(obj.eje_lat == 'y'):
        lateral = mathutils.Vector((0.0, 1.0, 0.0))
    elif(obj.eje_lat == '-y'):
        lateral = mathutils.Vector((0.0, -1.0, 0.0))
    elif(obj.eje_lat == 'z'):
        lateral = mathutils.Vector((0.0, 0.0, 1.0))
    else:
        lateral = mathutils.Vector((0.0, 0.0, -1.0))

    arriba = frontal.cross(lateral)
   
    
    
    #Calculamos el quaternion del ajuste de la dirección "frontal"   
    q = get_quat_from_vecs(frontal,tangente)
    
    
    #Calculamos e'
    lateral_actual = lateral.copy()
    lateral_actual.rotate(q)
    
    
    #Calculamos el quaternion del ajuste de la dirección lateral    
    q1 = get_quat_rot(arriba,tangente,lateral_actual,obj.alabeo)
    
    #Apilamos ambas rotaciones
    q2 = q1 @ q
    
    #Calculamos el quaternion del ajuste de la dirección "arriba" 
    #q3 = mathutils.Quaternion(tangente,math.pi)
    
    #Apilamos ambas rotaciones
    #q4 = q3 @ q2
    
    
    return q2
    
   

#_______________________________________________________
# custom_quat(frame, obj, coord):
#
# Parámetros
#   - frame: Frame actual
#   - obj: Variable objeto a la que se aplicarán los drivers
#   - coord: ?????? (x,y,z)
#
# Descripción: Función para la obtención del cuaternión de la orientación
#_______________________________________________________ 

def custom_quat(frame, obj, elemento):



    if (obj.ctrl_orientacion == True):
        cp_actual_x = custom_pos(frame, obj, 0, obj.metodo)
        cp_actual_y = custom_pos(frame, obj, 1, obj.metodo)
        cp_actual_z = custom_pos(frame, obj, 2, obj.metodo)

        cp_next_x = custom_pos(frame+1, obj, 0, obj.metodo)
        cp_next_y = custom_pos(frame+1, obj, 1, obj.metodo)
        cp_next_z = custom_pos(frame+1, obj, 2, obj.metodo)


        

        tan = mathutils.Vector((cp_next_x - cp_actual_x, cp_next_y - cp_actual_y, cp_next_z - cp_actual_z))

        tan.normalize()

        #print("___________________________________________________")

        #print("tangente:", tan)

        #print("cp_actual_x:", cp_actual_x)
        #print("cp_actual_y:", cp_actual_y)
        #print("cp_actual_z:", cp_actual_z)

        #print("cp_next_x:", cp_next_x)
        #print("cp_next_y:", cp_next_y)
        #print("cp_next_z:", cp_next_z)

        #print("x:", cp_next_x - cp_actual_x)
        #print("y:", cp_next_y - cp_actual_y)
        #print("z:", cp_next_z - cp_actual_z)

        #print("___________________________________________________")
        #   PROVISIONAL
        alabeo = 0

        q = obtener_quaternion(obj,tan)
        
        return q[elemento]
    else:
        return obj.rotation_quaternion[elemento]
    #obj.rotation_quaternion[0] = q[0]
    #obj.rotation_quaternion[1] = q[1]
    #obj.rotation_quaternion[2] = q[2]
    #obj.rotation_quaternion[3] = q[3]






#_______________________________________________________
# Register()
#_______________________________________________________ 
def register():

    #Registramos los drivers
    bpy.app.driver_namespace['get_pos'] = custom_pos
    bpy.app.driver_namespace['get_rot'] = custom_quat

    #Registramos las clases y operadores
    bpy.utils.register_class(AsignaCopiasOperator)          #Operador para las copias
    bpy.utils.register_class(GeneradorTrayectoriasPanel)    #Clase para la interfaz
    bpy.utils.register_class(AsignaDriverOperator)          #Operador para aplicación de drivers
    bpy.utils.register_class(DesasignaDriverOperator)       #Operador para borrado de drivers
    bpy.utils.register_class(CalculaTablaOperador)          #Operador el cálculo de la tabla
    bpy.utils.register_class(InsertarKeyframeLon)           #Operador insertar keyframes de distancia_recorrida
    bpy.utils.register_class(InsertarKeyframeAla)           #Operador insertar keyframes de alabeo

    #Registramos la propiedad objeto "método", que decide la interpolación
    bpy.types.Object.metodo = bpy.props.EnumProperty(
            name="Método",
            description="Método de interpolación.",
            items=[ ('Lineal', "Lineal", ""),
                    ('Hermite', "Hermite", ""),
                    ('Catmull-Rom', "Catmull-Rom", ""),
                   ]
            )
    
    #Registramos un booleano que decide si mostrar la tabla de velocidades
    bpy.types.Scene.show_velocidad = bpy.props.BoolProperty(name='Velocidades', default=False) 

    #Registramos el vector de velocidades para cada eje para Hermite
    bpy.types.Object.velocidadesx = bpy.props.FloatVectorProperty(subtype = "NONE", name = "Velocidad x", precision=4, size=32)
    bpy.types.Object.velocidadesy = bpy.props.FloatVectorProperty(subtype = "NONE", name = "Velocidad y", precision=4, size=32)
    bpy.types.Object.velocidadesz = bpy.props.FloatVectorProperty(subtype = "NONE", name = "Velocidad z", precision=4, size=32)

    #Registramos el desfase de x,y para el ruido
    bpy.types.Object.desfase0 = bpy.props.FloatProperty(name = "Desfase x", description="Desfase de onda x",min = 0,default = 0, max = math.pi)
    bpy.types.Object.desfase1 = bpy.props.FloatProperty(name = "Desfase y", description="Desfase de onda y",min = 0,default = 0, max = math.pi)

    #Registramos la velocidad de hermite (OBSOLETA)
    bpy.types.Object.velocidad = bpy.props.FloatProperty(name = "Velocidad", description="Velocidad Hermite",min = 0,default = 1, max = 20)
    
    #Registramos la amplitud del ruido para un objeto
    bpy.types.Object.amplitud = bpy.props.FloatProperty(name = "Amplitud", description="Frecuencia del ruido",min = 0,default = 1,max = 2)
    
    #Registramos la frecuencia del ruido para un objeto
    bpy.types.Object.frecuencia = bpy.props.FloatProperty(name = "Frecuencia", description="Amplitud del ruido",min = 0,default = 0,max = 5)
    
    #Registramos un boleano para decidir si las copias también heredan los keyframes
    bpy.types.Scene.EnlazarMovimiento = bpy.props.BoolProperty(name = "Enlazado de keyframes", description="Enlazar el movimiento de todos los objetos",default = True)
    
    #Registramos el número de copias por objeto
    bpy.types.Object.n_copias = bpy.props.IntProperty(name = "NºCopias", description="Número de copias",min = 0,default = 10)
    
    #Registramos TAU (Catmull-Rom)
    bpy.types.Object.tau = bpy.props.FloatProperty(name = "Tau", description="Tensión",min = 0,default = 1,max = 2)

    #Creamos clase "ParejaValores" que guarda fotograma y distancia
    class ParejasValores(bpy.types.PropertyGroup):
        fotograma : bpy.props.IntProperty(name="Fotograma", default=0)
        distancia : bpy.props.FloatProperty(name="Distancia", default=0)

    #Registramos clase "ParejaValores"
    bpy.utils.register_class(ParejasValores)

    #Registramos colección que almacena instancias de ParejasValores
    bpy.types.Object.colec = bpy.props.CollectionProperty(type=ParejasValores)

    #Registramos booleano que decide si aplicar parametrización por arco
    bpy.types.Object.par_arco = bpy.props.BoolProperty(name = "Parametrización por arco", description="Aplicar parametrización por arco", default = False)

    #Registramos el valor que determina la frecuencia de muestreo(en frames) para rellenar la tabla de distancias
    bpy.types.Object.frec_muestreo = bpy.props.IntProperty(name = "", description="Frecuencia en frames a la que se muestrea la trayectoria",min = 1,default = 1, max = 10)

    #Registramos el valor que determina la velocidad constante usada para la parametrización por arco
    bpy.types.Object.velparametrizacion = bpy.props.FloatProperty(name = "",unit = 'VELOCITY', description="Velocidad constante para la parametrización por arco",min = 1, max = 100 ,default = 10)

    #Registramos el valor que almacena la distancia que el usuario desea que se haya recorrido en cierto punto de la animación.
    bpy.types.Object.distancia_recorrida = bpy.props.FloatProperty(options={'ANIMATABLE'},name = "", description="Distancia que debe de haber recorrido el objeto en un frame determinado", min = 0 ,default = 0)

    #Registramos booleano que decide si reparametrizar la curva
    bpy.types.Object.aplicar_repar = bpy.props.BoolProperty(name = "Reparametrización de la curva", description="Recorrer la trayectoria con velocidad controlada por usuario", default = False)
    
    #Registramos booleano que decide si reparametrizar la curva
    bpy.types.Object.driver_on = bpy.props.BoolProperty(default = False)

    #Registramos booleano que decide si aplicar parametrización por arco
    bpy.types.Object.ctrl_orientacion = bpy.props.BoolProperty(name = "Control de Orientación", description="Aplicar el control de la orientación en función de la trayectoria de la curva", default = False)

    #Registramos la propiedad objeto "eje_front", que decide el eje usado para orientar el frontal del objeto
    bpy.types.Object.eje_front = bpy.props.EnumProperty(
            name="",
            description="Eje usado para dirigir el objeto hacia la tangente de la curva.",
            items=[ ('x', "X", ""),
                    ('-x', "X negativo", ""),
                    ('y', "Y", ""),
                    ('-y', "Y negativo", ""),
                    ('z', "Z", ""),
                    ('-z', "Z negativo", ""),
                   ]
            )

    #Registramos la propiedad objeto "eje_lat", que decide el eje usado para representar el lateral del objeto
    bpy.types.Object.eje_lat = bpy.props.EnumProperty(
            name="",
            description="Eje usado para representar el lateral del objeto.",
            items=[ ('x', "X", ""),
                    ('-x', "X negativo", ""),
                    ('y', "Y", ""),
                    ('-y', "Y negativo", ""),
                    ('z', "Z", ""),
                    ('-z', "Z negativo", ""),
                   ])
            # NO SÉ SI SE PUEDE HACER ESTO
            #if (bpy.types.Object.eje_front == "x"):
            #    items=[ 
            #            ('y', "y", ""),
            #            ('z', "z", ""),
            #        ]
            #elif (bpy.types.Object.eje_front == "y"):
            #    items=[ 
            #            ('x', "x", ""),
            #            ('z', "z", ""),
            #        ]
            #else:
            #    items=[ 
            #            ('x', "x", ""),
            #            ('y', "y", ""),
            #        ]
            
    

    #Registramos el valor que determina la frecuencia de muestreo(en frames) para rellenar la tabla de distancias
    bpy.types.Object.alabeo = bpy.props.FloatProperty(name = "Alabeo", description="Inclinación del objeto (roll) en RADIANES sobre el eje que apunta a la tangente",min = -math.pi/2,default = 0, max = math.pi/2 )


#_______________________________________________________
# Unregister()
#_______________________________________________________ 
def unregister():
    del bpy.types.Object.desfase0
    del bpy.types.Object.desfase1
    del bpy.types.Object.velocidadesx
    del bpy.types.Object.velocidadesy
    del bpy.types.Object.velocidadesz
    del bpy.types.Scene.show_velocidad
    del bpy.app.driver_namespace['get_pos']
    del bpy.app.driver_namespace['get_rot']
    del bpy.types.Object.amplitud
    del bpy.types.Object.frecuencia
    del bpy.types.Object.velocidad
    bpy.utils.unregister_class(AsignaCopiasOperator)
    bpy.utils.unregister_class(GeneradorTrayectoriasPanel)
    bpy.utils.unregister_class(AsignaDriverOperator)
    bpy.utils.unregister_class(DesasignaDriverOperator)
    bpy.utils.unregister_class(CalculaTablaOperador)
    bpy.utils.unregister_class(ParejasValores)
    bpy.utils.unregister_class(InsertarKeyframeLon)  
    del bpy.types.Object.n_copias
    del bpy.types.Object.metodo
    del bpy.types.Scene.EnlazarMovimiento
    del bpy.types.Object.velocidades1
    del bpy.types.Object.velocidades2
    del bpy.types.Object.tau
    del bpy.types.Object.colec
    del bpy.types.Object.par_arco
    del bpy.types.Object.frec_muestreo
    del bpy.types.Object.velparametrizacion
    del bpy.types.Object.distancia_recorrida
    del bpy.types.Object.aplicar_repar
    del bpy.types.Object.driver_on
    del bpy.types.Object.ctrl_orientacion
    del bpy.types.Object.eje_front
    del bpy.types.Object.eje_lat
    del bpy.types.Object.alabeo
    
if __name__ == "__main__":
    register()

