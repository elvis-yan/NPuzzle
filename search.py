import collections
from heapq import heapify, heappop, heappush
from state import State, Grid, StatePool


##_________________________________ BFS ______________________________________
#

def bfs(state, goal_state):
    if state == goal_state:
        return state
    frontier = Queue([state])
    explored = set()
    while frontier:
        s = frontier.pop()
        explored.add(s)
        for s2 in s.next_states():
            if s2 in explored or s2 in frontier: # not new
                continue
            if s2 == goal_state:
                return s2
            frontier.put(s2)
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
        explored.add(s)
        for s2 in s.next_states():
            if s2 in explored:
                continue
            if s2 == goal_state:
                return s2
            frontier.put(s2)

class Stack(list): put = list.append


##_________________________________ IDS ______________________________________
#  iterative deepening search

def ids(state, goal_state, pool):
    ## recursive depth limited search (reference AIMA)
    explored = set()
    cutoff = 'cutoff'
    failure = 'failure'

    def dls(state, limit):
        nonlocal explored
        explored.add(state.signature())
        if state == goal_state:
            return state
        elif limit == 0:
            return cutoff
        else:
            cutoff_occurred = False
            for state2 in pool.gen_next_states(state):
                if state2.signature() in explored:
                    state2.parent = None
                    pool.put(state2)
                    continue
                result = dls(state2, limit-1)
                # two cases to choose (1)optimal (2)check fewer states  -> [heuristic function]
                explored -= {state2.signature()}
                if result is cutoff:
                    state2.parent = None
                    pool.put(state2)
                    cutoff_occurred = True
                elif result is not failure:
                    return result
                else:
                    state2.parent = None
                    pool.put(state2)
            ## Don't do it here
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
        explored.clear()
        result = dls(state, depth)
        if result is not cutoff:
            return result
        else:
            depth += 1


##_________________________________ A* ______________________________________
#

def Astar(state, goal_state):
    if state == goal_state:
        return state
    ## for simplicity 'explored' contains 'frontier'
    frontier = PriorityQueue([state])
    explored = {state: 0} # state: actual cost
    while frontier:
        s = frontier.pop()
        if s == goal_state:
            return s
        for s2 in s.next_states():
            if s2 not in explored or s2.g < explored[s2]:
                frontier.put(s2)
                explored[s2] = s2.g
    

class PriorityQueue:
    def __init__(self, iterable):
        self.h = list((state.f(), state) for state in iterable)
        heapify(self.h)
    
    def put(self, state):
        heappush(self.h, (state.f(), state))
    
    def pop(self):
        f, state = heappop(self.h)
        return state


##_________________________________ Test ______________________________________
#

def randcases_test(search, n=3, n_shuffle=50, times=20):
    if search is ids:
        search = lambda s, s0: ids(s, s0, StatePool(lambda: State(n, n)))
    goal_state = State(n)
    for _ in range(times):
        s = Grid(n).shuffle(n_shuffle).value()
        print(s)
        state = State(n, n, s)
        end = search(state, goal_state)
        print(end.G.value(), end='\n\n')
        assert end == goal_state 


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

def test_astar():
    print('test astar ...')
    randcases_test(Astar, n=4, n_shuffle=100)
    print('astar test pass')


if __name__ == '__main__':
    # test_bfs()
    # test_dfs()
    # test_ids()
    test_astar()