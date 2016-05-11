import os
import cPickle

import networkx as nx

import config
import ngram_builder as ng


def make_graph():
    """
    Makes word order graph from the serialized edge dict
    :return: graph with connections representing words occurring one after another
    """
    G = nx.DiGraph()

    with open(os.path.join(config.DIR_DUMP, 'dump_edges.pkl'), 'rb') as f:
        digrams = cPickle.load(f)

        for digram_str, cnt in digrams.iteritems():
            w1, w2 = digram_str.split(' ')
            G.add_edge(w1, w2)

        return G


if __name__ == '__main__':
    G = make_graph()
    print len(G.nodes())
    print len(G.edges())
