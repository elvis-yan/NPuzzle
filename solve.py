import time
from graphics import Graphics
from x import State
from search import bfs

G = Graphics(3)
G.shuffle()
value = G.value()
state = State(3, 3, value)
goal_state = State(3)

end = bfs(state, goal_state)
actions = end.path()
input()
for v in actions:
    G.move(v)
    time.sleep(0.2)
input('quit? ')