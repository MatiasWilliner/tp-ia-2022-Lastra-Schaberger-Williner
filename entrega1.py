from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    limited_depth_first,
    iterative_limited_depth_first,
    astar,
    greedy,
)
from simpleai.search.viewers import WebViewer, BaseViewer

def jugar(paredes, cajas, objetivos, jugador, maximos_movimientos):
    # El estado va a estar conformado de la siguiente manera:
    # (pos_pj, mov_restantes, listado_cajas)
    # ((fila, col), 30, ((fila, col), (fila, col), (fila, col), (fila, col)))
    INICIAL = (jugador, maximos_movimientos, tuple(cajas))
    PAREDES = tuple(paredes)
    OBJETIVOS = tuple(objetivos)
    TAMANIO_TABLERO = max(PAREDES)

    resultado_secuencia = []

    MOVIMIENTOS = {
        "arriba" : (-1,0),
        "abajo" : (1,0),
        "izquierda" : (0, -1),
        "derecha" : (0, 1)
    }

    class SocobanProblem(SearchProblem):
        def is_goal(self, state):
            _, movimientos, cajas = state

            objetivos_cubiertos = True
            for objetivo in OBJETIVOS:
                if objetivo not in cajas:
                    objetivos_cubiertos = False
            return movimientos > 0 and objetivos_cubiertos

        # las acciones serán (pos_nueva, movimiento)
        # ejemplo ((3,3), "izquierda")
        def actions(self, state):
            pos_pj, movimientos, cajas = state
            fila, col = pos_pj
            acciones_posibles = []

            if movimientos == 0:
                return acciones_posibles

            adyacentes = []
            if fila > 0:
                adyacentes.append(((fila-1, col), "arriba"))
            if fila < TAMANIO_TABLERO[0]:
                adyacentes.append(((fila+1, col), "abajo"))
            if col > 0:
                adyacentes.append(((fila, col-1), "izquierda"))
            if col < TAMANIO_TABLERO[1]:
                adyacentes.append(((fila, col+1), "derecha"))

            for ady in adyacentes:
                if ady[0] not in PAREDES:
                    if ady[0] not in cajas:
                        acciones_posibles.append(ady)
                    else:
                        fila_nueva, col_nueva = ady[0]
                        movimiento = MOVIMIENTOS[ady[1]]
                        pos_siguiente = (fila_nueva + movimiento[0], col_nueva + movimiento[1])
                        if pos_siguiente not in PAREDES and pos_siguiente not in cajas:
                            acciones_posibles.append(ady)

            return acciones_posibles
                   
        def result(self, state, action):
            (fila, col), movimientos, cajas = state
            cajas_modificables = [list(caja) for caja in cajas]
            pos_nueva, accion = action

            if pos_nueva not in cajas:
                #resultado_secuencia.append((accion))
                return (pos_nueva, movimientos-1, cajas)
            
            indice = 0
            for index, caja in enumerate(cajas):
                if pos_nueva == caja:
                    indice = index
                    break
            movimiento = MOVIMIENTOS[accion]
            fila_caja_mover, col_caja_mover = cajas_modificables[indice]
            cajas_modificables[indice] = [fila_caja_mover + movimiento[0], col_caja_mover + movimiento[1]]

            #resultado_secuencia.append((accion))

            return (pos_nueva, movimientos-1, tuple(tuple(caja) for caja in cajas_modificables))

        def cost(self, state, action, state2):
            return 1

        def heuristic(self, state):
            (fila, col), movimientos, cajas = state
            cantidad_fuera_de_objetivo = 0
            for objetivo in OBJETIVOS:
                if objetivo not in cajas:
                    cantidad_fuera_de_objetivo += 1

            distancias = []
            for caja in cajas:
                fila_caja, col_caja = caja
                distancias.append(abs(fila - fila_caja) + abs(col - col_caja))

            return cantidad_fuera_de_objetivo + min(distancias) - 1
    
    if __name__ == "__main__":
        viewer = BaseViewer()
        #viewer = WebViewer()
        result = astar(SocobanProblem(INICIAL), viewer=viewer, graph_search=True)

        print("Estado meta:")
        print(result.state)

        for action, state in result.path():
            print("Haciendo", action, "llegué a:")
            print(state)
            if action is not None:
                resultado_secuencia.append(action[1])

        print("Profundidad:", len(list(result.path())))
        print("Costo",result.cost)
        print("Stats:")
        print(viewer.stats)
    
        return resultado_secuencia
    else:
        viewer = BaseViewer()
        result = astar(SocobanProblem(INICIAL), graph_search=True)
        for action, state in result.path():
            if action is not None:
                resultado_secuencia.append(action[1])

        return resultado_secuencia
    


if __name__ == "__main__":
    pj = (1,2)
    paredes = [
        (0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
        (1,0),(1,6),
        (2,0),(2,6),
        (3,0),(3,3),(3,4),(3,5),(3,6),
        (4,0),(4,3),(4,6),
        (5,0),(5,6),
        (6,0),(6,6),
        (7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6)
    ]
    objetivos = [(4,4)]
    cajas = [(2,4)]
    movimientos = 30
    print(jugar(paredes, cajas, objetivos, pj, movimientos))