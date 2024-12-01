from concurrent.futures import ProcessPoolExecutor as Pool
from functools import partial

def apply_tracking(input, f = None):
    return input[0], f(input[1])

def multiprocess(f, input, intervals = 8):
    pool = Pool(max_workers = intervals)

    #apply = partial(apply_tracking, f = f)
    output = pool.map(f, input)

    #return_array = [None] * len(input)
    #for index, value in output:
        #return_array[index] = value

    return list(output)
    