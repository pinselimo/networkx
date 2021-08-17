from random_graph import *

from networkx.algorithms import (
    betweenness_centrality,
    edge_betweenness_centrality,
    shortest_path,
)

N_TESTS = 100
EDGE_BTN = True
DELTA = 0.00001
SAMPLES = None


def compare_bc(G, M, weight=None, seed=None):
    """Unweighted (node) betweenness centrality should be equal regardless
    of the existance of multiple edges.

    For weighted BC we use a trick to ensure all shortest paths stay equal.
    Only new edges with a weight equal to or greather than their parallel
    counterpart are added.
    """
    btG = betweenness_centrality(G, k=SAMPLES, weight=weight, seed=seed)
    btM = betweenness_centrality(M, k=SAMPLES, weight=weight, seed=seed)

    for n in btM:
        if not (btG[n] - DELTA < btM[n] and btG[n] + DELTA > btM[n]):
            print("Original {} != {multi}".format(original, multi))
            exit(1)


def compare_edge_bc(G, M, weight=None, seed=None):
    """Edge betweenness centrality can change in the multigraph.
    We check if the sum of parallel edge BCs equals the singular edge case.

    If a weight is given the old implementation is weird. Its rescaling is
    incorrect.
    """
    ebcG = edge_betweenness_centrality(G, k=SAMPLES, weight=weight, seed=seed)
    ebcM = edge_betweenness_centrality(M, k=SAMPLES, weight=weight, seed=seed)
    for n in ebcG:
        u, v = n
        original = ebcG[n]
        multi = sum(ebcM[(u, v, k)] for k in M[u][v] if (u,v,k) in ebcM)
        if not (original - DELTA < multi and original + DELTA > multi):
            print("Original {} != {}".format(original, multi))
            exit(1)


if __name__ == "__main__":
    i = 1
    n = N_TESTS * 2 * 2
    for t in range(N_TESTS):
        for weight in (None, "w"):
            for directed in (True, False):
                print("\r{:2.2f} %".format(100 * i / n), end=" " * 4, flush=True)
                i += 1

                G = random_graph(size=20, seed=t, weights=(weight,))
                if directed:
                    G = G.to_directed()
                M = make_multi(G, seed=t)

                compare_bc(G, M, weight=weight, seed=t)
                if EDGE_BTN:
                    compare_edge_bc(G, M, weight=weight, seed=t)
