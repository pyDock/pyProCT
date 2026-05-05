"""
Compatibility helpers for the Python 2.7 random sequence operations used by
the original clustering code.
"""
import math


def py2_randrange(rng, start, stop=None, step=1):
    istart = int(start)
    if istart != start:
        raise ValueError("non-integer arg 1 for randrange()")

    if stop is None:
        if istart > 0:
            return int(rng.random() * istart)
        raise ValueError("empty range for randrange()")

    istop = int(stop)
    if istop != stop:
        raise ValueError("non-integer stop for randrange()")

    width = istop - istart
    if step == 1 and width > 0:
        return int(istart + int(rng.random() * width))
    if step == 1:
        raise ValueError("empty range for randrange() (%d,%d, %d)" %
                         (istart, istop, width))

    istep = int(step)
    if istep != step:
        raise ValueError("non-integer step for randrange()")
    if istep > 0:
        n = (width + istep - 1) // istep
    elif istep < 0:
        n = (width + istep + 1) // istep
    else:
        raise ValueError("zero step for randrange()")

    if n <= 0:
        raise ValueError("empty range for randrange()")
    return istart + istep * int(rng.random() * n)


def py2_randint(rng, a, b):
    return py2_randrange(rng, a, b + 1)


def py2_shuffle(rng, values):
    for i in reversed(range(1, len(values))):
        j = int(rng.random() * (i + 1))
        values[i], values[j] = values[j], values[i]


def py2_sample(rng, population, k):
    n = len(population)
    if not 0 <= k <= n:
        raise ValueError("sample larger than population")

    result = [None] * k
    setsize = 21
    if k > 5:
        setsize += 4 ** math.ceil(math.log(k * 3, 4))

    if n <= setsize or hasattr(population, "keys"):
        pool = list(population)
        for i in range(k):
            j = int(rng.random() * (n - i))
            result[i] = pool[j]
            pool[j] = pool[n - i - 1]
    else:
        selected = set()
        for i in range(k):
            j = int(rng.random() * n)
            while j in selected:
                j = int(rng.random() * n)
            selected.add(j)
            result[i] = population[j]

    return result
