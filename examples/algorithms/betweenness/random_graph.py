"""Generate random graphs"""
import numpy.random as npr
import random as rand
from functools import reduce

from networkx import Graph, DiGraph, MultiGraph, MultiDiGraph


def get_edges(G, n_edges, multi=False, weights=()):
    samples = list((npr.choice(G), npr.choice(G)) for _ in range(n_edges))
    if not multi:
        samples = set(samples)
    for w in weights:
        samples = [(*s, {w: 0.1+npr.rand()}) for s in samples]
    return samples


def random_graph(size=0, seed=None, maxsize=100, weights=()):
    if seed:
        rand.seed(seed)
        npr.seed(seed)

    if not size:
        size = npr.randint(2, maxsize)

    G = Graph()
    G.add_nodes_from(range(size))
    G.add_edges_from(get_edges(G, npr.randint(1, maxsize * 2), weights=weights))

    return G


def make_multi(_G, seed=None):
    """Create a multigraph out of a non-multigraph"""
    G = MultiGraph(_G)
    if _G.is_directed():
        G = G.to_directed()

    if seed:
        rand.seed(seed)
        npr.seed(seed)

    edges = [(u, v, dict(d)) for u, v, d in G.edges(data=True)]
    n_samples = npr.randint(len(G.edges))
    samples = [edges[npr.randint(len(G.edges))] for _ in range(n_samples)]

    for _, _, d in edges:
        for k in d:
            # Keep shortest paths equal by adding only higher weights
            d[k] += npr.rand()

    G.add_edges_from(samples)
    return G
