import math

#__________________________________________________________
# InterpLineal(u, x1, x2)
#
# Par�metros:
#   - u: proporci�n de 0 a 1 del tiempo dentro del segmento
#   - x1: primer punto del segmento
#   - x2: segundo punto del segmento
#
# Descripci�n: Funci�n que utiliza la interpolaci�n l�neal
# para calcular el punto correspondiente al tiempo indicado
#
# Return: punto interpolado
#__________________________________________________________
def InterpLineal(u, x1, x2):
    #Formula de interpolaci�n lineal, ecuaci�n general de una recta punto/pendiente
    valor = x1 + u*(x2 - x1)
    return valor

#__________________________________________________________
# InterpHermite(u,v1,v2,x1,x2)
#
# Par�metros:
#   - u: proporci�n de 0 a 1 del tiempo dentro del segmento
#   - v1: velocidad de la curva en el primer punto
#   - v2: velocidad de la curva en el segundo punto
#   - x1: primer punto del segmento
#   - x2: segundo punto del segmento
#
# Descripci�n: Funci�n que utiliza la interpolaci�n de hermite
# para calcular el punto correspondiente al tiempo indicado con
# las velocidades del usuario
#
# Return: punto interpolado
#__________________________________________________________
def InterpHermite(u,v1,v2,x1,x2):
    #Formula de la interpolaci�n de hermite, matriz general de los polinomios de hermite
    valor = (1-(3*(u**2))+(2*(u**3)))*x1 + (u**2*(3-(2*u)))*x2 + (u*((u-1)**2))*v1 + ((u**2)*(u-1))*v2
    return valor


#__________________________________________________________
# InterpCatmun(u, x1, x2, xa, xp, t)
#
# Par�metros:
#   - u: proporci�n de 0 a 1 del tiempo dentro del segmento
#   - x1: primer punto del segmento
#   - x2: segundo punto del segmento
#   - xa: punto directamente anterior al segmento
#   - xp: punto directamente posterior al segmento
#     t: tau, tensi�n de la curva del segmento
#
# Descripci�n: Funci�n que utiliza la interpolaci�n de Catmull Rom
# para calcular el punto correspondiente al tiempo indicado con
# las velocidades que calcula la misma funci�n
#
# Return: punto interpolado
#__________________________________________________________
def InterpCatmun(u, x1, x2, xa, xp, t):

    #Condicionales para calcular la velocidad en los tramos problem�ticos

    #Tramo problem�tico, segmento inicial
    if(xa == 0):
        v1 = t*(x2 - x1)
    else:
        v1 = t*(x2 - xa)

    #Tramo problem�tico, segmento final
    if(xp == 0):
        v2 = t*(x2 - x1)
    else:
        v2 = t*(xp - x1)

    #Coeficientes para calcular la ecuaci�n general de Catmull Rom
    c0 = x1
    c1 = v1
    c2 = 3*(x2 - x1) - v2 - 2*v1
    c3 = -2*(x2 - x1) + v2 + v1

    valor = c0 + c1*u + c2*u**2 + c3*u**3

    return valor