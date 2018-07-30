import time
from graphics import Graphics
from state import State
from search import bfs, dfs

M = 3
N = 3

G = Graphics(M, N)
G.shuffle()
value = G.value()
state = State(M, N, value)
goal_state = State(M, N)

s = input('search[dfs, bfs]: ')
if s == 'dfs':
    search = dfs
    d = .0005
elif s == 'bfs':
    search = bfs
    d = .05
else:
    raise ValueError("Search method '{}' not exist".format(s))



end = search(state, goal_state)
actions = end.path()
print('#move: ', len(actions))
input("show me the answer?")
for (i,v) in enumerate(actions):
    if i % 2000 == 0:
        print(i)
    G.move(v)
    time.sleep(d)
input('quit? ')