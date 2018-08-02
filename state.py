import copy
import random


class State:
    Counter = 0

    def __init__(self, m=1, n=1, s=""):
        State.Counter += 1
        if n == 1:
            n = m
        self.G = Grid(m, n, s)
        self.parent = None
        self.action = None
        self.g = 0

    def clone(self):
        state = State()
        state.G.matrix = copy.deepcopy(self.G.matrix)
        state.g = self.g
        return state

    def next_states(self):
        for v in ['up', 'down', 'left', 'right']:
            s = self.clone()
            try:
                s.G.move(v)
                s.parent = self
                s.action = v
                s.g += 1
                yield s
            except MoveOutOfBoundary:
                pass

    def path(self):
        actions = []
        cur, parent = self, self.parent
        while parent is not None:
            actions.append(cur.action)
            cur = parent
            parent = cur.parent
        actions.reverse()
        return actions

    def h(self):
        mat = self.G.matrix
        rows, cols = len(mat), len(mat[0])
        def _h(v, i, j):
            i0, j0 = v//cols, v%cols
            return abs(i-i0) + abs(j-j0)
        result = 0
        for i in range(rows):
            for j in range(cols):
                v = mat[i][j]
                if v != 0:
                    result += _h(v, i, j)
        return result

    def f(self): return self.g + self.h()

    def signature(self):
        return '_'.join(str(v) for row in self.G.matrix for v in row)

    def __hash__(self):
        mat = self.G.matrix
        rows, cols = len(mat), len(mat[0])
        BASE = rows * cols
        factor = 1
        result = 0
        for i in range(rows):
            for j in range(cols):
                v = mat[i][j]
                result += v * factor
                factor *= BASE
        return result


    def __eq__(self, state):
        return self.G.matrix == state.G.matrix
    
    def __lt__(self, state):
        return self.f() < state.f()


class StatePool():
    def __init__(self, factory, n=100):
        self.factory = factory
        self.pool = [factory() for _ in range(n)]

    def get(self):
        try:
            return self.pool.pop()
        except IndexError:
            return self.factory()

    def put(self, state):
        self.pool.append(state)

    def gen_next_states(self, state):
        for v in ['up', 'down', 'left', 'right']:
            s2 = self.clone(state)
            # s2 = state.clone()
            try:
                s2.G.move(v)
                s2.parent = state
                s2.action = v
                s2.g = state.g + 1
                yield s2
            except MoveOutOfBoundary:
                self.put(s2)
        
    def clone(self, state):
        s2 = self.get()
        mat = state.G.matrix
        rows, cols = len(mat), len(mat[0])
        for i in range(rows):
            for j in range(cols):
                s2.G.matrix[i][j] = mat[i][j]
        return s2


def search(state, goal_state):
    # while has unchecked state:
    #     if state == goal_state:
    #         gen_path()
    #         return

    # bfs dfs ids a_star ida_star
    pass


# Problem Representation
class Grid:
    def __init__(self, m=1, n=1, s=""):
        if n == 1:
            n = m
        self.matrix = self._gen_matrix(m, n)
        values = range(m*n) if s == "" else self.get_values_from_string(s)
        self._set_matrix(values)

    def get_values_from_string(self, s):
        if '_' in s:
            l = s.split('_')
        else:
            l = list(s)
        l = list(map(int, l))
        return l
   
    def move(self, v):
        vectors = {'up': (-1,0), 'down': (1,0), 'left': (0,-1), 'right': (0,1)}
        d = vectors[v]
        i, j = self.zero
        i2, j2 = i+d[0], j+d[1]
        rows, cols = len(self.matrix), len(self.matrix[0])
        if i2 < 0 or i2 >= rows or j2 < 0 or j2 >= cols:
            raise MoveOutOfBoundary("matrix({}, {}) [{},{}] {})".format(rows, cols, i, j, v))
        self.matrix[i][j], self.matrix[i2][j2] = self.matrix[i2][j2], self.matrix[i][j]

    def shuffle(self, n=100):
        actions = ['up', 'down', 'left', 'right']
        for _ in range(n):
            v = random.choice(actions)
            try:
                self.move(v)
            except MoveOutOfBoundary:
                pass
        return self

    def value(self):
        return '_'.join(str(v) for row in self.matrix for v in row)

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
        rows, cols = len(self.matrix), len(self.matrix[0])
        vals = list(vals)
        if len(vals) != rows * cols:
            print(len(vals), vals)
            raise ValueError("len(s) should be a square number")

        for i,v in enumerate(vals):
            r, c = i//cols, i%cols
            self.matrix[r][c] = v
    
    def __hash__(self):
        pass


MoveOutOfBoundary = Exception


def test():
    # Create
    g = Grid(3, 4)
    assert g.matrix == [[0,1,2,3], [4,5,6,7], [8,9,10,11]]
    g = Grid(3, 3, '876543210')
    assert g.matrix == [[8,7,6], [5,4,3], [2,1,0]]
    g = Grid(4, 3, '11_10_9_8_7_6_5_4_3_2_1_0')
    assert g.matrix == [[11,10,9], [8,7,6], [5,4,3], [2,1,0]]

    # Move
    g = Grid(2, 4, '1_2_3_0_4_5_6_7')
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
    s = State(3)
    states = list(s.next_states())
    assert len(states) == 2
    s_down, s_right = states[0], states[1]
    assert s_down.parent  == s and s_down.action == 'down' and s_down.G.matrix    == [[3,1,2], [0,4,5], [6,7,8]]
    assert s_right.parent == s and s_right.action == 'right' and s_right.G.matrix == [[1,0,2], [3,4,5], [6,7,8]]
    
    # Path
    s = State(3)
    s_right = list(s.next_states())[1]
    s_down = list(s_right.next_states())[0]
    s_left = list(s_down.next_states())[2]
    assert s_left.path() == ['right', 'down', 'left']

    print('test pass')

def test_h():
    assert State(3, 3, '724506831').h() == 18
    assert State(3, 3, '325780416').h() == 13
    assert State(3, 3, '106248357').h() == 13
    print('h_func test pass')


if __name__ == '__main__':
    test()
    test_h()