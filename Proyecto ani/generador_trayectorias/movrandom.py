import random

def movrand(m_max):
    """Obtiene un número aleatorio entre al amplitud deseada y su mitad (amplitud, amplitud/2)
    """
    mov = random.uniform(m_max/1.1, m_max)
    return mov

"""
Si en custompos calculamos x, la final es x + movrand. Para calcular la frecuencia tenemos que hacer
que el desplazamiento se aplique cada x frames.
"""