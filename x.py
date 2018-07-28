import copy

class State:

    def __init__(self, grid=None):
        self.G = copy.deepcopy(grid)
        self.parent = None

    def next_states(self):
        for v in ['up', 'down', 'left', 'right']:
            s = State(self.G)
            try:
                s.G.move(v)
                s.parent = self
                yield s
            except MoveOutOfBoundary:
                pass


    def path(self):
        pass

    
    def __hash__(self):
        pass

    def __eq__(self, state):
        return self.G.matrix == state.G.matrix


def search(state, goal_state):
    # while has unchecked state:
    #     if state == goal_state:
    #         gen_path()
    #         return

    # bfs dfs idas a_star ida_star
    pass


# Problem Representation
class Grid:
    def __init__(self, m=0, n=0):
        self.matrix = self._gen_matrix(m, n)
        self._set_matrix(range(m*n))

    def set(self, s, m=0, n=0):
        if '_' in s:
            l = s.split('_')
        else:
            l = list(s)
        l = list(map(int, l))
        if m==0 and n==0:
            m = n = int(len(l)**.5)
        assert m*n == len(l), ValueError("len(s) should be a square number")
        self.matrix = self._gen_matrix(m, n)
        self._set_matrix(l)

   
    def move(self, v):
        vectors = {'up': (-1,0), 'down': (1,0), 'left': (0,-1), 'right': (0,1)}
        d = vectors[v]
        i, j = self.zero
        i2, j2 = i+d[0], j+d[1]
        rows, cols = len(self.matrix), len(self.matrix[0])
        if i2 <0 or i2 >= rows or j2 < 0 or j2 >= cols:
            raise MoveOutOfBoundary("matrix({}, {}) [{},{}] {})".format(rows, cols, i, j, v))
        self.matrix[i][j], self.matrix[i2][j2] = self.matrix[i2][j2], self.matrix[i][j]

    @property
    def zero(self):
        "return the zero position"
        for (i, row) in enumerate(self.matrix):
            for (j, v) in enumerate(row):
                if v == 0:
                    return i,j
        raise Exception("Never Get Here")

    def _gen_matrix(self, m, n):
        return [[0 for _ in range(n)] for _ in range(m)]

    def _set_matrix(self, vals):
        n = len(self.matrix[0])
        for i,v in enumerate(vals):
            r, c = i//n, i%n
            self.matrix[r][c] = v
    
    def __hash__(self):
        pass

MoveOutOfBoundary = Exception

def test():
    # Create
    g = Grid(3, 4)
    assert g.matrix == [[0,1,2,3], [4,5,6,7], [8,9,10,11]]
    g.set('876543210')
    assert g.matrix == [[8,7,6], [5,4,3], [2,1,0]]
    g.set('11_10_9_8_7_6_5_4_3_2_1_0', 4, 3)
    assert g.matrix == [[11,10,9], [8,7,6], [5,4,3], [2,1,0]]

    # Move
    g.set("1_2_3_0_4_5_6_7", 2, 4)
    assert g.zero == (0, 3)
    g.move('down')
    assert g.matrix == [[1,2,3,7], [4,5,6,0]]
    try:
        g.move('down')
    except MoveOutOfBoundary:
        pass
    g.move('left')
    assert g.matrix == [[1,2,3,7], [4,5,0,6]] 

    # NextStates
    g = Grid(3, 3)
    s = State(g)
    states = list(s.next_states())
    assert len(states) == 2
    s_down, s_right = states[0], states[1]
    assert s_down.parent    == s and s_down.G.matrix    == [[3,1,2], [0,4,5], [6,7,8]]
    assert s_right.parent == s and s_right.G.matrix == [[1,0,2], [3,4,5], [6,7,8]]
    

    print('test pass')



test()