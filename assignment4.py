# FIT2004 S1/2021: Assignment 4 - Graph Algorithms
import math


class WordGraph:
    def __init__(self, lst):
        # create an adjacency list by first creating an array
        self.vertices = [None] * len(lst)
        for i in range(len(lst)):
            # create a vertex for each element in the lst with i being the id which represents the index of the vertex position.
            self.vertices[i] = Vertex(i)

        length_char = len(lst[0])

        # outer loop to loop through the vertex
        for i in range(len(lst)):
            # second loop will start looping at vertex index + 1
            for j in range(i+1, len(lst)):
                counter = 0  # to keep track and make sure the difference between the word only differs by 1
                weight = 0  # to keep track of the weight where the difference between the word is only differs by 1
                for k in range(length_char):
                    if lst[i][k] != lst[j][k]:
                        # for question 2 since q2 the graph is weighted.
                        weight = abs((ord(lst[i][k])-96) - (ord(lst[j][k])-96))
                        counter += 1

                if counter == 1:  # if counter is indeed one meaning that it satisfy the condition that both the strings have and edge between them.
                    # create an edge object to be added into the self.edge list
                    current_edge = Edge(
                        self.vertices[i], self.vertices[j], weight)
                    current_vertex = self.vertices[i]
                    current_vertex.add_edge(current_edge)
                    current_vertex.add_edge_index(j)
                    current_vertex.add_weight_val(weight)

                    # since the graph is undirected , we need the flip version of lst_edge[i] and lst_edge[j] to avoid recomputation
                    current_edge = Edge(
                        self.vertices[j], self.vertices[i], weight)
                    current_vertex = self.vertices[j]
                    current_vertex.add_edge(current_edge)
                    current_vertex.add_edge_index(i)
                    current_vertex.add_weight_val(weight)

    # this function is used to reset once dijikstra is performed so that we can perform second time.
    def reset(self):
        for i in range(len(self.vertices)):
            self.vertices[i].discovered = False
            self.vertices[i].visited = False
            self.vertices[i].previous = None
            self.vertices[i].distance = 0

    def best_start_word(self, target_words):
        """
        INPUT : TARGET_WORDS IS A NON-EMPTY LIST OF INDICES OF WORDS IN THE GRAPH

        OUTPUT : THIS FUNCTION WILL RETURNS AN INTEGER WHICH IS THE INDEX OF THE WORD IN THE GRAPH
        WHICH PRODUCES THE OVERALL SHORTEST WORD LADDERS TO EACH OF THE WORDS IN TARGET_WORDS.
        IF NO SUCH WORD EXIST , THIS FUNCTION WILL RETURN -1

        COMPLEXITY : THIS FUNCTION WILL RUN IN O(W^3) TIME WHERE W = NUMBER OF WORDS IN THE INSTANCE OF WORDGRAPH.
        THE REASON WHY THIS FUNCTION WILL RUN IN O(W^3) IS BECAUSE IN THIS FUNCTION THERE'S 3 FOR LOOPS WHICH CONTRIBUTE
        TO THE UPPERBOUND COMPLEXITY AND THE IMPLEMENTATION OF 3 FOR LOOPS IS DUE TO THE FACT OF USING FLOYD-WARSHALL ALGORITHM.

        """
        # target_words = [2,7,5]
        # target words are dad, abb, acc. Best start word is aaa
        #  words = ["aaa","aad","dad","daa","aca","acc","aab","abb"]

        # to determine the length of the list of vertex to know how many vertex is there.
        n = len(self.vertices)
        counter = 0
        min_val = 0
        lst2 = []
        lst = []  # to store the index of vertices
        lst_shortest = [None] * n
        for i in range(len(lst_shortest)):
            lst_shortest[i] = []

        # now i am going to use floyd-warshall algorithm by first creating the matrix of vertices.
        matrix = [[math.inf] * n for i in range(n)]

        # dist[i][i] = 0 meaning to say distance from a vertex to itself is 0
        for i in range(n):
            matrix[i][i] = 0

        # i will use the list to append all index of vertices which is connected to each other
        for i in range(len(self.vertices)):
            lst.append(self.vertices[i].edges_index)

        # now i am going to add the weight of those connected vertex.
        # and since in q1 the graph is unweighted, i will just hard code the weight to be 1 instead.
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                connected_edge_index = lst[i][j]
                matrix[i][connected_edge_index] = 1
        # print(matrix)
        # floyd Warshall algorithm to find shortest distance between pair of vertices by using 3 loops
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    matrix[i][j] = min(matrix[i][j], matrix[i][k]+matrix[k][j])
        # print(matrix)
        for i in range(n):
            for j in range(len(target_words)):
                # if there's an inf found in the matrix meaning that the graph in disconnected so we will just return -1 instead else we will
                # add into the lst_shortest which is a matrix of size n * n where n = len(self.vertices)
                if matrix[i][target_words[j]] is not math.inf:
                    lst_shortest[i].append(matrix[i][target_words[j]])
                else:
                    # return -1
                    break
        # print(lst_shortest)

        for item in lst_shortest:
            if len(item) == len(target_words):
                counter += 1

        if counter == 0:  # meaning that the graph is disconnected and no best word to target then we return -1
            return -1
        # print(lst_shortest)

        for item in lst_shortest:
            if len(item) < len(target_words):
                lst2.append(math.inf)
            else:
                lst2.append(max(item))

        # take the minimum value from lst2
        min_val = min(lst2)

        # try to match the results to the elements in lst2 in order to access their index.
        for i in range(len(lst2)):
            if lst2[i] == min_val:
                return i

    def dijkstra_algorithm(self, source):
        """
        THE IDEA OF THIS IMPLEMENTATION IS REFERENCED FROM DR.IAN LIM WERN HAN (FIT 2004 LECTURE) LECTURE VIDEO WEEK 10 

        THIS FUNCTION WILL BASICALLY FIND ALL SHORTEST DISTANCE FROM THE SOURCE BY PERFORMING EDGE RELAXATION IF THEY FIND A 
        NEW SHORTEST DISTANCE AND FINALLY WILL FINALIZED IT.
        """
        # firstly create an object of MINHEAP called discovered
        discovered = MinHeap(len(self.vertices))
        # add_node(distance,vertex object)
        discovered.add_node(0, self.vertices[source])
        # once we have added it into the heap we can now set discovered variable in vertex class to be true.
        self.vertices[source].discovered = True

        while discovered.is_empty() is False:  # meaning that the heap is not empty.
            # since its a min heap it will always give vertex which have the shortest distance.
            min_vertex = discovered.get_min()
            # get the vertex and check for visited
            min_vertex[1].visited = True
            # get all the edges which is connected to the source and start to find their shortest distance
            for edge in min_vertex[1].edges:
                if edge.v.discovered is False:
                    discovered.add_node(
                        min_vertex[0] + edge.w, edge.v)
                    edge.v.discovered = True
                    edge.v.distance = edge.u.distance + edge.w
                    edge.v.previous = edge.u.id

                elif edge.v.visited == False:
                    # meaning that the vertex is in the heap but the distance is not finalize yet.
                    # if there's still a shorter distance we will use that.
                    if edge.v.distance > edge.u.distance + edge.w:
                        edge.v.distance = edge.u.distance + edge.w
                        edge.v.previous = edge.u.id
                        item = discovered.get_item(edge.v)
                        # update the distance in the heap
                        discovered.priority_queue[item][0] = min_vertex[0] + edge.w

    def constrained_ladder(self, start, target, constraint_words):
        """
        INPUT : START AND TARGET ARE INDICES OF VERTICES.START IS THE INDEX OF THE WORD WHERE THE WORD LADDER
        MUST START , AND TARGET IS THE INDICES OF THE WORD WHERE THE WORD LADDER MUST END.CONSTRAINT WORD IS 
        A LIST OF INDICES.AT LEAST ONE OF THESE WORDS MUST APPEAR IN THE WORD LADDER.

        OUTPUT : CONSTRAINT_LADDER RETURNS A LIST OF INDICES OF VERTICES (IN ORDER) CORRESPONDING TO WORDS 
        REPRESENTING THE WORD LADDER . IF THERE ARE NO SUCH LADDERS, RETURN NONE.

        COMPLEXITY : THIS FUNCTION WILL RUN IN O(D LOG (W) + W LOG W) WHERE D IS THE NUMBER OF PAIRS 
        OF WORDS IN WORDGRAPH WHICH DIFFER BY EXACTLY ONE LETTER AND W IS THE NUMBER OF WORDS IN WORDGRAPH.
        """

        # first run dijikstra on the start
        self.dijkstra_algorithm(start)

        # then use a list to store their previous to allow backtracking
        lst_backtrack1 = []
        # a list used to store the shortest distance from start to all other vertex.
        lst_distance1 = []
        for i in range(len(self.vertices)):
            lst_backtrack1.append(self.vertices[i].previous)

        for i in range(len(self.vertices)):
            lst_distance1.append(self.vertices[i].distance)

        # before doing second dijikstra we need to first reset the graph
        self.reset()
        # do second dijikstra on the target
        self.dijkstra_algorithm(target)
        lst_backtrack2 = []
        lst_distance2 = []
        for i in range(len(self.vertices)):
            lst_backtrack2.append(self.vertices[i].previous)

        for i in range(len(self.vertices)):
            lst_distance2.append(self.vertices[i].distance)
        # print(lst_distance2)

        lst_res1 = []
        lst_res2 = []
        # is the length of the constraint word is just 1 then we will use that to backtrack.
        if len(constraint_words) == 1:
            intermediate = constraint_words[0]

            i = intermediate
            # backtracking process from start to intermediate(constraint word)
            while lst_backtrack1[i] is not None:
                lst_res1.append(lst_backtrack1[i])
                i = lst_backtrack1[i]

            lst_res1.reverse()

            i = intermediate
            # second backtrack process from intermediate to target
            while lst_backtrack2[i] is not None:
                lst_res2.append(lst_backtrack2[i])
                i = lst_backtrack2[i]

            if len(lst_res2) == 0 and len(lst_res1) == 0:
                return None
            else:
                return lst_res1 + [intermediate] + lst_res2

        else:  # meaning that the length of constraint word is > 1
            index = constraint_words[0]
            min_distance = lst_distance1[index] + lst_distance2[index]
            for i in range(1, len(constraint_words)):
                index2 = constraint_words[i]
                # since we knew the item in constraint words is the index of vertex we can find distance.
                new_distance = lst_distance1[index2] + lst_distance2[index2]

                if new_distance != 0 and min_distance != 0 and min_distance > new_distance:
                    min_distance = new_distance
                    index = constraint_words[i]
                elif min_distance == 0 and new_distance != 0:
                    min_distance = new_distance
                    index = constraint_words[i]

            # we will then use this index to do the backtracking.
            intermediate = index

            i = intermediate
            # backtracking from source to intermediate
            while lst_backtrack1[i] is not None:
                lst_res1.append(lst_backtrack1[i])
                i = lst_backtrack1[i]

            lst_res1.reverse()  # reverse to obtain the correct order.

            i = intermediate
            # backtrack from intermediate to target
            while lst_backtrack2[i] is not None:
                lst_res2.append(lst_backtrack2[i])
                i = lst_backtrack2[i]

            if len(lst_res2) == 0 and len(lst_res1) == 0:
                return None
            else:
                return lst_res1 + [intermediate] + lst_res2


