"""
Seth Brenneman
--------------
Analysis of Algorithms
----------------------
March 30, 2021
--------------
Ford-Fulkerson 
-------------
This problem comes from chapter 7 expercise 6 in Algorithm Design by Jon Kleinberg and Eva Tardos. 'Suppose you’re a consultant for the Ergonomic 
Architecture Commission, and they come to you with the following problem. They’re really concerned about designing houses that are 
“user-friendly,” and they’ve been having a lot of trouble with the setup of light fixtures and switches in newly designed houses. Consider, for 
example, a one-floor house with n light fixtures and n locations for light switches mounted in the wall. You’d like to be able to wire up one 
switch to control each light fixture, in such a way that a person at the switch can see the light fixture being controlled.'

Credit to Daniel Showalter for providing the function to check whether two lines intersect for the lights and switches problem.

The max_flow_graph function was adapted from Daniel Showalter's maxFlow function.

Credit to Quinston Pimenta (https://www.youtube.com/watch?v=GoVjOT30xwo) for detailing and showing how the Ford Fulkerson algorithm 
works and translates into code. He is responsible for providing the breadth first search function and the Fulkerson function to get my code running.
"""
from timeit import timeit

Walls = [(1,2),(1,5),(8,5),(8,3),(11,3),(11,1),(5,1),(5,3),(4,3),(4,1),(1,1),(1,2)]

# Use these walls for n > 3
# Walls = [(1,2),(1,6),(8,6),(8,4),(11,4),(11,0),(5,0),(5,4),(4,4),(4,0),(1,0),(1,2)]

# n = 3: Ergonomic
Lights = [(2,4),(2,2),(5,4)]
Switches = [(4,4),(6,3),(6,2)]

# n = 6
# Lights = [(2,2),(3,3),(6,5),(7,1),(10,3),(8,3)]
# Switches = [(2,5),(4,5),(5,5),(9,2),(8,1),(7,4)]

# n = 9
# Lights = [(2,2),(3,3),(6,5),(7,1),(10,3),(8,3),(3,2),(6,1),(7,5)]
# Switches = [(2,5),(4,5),(5,5),(9,2),(8,1),(7,4),(3,4),(9,1),(3,1)]

# n = 12
# Lights = [(2,2),(3,3),(6,5),(7,1),(10,3),(8,3),(3,2),(6,1),(7,5),(2,1),(6,2),(7,2)]
# Switches = [(2,5),(4,5),(5,5),(9,2),(8,1),(7,4),(3,4),(9,1),(3,1),(10,1),(8,2),(2,3)]

# n = 15
# Lights = [(2,2),(3,3),(6,5),(7,1),(10,3),(8,3),(3,2),(6,1),(7,5),(2,1),(6,2),(7,2),(6,3),(9,3),(2,4)]
# Switches = [(2,5),(4,5),(5,5),(9,2),(8,1),(7,4),(3,4),(9,1),(3,1),(10,1),(8,2),(2,3),(7,3),(3,5),(10,2)]

# n = 3: Ergonomic
# Lights = [(2,4),(2,2),(5,4)]
# Switches = [(4,4),(6,3),(6,2)]

# n = 3: Not ergonomic
# Lights = [(2,4),(2,2),(5,4)] 
# Switches = [(6,2),(7,4),(6,3)]  


# Return true if line segments AB and CD intersect
# Source: http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def ccw(A, B, C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def does_intersect(A, B, C, D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def is_visible(pt1, pt2, Walls):
    x1,y1 = pt1
    x2,y2 = pt2
    for i, wall in enumerate(Walls[:-1]):
        x3,y3 = wall
        x4,y4 = Walls[i+1]
        if does_intersect((x1,y1),(x2,y2),(x3,y3),(x4,y4)):
            return False
    return True        


