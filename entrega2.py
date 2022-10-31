from simpleai.search import CspProblem, backtrack, MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE, HIGHEST_DEGREE_VARIABLE

def armar_mapa(filas, columnas, cantidad_paredes, cantidad_cajas_objetivos):
    variables = ['pj']

    paredes = []
    cajas = []
    objetivos = []

    for pared in range(cantidad_paredes):
        paredes.append('p'+str(pared))
    for caja_objetivo in range(cantidad_cajas_objetivos):
        cajas.append('c'+str(caja_objetivo))
        objetivos.append('o'+str(caja_objetivo))

    variables = variables + paredes + cajas + objetivos
    
    dominio = {}

    for var in variables:
        aux = []
        for fila in range(filas):
            for col in range(columnas):
                if var not in cajas:
                    aux.append((fila,col))
                elif fila != 0 and fila != filas-1 and col != 0 and col != columnas-1:
                    aux.append((fila, col))
        dominio[var] = aux

    

#armar_mapa(4,5,3,5)
