from itertools import combinations
from simpleai.search import CspProblem, backtrack, MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE, HIGHEST_DEGREE_VARIABLE

def armar_mapa(filas, columnas, cantidad_paredes, cantidad_cajas_objetivos):
    paredes = []
    cajas = []
    objetivos = []

    for pared in range(cantidad_paredes):
        paredes.append('p'+str(pared))
    for caja_objetivo in range(cantidad_cajas_objetivos):
        cajas.append('c'+str(caja_objetivo))
        objetivos.append('o'+str(caja_objetivo))

    variables = ['pj'] + cajas + objetivos + paredes 
    
    dominio = {}
    
    for var in variables:
        aux = []
        for fila in range(filas):
            for col in range(columnas):
                if var not in cajas:
                    aux.append((fila,col))
                elif (fila, col) not in [(0,0), (filas-1,0), (0, columnas-1), (filas-1, columnas-1)]:
                    aux.append((fila, col))     # Restriccion unaria - Cajas no pueden estar en las esquinas, lo saco del dominio
        dominio[var] = aux

    restricciones = []

    # No puede haber dos objetos físicos en la misma posición. Se consideran objetos a las paredes, las cajas, y el jugador
    def distinta_posicion(variables, values):
        pos1, pos2 = values
        return pos1 != pos2

    for v1, v2 in combinations(['pj']+paredes+cajas, 2):
        restricciones.append(((v1, v2), distinta_posicion))

    # Los objetivos no pueden estar en las mismas posiciones que paredes, porque impedirían ganar.
    for pared in paredes:
        restricciones.append((('pj', pared), distinta_posicion))

    # Agrego q los objetivos no pueden tener la misma posición
    for v1, v2 in combinations(objetivos,2):
        restricciones.append(((v1,v2), distinta_posicion))

    # El juego no debe estar ya ganado
    def juego_no_ganado(variables, values):
        return len(set(values)) != cantidad_cajas_objetivos

    restricciones.append((tuple(cajas+objetivos), juego_no_ganado))

    # Las cajas no deben tener más de una pared adyacente. Si la caja está en los bordes, ya tiene una adyacente.
    def menor_igual_de_una_pared_adyacente(variables, values):
        fila_caja, col_caja = values[0] # Agregamos primero en la restriccion a la caja
        #print(fila_caja, col_caja)
        pos_adyacentes = []
        if fila_caja > 0:
            pos_adyacentes.append((fila_caja-1, col_caja))
        if fila_caja < filas-1:
            pos_adyacentes.append((fila_caja+1, col_caja))
        if col_caja > 0:
            pos_adyacentes.append((fila_caja, col_caja-1))
        if col_caja < columnas-1:
            pos_adyacentes.append((fila_caja, col_caja+1))
        #print(pos_adyacentes)
        contador = 0
        for val in values:
            if val in pos_adyacentes:
                contador += 1

        esta_en_borde = fila_caja == 0 or col_caja == 0 or fila_caja == filas-1 or col_caja == columnas-1
        #print(values[0], values[1], esta_en_borde, contador)
        if esta_en_borde:
            return contador == 0
        return contador <= 1

    if len(paredes) > 1:
        for p1, p2 in combinations(paredes,2):
            for caja in cajas:
                restricciones.append(((caja, p1, p2), menor_igual_de_una_pared_adyacente))
    else:
        for caja in cajas:
                restricciones.append((tuple([caja]+paredes), menor_igual_de_una_pared_adyacente))

    problema = CspProblem(variables, dominio, restricciones)

    solucion = backtrack(
        problema,
        inference=False,
        variable_heuristic=MOST_CONSTRAINED_VARIABLE,
        value_heuristic=LEAST_CONSTRAINING_VALUE,
    )

    resultado_paredes = []
    for pared in paredes:
        resultado_paredes.append(solucion[pared])

    resultado_cajas = []
    for caja in cajas:
        resultado_cajas.append(solucion[caja])

    resultado_objetivos = []
    for obj in objetivos:
        resultado_objetivos.append(solucion[obj])

    #print(solucion)
    return (resultado_paredes, resultado_cajas, resultado_objetivos, solucion['pj'])

#print(armar_mapa(3,3,1,1))