def breadth_first_search(graph, source, sink, parentTracker):
    discovered = [False] * len(graph) # Create a list that stores whether a node has been visited
    discovered[source] = True # Set the source node to discovered
    queue = [] # Queue to store the nodes that will soon be traversed
    queue.append(source) # Append the source node to the queue
    parentTracker[source] = -1 # This parent tracker list keeps track of the parent nodes for each node

    while len(queue) > 0: # While the queue still has nodes to be traversed
        u = queue.pop(0) # Current node (u) is the next node from the queue
        for v in range(0, len(graph)): # For all the other nodes in the graph
            if discovered[v] == False and graph[u][v] > 0: # If there exists a path between u and v and v has not been discovered and the residual graph is greater than 0
                queue.append(v) # Add v to the queue
                discovered[v] = True # Set the v node to visited
                parentTracker[v] = u # Make u the parent of node v

    if discovered[sink]: #If the sink was visited return True and look for another traversal
        return True
    else:
        return False


def create_max_flow_graph(walls, lights, switches):
    numLights = len(lights)
    numSwitches = len(switches)
    vertices = 1 + numLights + numSwitches + 1
    adjMatrix = [[]] * vertices

    i = 0
    while i < vertices:
        adjMatrix[i] = list(0 for j in range(0, vertices))
        i += 1

    for i in range(1): # Setup source edges 
        for j in range(1, numLights + 1):
            adjMatrix[i][j] = 1

    for i in range(numSwitches + 1, vertices - 1): # Setup sink edges
        for j in range(1):
            adjMatrix[i][-1] = 1

    for i, light in enumerate(lights): # Populate the adjacency matrix by checking each light and switch combination
        for j, switch in enumerate(switches):
            if is_visible(light, switch, walls):
                adjMatrix[i + 1][j + numLights + 1] = 1

    # To see adjacency matrix uncomment code block below
    '''
    for i in adjMatrix: 
        print(i)
        
    print('')
    '''
    return adjMatrix


def ford_fulkerson(graph, source, sink):
    parentTracker = [0] * len(graph)
    u, v = 0, 0
    residualGraph = graph
    maxFlow = 0

    while breadth_first_search(residualGraph, source, sink, parentTracker):
        pathFlow = float('inf')
        v = sink

        while not v == source:
            u = parentTracker[v]
            pathFlow = min(pathFlow, residualGraph[u][v])
            v = parentTracker[v]

        v = sink

        while not v == source:
            u = parentTracker[v]
            residualGraph[u][v] -= pathFlow
            residualGraph[v][u] += pathFlow
            v = parentTracker[v]
        
        maxFlow += pathFlow
    return maxFlow


# To use timeit module, uncomment code block below
'''
def main_timeit():
    if len(Lights) != len(Switches):
        print("The number of lights and the number of switches must be the same.")
        exit(0)
    else:
        graph = max_flow_graph(Walls, Lights, Switches)
        maxFlow = ford_fulkerson(graph, 0, len(graph) - 1)

    if maxFlow == len(Lights):
        print("These lights and switches are ergonomic.")
    else:
        print("These lights and switches are not ergonomic.")


# Credit to Brandon Chupp for figuring out the timeit wrapper function
def wrapper(func, *args):
    def wrapped():
        return func(*args)
    return wrapped

Ford_Fulkerson = wrapper(main_timeit())
N = len(Lights)
'''

if __name__ == '__main__':
    if len(Lights) != len(Switches):
        print("The number of lights and the number of switches must be the same.")
        exit(0)
    else:
        graph = create_max_flow_graph(Walls, Lights, Switches)
        maxFlow = ford_fulkerson(graph, 0, len(graph) - 1)
        # Uncomment to use timeit module
        # print("size:", N, "Ford Fulkerson Time:", timeit(ford_fulkerson, number = 10000)/10000)

    if maxFlow == len(Lights):
        print("These lights and switches are ergonomic.")
    else:
        print("These lights and switches are not ergonomic.")
