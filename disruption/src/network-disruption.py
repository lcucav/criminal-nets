# If you use parts of this code please cite the following articles:

# @misc{cavallaro2020disrupting,
#     title={Disrupting Resilient Criminal Networks through Data Analysis: The case of Sicilian Mafia},
#     author={Lucia Cavallaro and Annamaria Ficara and Pasquale De Meo and Giacomo Fiumara and Salvatore Catanese and Ovidiu Bagdasar and Antonio Liotta},
#     year={2020},
#     eprint={2003.05303},
#     archivePrefix={arXiv},
#     primaryClass={cs.SI}
# }

# coding: utf-8
__author__ = "Lucia Cavallaro, Pasquale De Meo, Annamaria Ficara, and Giacomo Fiumara"
__version__ = "0.0.1"
# In[1]:

import networkx as nx
import numpy as np
import copy
import pandas as pd
import array
import operator


names = ['id', 'data']
formats = ['int32', 'int32']
dtype = dict(names=names, formats=formats)

filename = {'Montagna_meetings_edgelist': 'meeting', 'Montagna_phonecalls_edgelist': 'phone_calls'}
nrem = 5  # top valued nodes to be removed


def collective_influence_centality(Graph, torem, weight=None):
    """
    Compute Collective Influence (CI) Centrality per each node (up to distance d=2).
    Decreasing order: from lowest to highest CI

    :param Graph: (Graph obj) Input Graph.
    :param torem: (array.array)  Array of nodes to be removed
    :param weight : (string) None or string, optional (default=None)
      If None, all edge weights are considered equal.
      Otherwise holds the name of the edge attribute used as weight.
    :return: (array.array) Sorted by CI numpy array (from higher to lower).
    """
    colinf = dict()
    for node in Graph:
        summatory = 0
        for iter_node in Graph.neighbors(node):
            if weight is None:
                summatory += Graph.degree(iter_node) - 1
            else:
                summatory += Graph.degree(iter_node, weight='weight') - 1
        if weight is None:
            colinf[node] = (Graph.degree(node) - 1) * summatory
        else:
            colinf[node] = (Graph.degree(node, weight='weight') - 1) * summatory
    npcolinf = np.fromiter(colinf.items(), dtype=dtype, count=len(colinf))
    sorted_colinf = np.sort(npcolinf, order='data')
    for rem_n in range(1, nrem + 1):
        # To populate the array of the nodes to be removed (the nrem ones with the highest centrality score).
        torem.append(sorted_colinf[-rem_n][0])  # Sorted in descreasing order.
    return torem


def average_degree(Graph):  # ToDo: Unused Function. Removal Considered.
    """
    Compute Average Degree in the input Graph.

    :param Graph: (Graph obj) Input Graph.
    :return: (float) Average Degree in Graph.
    """
    degree = []
    for x in nx.degree(Graph):
        degree.append(x[1])
    return sum(degree) / float(nx.number_of_nodes(Graph))


def lcc_size(Graph):
    """
    Compute Largest Connected Component (LCC) in a Graph.

    :param Graph: (Graph obj) Input Graph.
    :return: (int) Size of the LCC.
    """
    compsize = []
    for c in nx.connected_components(Graph):
        compsize.append(nx.number_of_nodes(Graph.subgraph(c)))
    return max(compsize)


def max_centr(Graph, centrality_function, torem, weight=None):
    """
    Nodes sorting (as dict, key:node_name, value:centrality_score) according to the centrality function.

    :param Graph: (Graph obj) Input Graph.
    :param centrality_function (function) NetworkX centrality function.
    :param torem: (array.array)  Array of nodes to be removed
    :param weight : (string) None or string, optional (default=None)
      If None, all edge weights are considered equal.
      Otherwise holds the name of the edge attribute used as weight.
    #:return kmax: (int) k-th Node name.
    #:return vmax: (float) Centrality Score for k-th node.
    :return: (array.array) Sorted by CI numpy array (from higher to lower).

    Example: centrality_function = nx.degree_centrality
    """
    if weight is None:
        dcentr = centrality_function(Graph)
    else:
        dcentr = centrality_function(Graph, weight='weight')
    sorted_x = sorted(dcentr.items(), key=operator.itemgetter(1))
    for rem_n in range(1, nrem + 1):
        torem.append(sorted_x[-rem_n][0])
    return torem


