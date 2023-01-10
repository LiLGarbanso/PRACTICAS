import bpy


def crea_copias(obj, context, copy_action):
    """ Crea varias copias de un objeto y elimina las fcurves de posición

    Devuelve: colección con las copias creadas
    """

    scene = bpy.context.scene
    n = obj.n_copias

    #bpy.ops.object.select_all(action='DESELECT')

    #for obj in bpy.data.collections["Copias de "+obj.name].all_objects:
        #obj.select_set(True)
        #bpy.ops.object.delete()
    collection = bpy.data.collections.get("Copias de "+obj.name, "Ninguna")
    
    if (collection != "Ninguna"):
        for obj_aux in collection.objects:
            bpy.data.objects.remove(obj_aux, do_unlink=True)
        bpy.data.collections.remove(collection)
    

    if n > 0:
        base_collection = scene.collection

        # En lugar de dejar los objetos nuevos directamente en la colección básica,
        # creamos una. Esto facilitará el trabajo posterior
        # Si ya existe, creará otra.
        # Puede ser interesante eliminar los objetos que se crearon la última vez
        collection_name = "Copias de "+obj.name
        copies_collection = bpy.data.collections.new(collection_name)
        base_collection.children.link(copies_collection)

        original_action = obj.animation_data.action

        for i in range (n):

            # Creamos una copia del objeto obj
            # Hay que añadirlo a la colección. De lo contrario no
            # lo veremos en la escena
            new_obj = obj.copy()
            copies_collection.objects.link(new_obj)
        
            # La acción (con los fotogramas clave) no se copia. Se crea
            # una referencia. Si modificamos los fotogramas clave de
            # una copia, cambiarán todos, incluído el original
            # Si no queremos que ocurra esto, copiamos la acción, creando
            # una nueva.
            if (copy_action == False):
                new_obj.animation_data.action = original_action.copy()
            #
        #

        return copies_collection
    else:
        return False
#
