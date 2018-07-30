import cProfile, pstats, io
from state import State
from search import bfs, dfs, ids

def profile(search, s):
    state = State(3, 3, s)
    goal_state = State(3)
    pr = cProfile.Profile()
    pr.enable()
    search(state, goal_state)
    pr.disable()
    buf = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=buf).sort_stats(sortby)
    ps.print_stats()
    print(buf.getvalue())


if __name__ == '__main__':
    s = '1_6_0_3_5_2_7_4_8'
    profile(dfs, s)