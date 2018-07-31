import cProfile, pstats, io
from state import State, StatePool
from search import bfs, dfs, ids, Astar

def profile(search, s):
    N = int(len(s.split('_'))**.5)
    
    if search is ids:
        search = lambda s, s0: ids(s, s0, StatePool(lambda: State(N, N)))
    state = State(N, N, s)
    goal_state = State(3)
    pr = cProfile.Profile()
    pr.enable()
    end = search(state, goal_state)
    pr.disable()
    buf = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=buf).sort_stats(sortby)
    ps.print_stats()
    print(buf.getvalue())
    print(len(end.path()), end.path())


if __name__ == '__main__':
    # s = '1_0_6_2_4_8_3_5_7'
    # s = '3_2_5_7_8_0_4_1_6'
    s = '9_2_7_0_3_11_1_6_4_13_15_10_8_12_5_14'
    profile(Astar, s)
    print("Counter: ", State.Counter)