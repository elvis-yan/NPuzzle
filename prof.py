import cProfile, pstats, io
from state import State, StatePool
from search import bfs, dfs, ids

def profile(search, s):
    pool = StatePool(lambda: State(3, 3))
    state = State(3, 3, s)
    goal_state = State(3)
    pr = cProfile.Profile()
    pr.enable()
    end = search(state, goal_state, pool)
    pr.disable()
    buf = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=buf).sort_stats(sortby)
    ps.print_stats()
    print(buf.getvalue())
    print(len(end.path()), end.path())
    return pool


if __name__ == '__main__':
    # s = '1_0_6_2_4_8_3_5_7'
    s = '3_2_5_7_8_0_4_1_6'
    pool = profile(ids, s)
    print(len(pool.pool))
    print("Counter: ", State.Counter)