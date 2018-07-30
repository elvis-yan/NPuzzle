import collections
from state import State, Grid

##_________________________________ BFS ______________________________________
#
def bfs(state, goal_state):
    N = 1   # number of explored states
    if state == goal_state:
        # print(N)
        return state
    frontier = Queue([state])
    explored = set([state])
    while frontier:
        s = frontier.pop()
        for s2 in s.next_states():
            if s2 in explored or s2 in frontier: # not new
                continue
            N += 1
            # if N % 2000 == 0:
            #     print(N)
            if s2 == goal_state:
                # print(N)
                return s2
            frontier.put(s2)
            explored.add(s2)
    # print(N)


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


def randcases_test(search, n=50):
    goal_state = State(3)
    for _ in range(n):
        s = Grid(3).shuffle().value()
        print(s)
        state = State(3, 3, s)
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


if __name__ == '__main__':
    test_bfs()
    test_dfs()