import math
import os
import time
import random
from queue import PriorityQueue

class Graph():
    def __init__(self, length, width, start_node, end_node):
        self.node_state_hash = {'@': 0b1110, '$': 0b1101, '*': 0b1100, 'S': 0b10, 'G': 0b11, '.': 0b0, '#': 0b1, u'↘': 0b100, u'→': 0b101, u'↗': 0b110, u'↑': 0b111, u'↖': 0b1000, u'←': 0b1001, u'↙': 0b1010, u'↓': 0b1011}
        self.inverse_node_hash = self.hash_to_inverse(self.node_state_hash)

        self.l = length
        self.w = width
        self.grid = [[self.node_state_hash['.'] for i in range(self.l)] for i in range(self.w)]

        self.starting_node = start_node
        self.ending_node = end_node
        self.grid[self.starting_node[1]][self.starting_node[0]] = self.node_state_hash['S']
        self.grid[self.ending_node[1]][self.ending_node[0]] = self.node_state_hash['G']

        self.walls = None

        coords = []

        self.blacklist = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == self.node_state_hash['#']:
                    self.blacklist.append((j, i))

        '''
        S - 10
        G - 11
        . - 0
        # - 1
        '''

    def generate_rects(self, num_rects):
        rects = []

        for i in range(num_rects):
            starting_point = (random.randint(0, self.l - 11), random.randint(0, self.w - 1)) # (cols, rows)
            print(self.w, starting_point[0])
            w = random.randint(0, (self.w - starting_point[0]) - 1)
            h = random.randint(0, (self.l - starting_point[1]) - 1)

            rects.append((starting_point, w, h))
        
        return rects
    
    def rect_to_wall(self, rect):
        wall = []

        starting_point = rect[0]
        w = rect[1]
        h = rect[2]

        x_points = list(range(starting_point[0], starting_point[0] + w, 1))
        y_points = list(range(starting_point[1], starting_point[1] + h, 1))

        for i in range(len(x_points)):
            for j in range(len(y_points)):
                wall.append((x_points[i], y_points[j]))
        
        return wall
    
    def graph_updater(self, random_rects):
        walls = []
        for rect in random_rects:
            walls.append(self.rect_to_wall(rect))
        
        self.walls = walls

        for i in range(len(walls)):
            for j in range(len(walls[i])):
                x = walls[i][j][0]
                y = walls[i][j][1]

                self.grid[y][x] = self.node_state_hash['#']
    
    def wall_generation(self, generation_state='random', num_walls = 2, coords=None):
        if generation_state == 'random':
            random_rects = self.generate_rects(num_rects=num_walls)

            self.graph_updater(random_rects)
        elif generation_state == 'custom':
            self.graph_updater(coords)

    def euclidian(self, p1, p2):
        # return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def manhattan(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    """
    def get_gcost(self, curr_node, path):
        total = 0
        for i in range(1, len(path)):
            total += self.euclidian(path[i], path[i - 1])

        return total
    """

    # uses euclidian
    def get_hcost(self, curr_node, ending_coords, heuristic_type='euclidian'):
        if heuristic_type == 'euclidian':
            return self.euclidian(curr_node, ending_coords)
        if heuristic_type == 'manhattan':
            return self.manhattan(curr_node, ending_coords)

    def get_fcost(self, coords, goal, curr_g_cost, path, heuristic):
        addition_matrix = [(1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (-1, 1)]

        coords_list = [(coords[0] + addition_matrix[i][0], coords[1] + addition_matrix[i][1]) for i in range(len(addition_matrix))]

        reps = []
        print(coords)
        for i in range(len(coords_list)):
            if (coords_list[i][1] < 0 or coords_list[i][0] < 0):
                reps.append(coords_list[i])
            elif (coords_list[i][1] >= (self.w)) or (coords_list[i][0] >= (self.l)):
                reps.append(coords_list[i])
                # print(coords_list[i], self.grid[coords_list[i][1]][coords_list[i][0]], 1)
            elif (coords_list[i] in path) or self.get_node_state(coords_list[i]) == self.node_state_hash['#']:
                reps.append(coords_list[i])
                # print(coords_list[i], self.grid[coords_list[i][1]][coords_list[i][0]], 2)
            elif coords_list[i] in self.blacklist:
                reps.append(coords_list[i])
                # print(coords_list[i], self.grid[coords_list[i][1]][coords_list[i][0]], 3)

        for rep in reps:
            coords_list.remove(rep)        

        lowest_fcost = float('inf')
        local_best_node = None
        for i in range(len(coords_list)):
            local_fcost = curr_g_cost + 1 + self.get_hcost(coords_list[i], goal, heuristic_type=heuristic)
            # local_fcost = self.get_hcost(coords_list[i], goal, heuristic_type=heuristic)
            if local_fcost < lowest_fcost:
                lowest_fcost = local_fcost
                local_best_node = coords_list[i]
        
        return local_best_node
    
    def get_neighbors(self, coords):
        addition_matrix = [(1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (-1, 1)]

        coords_list = [(coords[0] + addition_matrix[i][0], coords[1] + addition_matrix[i][1]) for i in range(len(addition_matrix))]

        reps = [] 
        for i in range(len(coords_list)):
            if (coords_list[i][1] < 0 or coords_list[i][0] < 0):
                reps.append(coords_list[i])
            elif (coords_list[i][1] >= (self.w)) or (coords_list[i][0] >= (self.l)):
                reps.append(coords_list[i])
                # print(coords_list[i], self.grid[coords_list[i][1]][coords_list[i][0]], 1)
            elif self.get_node_state(coords_list[i]) == self.node_state_hash['#']:
                reps.append(coords_list[i])
                # print(coords_list[i], self.grid[coords_list[i][1]][coords_list[i][0]], 2)
            elif coords_list[i] in self.blacklist:
                reps.append(coords_list[i])
                # print(coords_list[i], self.grid[coords_list[i][1]][coords_list[i][0]], 3)

        for rep in reps:
            coords_list.remove(rep)

        return coords_list    

    def greedy_heuristic_alg(self, heuristic_type='euclidian'):
        current_node = self.starting_node
        g_cost = 0
        path = []

        while current_node != self.ending_node:
            next_node = self.get_fcost(current_node, self.ending_node, g_cost, path, heuristic=heuristic_type)

            cy = current_node[1]
            cx = current_node[0]
            ny = next_node[1]
            nx = next_node[0]

            path_vector = [nx - cx, ny - cy]

            path_direction = self.get_path_vector(path_vector)

            g_cost += 1
            current_node = next_node
            path.append(next_node)

            if self.get_node_state(next_node) != self.node_state_hash['G']:
                self.update_board([next_node], path_direction)

            grid_state = self.get_grid()

            os.system('cls')
            print(grid_state)
            # time.sleep(0.1)

        return path
    
    def AStar(self, heuristic_type='euclidian'):
        count = 0

        open_set = PriorityQueue()
        # PQ node -> (f_score, count, node_coords)
        open_set.put((0, count, self.starting_node))
        came_from = {}
        
        g_score = {}
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                g_score.update({(i, j) : float('inf')})

        g_score[self.starting_node] = 0

        f_score = {}
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                f_score.update({(i, j) : float('inf')})
        
        f_score[self.starting_node] = self.euclidian(self.starting_node, self.ending_node)

        open_set_hash = {self.starting_node}

        while not open_set.empty():
            current_node = open_set.get()[2] # get's f score of highest priority element in queue
            open_set_hash.remove(current_node)

            if (current_node[1], current_node[0]) == self.ending_node:
                print(self.reconstruct_path(came_from))
                return True # reconstruct path
            
            for neighbor in self.get_neighbors(current_node):
                temp_g_score = g_score[current_node] + 1

                if temp_g_score < g_score[neighbor]: # checking if we found a better path to the neighbor we are looking at
                    # updating g_score of neighbor if it is lower
                    came_from[neighbor] = current_node
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.euclidian(neighbor, self.ending_node)

                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)

                        self.open_node(neighbor)

            os.system('cls')
            grid = self.get_grid()
            print(grid)

            if current_node != self.starting_node: # if node we just considered is not start node then close it off (already considered and won't be added into priority queue again)
                self.close_node(current_node)

        return False

    def reconstruct_path(self, came_from):
        path = list(came_from.keys())
        path.reverse()

        for i in range(len(path)):
            self.update_board([path[i]], self.node_state_hash['@'])
            
            os.system('cls')
            grid = self.get_grid()
            print(grid)

    def open_node(self, coords):
        self.grid[coords[1]][coords[0]] = self.node_state_hash['$']  

    def close_node(self, coords):
        self.grid[coords[1]][coords[0]] = self.node_state_hash['*']     

    def hash_to_inverse(self, hashmap):
        keys = list(hashmap.keys())
        vals = [hashmap[key] for key in keys]

        inverse_hashmap = {}
        for i in range(len(vals)):
            inverse_hashmap.update({vals[i]: keys[i]})

        print(inverse_hashmap)
        
        return inverse_hashmap
    
    def get_node_state(self, coords):
        return self.grid[coords[1]][coords[0]]

    def update_board(self, coords, update):
        for i in range(len(coords)):
            self.grid[coords[i][1]][coords[i][0]] = update
    
    def get_path_vector(self, path_vector):
        if path_vector[0] > 0 and path_vector[1] > 0:
            path_direction = u'↘'
        if path_vector[0] < 0 and path_vector[1] > 0:
            path_direction = u'↙'
        if path_vector[0] > 0 and path_vector[1] < 0:
            path_direction = u'↗'
        if path_vector[0] < 0 and path_vector[1] < 0:
            path_direction = u'↖'
        if path_vector[0] > 0 and path_vector[1] == 0:
            path_direction = u'→'
        if path_vector[0] < 0 and path_vector[1] == 0:
            path_direction = u'←'
        if path_vector[0] == 0 and path_vector[1] < 0:
            path_direction = u'↑'
        if path_vector[0] == 0 and path_vector[1] > 0:
            path_direction = u'↓'
        
        return self.node_state_hash[path_direction]

    def get_grid(self):
        graph = self.grid

        final_str = ''
        for i in range(len(graph)):
            temp = ''
            for j in range(len(graph[i])):
                temp += '{} '.format(self.inverse_node_hash[graph[i][j]])
            final_str += '{}{}'.format(temp, '\n')
        
        return final_str