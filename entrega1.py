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
    PAREDES = paredes
    OBJETIVOS = objetivos

    class SocobanProblem(SearchProblem):
        def is_goal(self, state):
            return super().is_goal(state)

        def actions(self, state):
            return super().actions(state)

        def result(self, state, action):
            return super().result(state, action)

        def cost(self, state, action, state2):
            return super().cost(state, action, state2)

        def heuristic(self, state):
            return super().heuristic(state)

if __name__ == "main":
    pass