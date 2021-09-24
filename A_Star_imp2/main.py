from graph_class import Graph
import math
import random

if __name__ == '__main__':
    x, y = random.randint(0, 54), random.randint(0, 54)
    x2, y2 = random.randint(0, 54), random.randint(0, 54)
    graph = Graph(length=55, width = 55, start_node=(1, 1), end_node=(54, 54)) # sn -> (j, i) en -> (j, i)

    grid = graph.get_grid()

    print(grid)

    graph.wall_generation(generation_state='random', num_walls=5)
    # graph.wall_generation(generation_state='custom', num_walls=5, coords=[[(10, 10), 10, 5]])

    grid = graph.get_grid()

    print(grid)

    # path = graph.greedy_heuristic_alg(heuristic_type='euclidian')
    # print(path)
    graph.AStar(heuristic_type='euclidian')