import cProfile, pstats, io
from state import State, StatePool
from search import bfs, dfs, ids, Astar, SimulatedAnnealing, IDAstar

def profile(search, s):
    N = int(len(s.split('_'))**.5)
    
    if search in (ids, IDAstar):
        fn = search
        search = lambda s, s0: fn(s, s0, StatePool(lambda: State(N, N)))
    state = State(N, N, s)
    goal_state = State(N)
    pr = cProfile.Profile()
    pr.enable()
    end = search(state, goal_state)
    pr.disable()
    buf = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=buf).sort_stats(sortby)
    ps.print_stats()
    print(buf.getvalue())
    print(len(end.path()))


if __name__ == '__main__':
    # s = '1_0_6_2_4_8_3_5_7'
    # s = '3_2_5_7_8_0_4_1_6'
    # s = '9_2_7_0_3_11_1_6_4_13_15_10_8_12_5_14'
    s = '13_8_14_3_9_1_0_7_15_5_4_10_12_2_6_11'  # 41
    # s = '8_1_3_7_4_5_0_9_14_6_11_2_12_13_10_15'
    profile(IDAstar, s)
    print("Counter: ", State.Counter)