def disruption(Graph, centrality_function, centrality_label,
               lccinit, dflcc, dflccvar, casekey, weight=None):
    """
    Network Disruption. Compute Largest Connected Component (LCC) and Collective Influence (CI) after nodes removal.

    :param Graph: (Graph obj) Input Graph.

    :param centrality_function: (function) NetworkX centrality function.
    :param centrality_label: (str) Centrality metrics label.

    :param lccinit: (int) Largest Connected Component size of the initial graph.
    :param dflcc: (pandas.core.frame.DataFrame) LCC Dataframe.
    (Dataframe will be composed by: Iter_Num, LCC size after node removal according to the Centrality_Metrics).
    :param dflccvar: (pandas.core.frame.DataFrame) LCC size variation compared with the initial LCC Dataframe.
    (Dataframe will be composed by: Iter_Num, LCC size after node removal according to the Centrality_Metrics).

    :param casekey: (str) Node removal selected (case = {1: 'sequential', 2: 'block'}) before compute LCC.
    :param weight : (string) None or string, optional (default=None)
      If None, all edge weights are considered equal.
      Otherwise holds the name of the edge attribute used as weight.

    :return dflcc: (pandas.core.frame.DataFrame) LCC Dataframe.
    (Dataframe will be composed by: Iter_Num, LCC size after node removal according to the Centrality_Metrics).
    :return dflccvar: (pandas.core.frame.DataFrame) LCC size variation compared with the initial LCC Dataframe.
    (Dataframe will be composed by: Iter_Num, LCC size after node removal according to the Centrality_Metrics).
    """
    dictx = dict()  # Dict current LCC size
    dicty = dict()  # Dict current LCC normalized percentage variation compared with the initial LCC
    kiter = 0
    toremove = array.array('i', [])
    while Graph.number_of_nodes() > nrem:
        # The while-loop stops when there are no enough nodes in the Graph to be removed.
        i = 0
        if casekey == 2:  # BLOCK
            toremove = array.array('i', [])
            # BLOCK case:
            # Step1: Compute LCC size and Centralities scores,
            # Step2: Create an array of N nodes with the highest score (to be removed)
            # Step3: Back to Step1.
            # NB: The next node's score (in nrem nodes to be removed at once) WILL NOTE BE affected.
            dictx[kiter] = lcc_size(Graph)
            dicty[kiter] = 1 - (abs((lcc_size(Graph) - lccinit) / lccinit))
            if centrality_label == 'Collective Influence':
                toremove = collective_influence_centality(Graph, toremove, weight=weight)
            elif centrality_label != 'Collective Influence':
                toremove = max_centr(Graph, centrality_function, toremove, weight=weight)

        while i < nrem:
            if Graph.number_of_nodes() <= nrem:
                break
            if casekey == 1:  # SEQUENTIAL
                toremove = array.array('i', [])
                # SEQUENTIAL case:
                # Step1: Compute LCC size and Centralities scores,
                # Step2: Create an array of N nodes with the highest score (to be removed)
                # Step3: Back to Step1.
                # NB: The next node's score (in nrem nodes to be removed at once) WILL BE affected.
                dictx[kiter] = lcc_size(Graph)
                dicty[kiter] = 1 - (abs((lcc_size(Graph) - lccinit) / lccinit))
                if centrality_label == 'Collective Influence':
                    toremove = collective_influence_centality(Graph, toremove, weight=weight)
                elif centrality_label != 'Collective Influence':
                    toremove = max_centr(Graph, centrality_function, toremove, weight=weight)
            Graph.remove_node(toremove[0])
            toremove.pop(0)
            kiter += 1
            i += 1
    dflcc['No'] = list(dictx.keys())
    dflccvar['No'] = dflcc['No']
    dflcc[centrality_label] = list(dictx.values())
    dflccvar[centrality_label] = list(dicty.values())
    return dflcc, dflccvar


def degree_centrality_w(Graph, weight=None):
    # ToDo: In the future, it should be takes into account both number of in-edges and their weights.
    #  E.g. up to now, node A and node B has the same degree_centrality_w.
    #       node A with 3 links (a1,a2,a3) having the following weights: w_a1=3, w_a2_=2, w_a3=10.
    #       node B with 1 link (b1) having the following weight: w_b1=15.
    """Compute the degree centrality for nodes. From NetworkX, but adapted for weighted graphs.

    The degree centrality for a node v is the fraction of nodes it
    is connected to.

    Parameters
    ----------
    Graph : graph
      A networkx graph

    weight : None or string, optional (default=None)
      If None, all edge weights are considered equal.
      Otherwise holds the name of the edge attribute used as weight.

    Returns
    -------
    nodes : dictionary
       Dictionary of nodes with degree centrality as the value.
    """
    if len(Graph) <= 1:
        return {nn: 1 for nn in Graph}

    s = 1.0 / (len(Graph) - 1.0)
    # New implementation:
    if weight is None:
        centrality = {nn: d * s for nn, d in Graph.degree()}
    else:
        centrality = {nn: d * s for nn, d in Graph.degree(weight='weight')}
    return centrality


if __name__ == '__main__':
    for file, name in filename.items():  #  Iterate among the datasets: Meeting e Phone Calls

        #
        # Data Extraction
        #
        fin = open('../../dataset/' + file + '.csv', 'r')
        lines = fin.readlines()
        G = nx.Graph()
        for row in lines:
            r = row.split()
            n1, n2, w = int(r[0]), int(r[1]), int(r[2])
            G.add_edge(n1, n2, weight=w)
        print("\nDataset: ", name)
        print(nx.info(G), "\n")
        Gor = copy.deepcopy(G)
        #
        # Disruption
        #
        lcc_init = lcc_size(G)  # Original LCC
        cases = {1: 'sequential', 2: 'block'}
        w_enable = [None, 'weight']

        f = {
            'Betweenness': nx.betweenness_centrality,
            'Katz': nx.katz_centrality_numpy,
            'Collective Influence': collective_influence_centality,
            'Degree': degree_centrality_w
        }
        # NB: Use nx.katz_centrality_numpy instead of nx.katz_centrality otherwise PowerIterationFailedConvergence rise
        for ww in w_enable:  # Iterate between weighted (string) and unweighted (None, by default) versions.
            for k, v in cases.items():  # Iterate between Sequential and Block nodes removal.
                df_lcc = pd.DataFrame()
                df_lcc_var = pd.DataFrame()
                for colname, function in f.items():  # Iterate the centrality metrics to be used.
                    df_lcc, df_lcc_var = disruption(copy.deepcopy(Gor), function, colname, lcc_init,
                                                    df_lcc, df_lcc_var, k, ww)
                #
                # Exporting Results
                #
                if ww is None:
                    w_en = 'Unweighted'
                else:
                    w_en = 'Weighted'
                df_lcc_var.to_csv('../results/{0}/{1}/df_{2}_{3}nrem.csv'.format(v, name, w_en, nrem))
                # To plot the results, please run network-disruption-plots.py
