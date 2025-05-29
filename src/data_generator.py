import numpy as np

def gen_pop(size, pop_tuga = 10580000):
    while True:
        pop = np.random.randint(500, 5001, size=len(size))
        if pop.sum() <= pop_tuga:
            return pop
