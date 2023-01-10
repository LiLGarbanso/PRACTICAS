from . import Interpolaciones
#import Interpolaciones
"""
Interpola(f, f1, f2, x1, x2, met)

f --> frame actual, del cual queremos obtener la posición
f1--> keyframe anterior
f2--> keyframe siguiente
x1--> coordenadas del keyframe anterior
x2--> coordenadas del keyframe siguiente
met--> metodo de interpolación que queremos utilizar

"""
#__________________________________________________________
# Interpola(f, f1, f2, x1, x2, xa, xp, v1, v2, t, met)
#
# Parámetros:
#   - f: frame actual, del cual queremos obtener la posición
#   - f1: keyframe anterior
#   - f2: keyframe siguiente
#   - x1: coordenadas del keyframe anterior
#   - x2: coordenadas del keyframe siguiente
#   - xa: coordenadas del keyframe directamente anterior al segmento (solo se utiliza en Catmull)
#   - xp: coordenadas del keyframe directamente posterior al segmento (solo se utiliza en Catmull)
#     v1: velocidad de la curva en el primer keyframe del segmento (solo se utiliza en Hermite)
#     v2: velocidad de la curva en el segunda keyframe del segmento (solo se utiliza en Hermite)
#     t: tau, tensión de la curva del segmento (solo se utiliza en Camull)
#     met: metodo de interpolación que queremos utilizar
#
# Descripción: Función que gestiona con que método de interpolación
# calcularemos la posición del frame actual
#
# Return: punto interpolado
#__________________________________________________________
def Interpola(f, f1, f2, x1, x2, xa, xp, v1 ,v2, met, tau):

    u = (f-f1)/(f2-f1)

    if (met == 'Lineal'):
        valor = Interpolaciones.InterpLineal(u, x1, x2)
    elif (met == 'Hermite'):
        valor = Interpolaciones.InterpHermite(u,v1,v2,x1,x2)
    elif (met == 'Catmull-Rom'):
        valor = Interpolaciones.InterpCatmun(u,x1,x2, xa, xp, tau)
    else:
        valor = 0
    return valor