class Vertex:
    def __init__(self, id):
        self.edges = []  # a list consisting of all edges that a vertex can connect
        self.id = id  # the vertex value
        # a list consisting of all edges that a vertex can connect but instead of storing strings we store index.
        self.edges_index = []
        # to see what is the weight of the neighbours of each vertex so that we can keep track.
        self.weight_lst = []
        self.discovered = False  # to check whether the vertex is already discovered or not
        self.visited = False  # to check whether the vertex is already visited or not
        self.distance = 0  # to keep track of the new shortest distance
        self.previous = None  # to allow backtracking to be carry out

    def add_edge(self, edge):
        self.edges.append(edge)

    def add_edge_index(self, index):
        self.edges_index.append(index)

    def add_weight_val(self, weight):
        self.weight_lst.append(weight)

    def get_id(self):
        return self.id


class Edge:
    def __init__(self, u, v, w=1):
        # by default if w is not set , it will be 1
        self.u = u
        self.v = v
        self.w = w


class MinHeap:
    """
    THIS MINHEAP IMPLEMENTATION IS REFERENCED FROM https://github.com/wychin229/fit2004_data-structure-and-algo_A4/blob/master/assignment4.py
    AS THIS IMPLEMENTATION OF MINHEAP CLASS IS REQUIRED TO PERFORMED DIJIKSTRA ALGORITHMS TO FIND THE SHORTEST PATH FROM THE SOURCE 
    TO ALL THE OTHER VERTEX.

    """

    def __init__(self, size):
        self.count = 0
        self.priority_queue = [None]*(size)

    def is_empty(self):
        if self.count > 0:
            return False
        else:
            return True

    def get_item(self, other):  # other is a vertex object
        for i in range(1, self.count+1):
            if other == self.priority_queue[i][1]:
                return i

    # key represents the distance from source , data represents a vertex objects.
    def add_node(self, key, data):
        item = [key, data]
        # put the item in the last position of minheap
        self.priority_queue[self.count+1] = item
        self.count += 1  # update counter
        self.rise(self.count)  # the index of the inserted item

    def rise(self, index):
        while index > 1 and self.priority_queue[index][0] < self.priority_queue[index//2][0]:
            self.swap(index, index//2)
            index //= 2

    def swap(self, current, parent):
        self.priority_queue[current], self.priority_queue[parent] = \
            self.priority_queue[parent], self.priority_queue[current]

    def get_min(self):
        if self.is_empty() is False:
            if self.count > 1:
                self.swap(self.count, 1)
                item = self.priority_queue.pop(
                    self.count)
                self.count -= 1
                self.sink(1)
                return item
            else:
                self.count -= 1
                return self.priority_queue[1]
        else:
            return False

    def smallest_child(self, index):
        if 2*index == self.count or self.priority_queue[2*index][0] < self.priority_queue[2*index+1][0]:
            return 2*index
        else:
            return 2*index+1

    def sink(self, index):
        while 2*index <= self.count:
            child = self.smallest_child(index)
            if self.priority_queue[index][0] <= self.priority_queue[child][0]:
                break
            self.swap(child, index)
            index = child
