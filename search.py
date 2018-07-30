import collections
from state import State, Grid, StatePool

##_________________________________ BFS ______________________________________
#
def bfs(state, goal_state, pool=None):
    if state == goal_state:
        return state
    frontier = Queue([state])
    explored = set([state])
    while frontier:
        s = frontier.pop()
        for s2 in s.next_states():
            if s2 in explored or s2 in frontier: # not new
                continue
            if s2 == goal_state:
                return s2
            frontier.put(s2)
            explored.add(s2)
    raise Exception('Never Get Here')


class Queue():
    def __init__(self, iterable=None, maxlen=None):
        self.q = collections.deque(iterable, maxlen)
        self.set = set(iterable)

    def put(self, v):
        self.q.append(v)
        self.set.add(v)
    
    def pop(self):
        v = self.q.popleft()
        self.set.remove(v)
        return v
    
    def __len__(self):
        return len(self.q)

    def __contains__(self, v):
        return v in self.set

##_________________________________ DFS ______________________________________
#
def dfs(state, goal_state):
    if state == goal_state:
        return state
    frontier = Stack([state])
    explored = set()
    while frontier:
        s = frontier.pop()
        for s2 in s.next_states():
            if s2 in explored:
                continue
            if s2 == goal_state:
                return s2
            frontier.put(s2)
            explored.add(s2)

class Stack(list): put = list.append


##_________________________________ IDS ______________________________________
#  iterative deepening search

def ids(state, goal_state, pool):
    ## recursive depth limited search (reference AIMA)
    cutoff = 'cutoff'
    failure = 'failure'
    def dls(state, limit):
        if state == goal_state:
            return state
        elif limit == 0:
            return cutoff
        else:
            cutoff_occurred = False
            for state2 in pool.gen_next_states(state):
                result = dls(state2, limit-1)
                if result is cutoff:
                    state2.parent = None
                    pool.put(state2)
                    cutoff_occurred = True
                elif result is not failure:
                    return result
                else:
                    print('---------------------------')
                    state2.parent = None
                    pool.put(state2)
            # state.parent = None
            # pool.put(state)
            if cutoff_occurred:
                return cutoff
            else:
                return failure
    ## ~end
    
    depth = 0
    while True:
        print('depth: ', depth)
        result = dls(state, depth)
        if result is not cutoff:
            return result
        else:
            depth += 1


def randcases_test(search, n=50):
    pool = StatePool(lambda: State(3, 3))
    goal_state = State(3)
    for _ in range(n):
        s = Grid(3).shuffle(40).value()
        print(s)
        state = State(3, 3, s)
        end = search(state, goal_state, pool)
        print(end.G.value(), end='\n\n')
        assert end == goal_state 

G = None
def test_bfs():
    print('test bfs ...')
    # state = State(Grid(3, 3))
    # goal_state = State(Grid(3, 3))
    # goal_state.G.matrix[0][0] = -1
    # bfs(state, goal_state)
    goal_state = State(3)
    state = State(3, 3, '312458067')
    end = bfs(state, goal_state)
    assert end.path() == ['right', 'right', 'up', 'left', 'left', 'up'] and end == goal_state

    randcases_test(bfs)
    print('bfs test pass')

def test_dfs():
    print('test dfs ...')
    randcases_test(dfs)
    print('dfs test pass')

def test_ids():
    print('test ids ...')
    randcases_test(ids)
    print('ids test pass')


if __name__ == '__main__':
    # test_bfs()
    # test_dfs()
    test_ids()