# If you use parts of this code please cite the following articles:

# @article{ficaracavallaroetal2021missingdata,
#     title={Criminal Networks Analysis in Missing Data scenarios through Graph Distances},
#     author={Ficara, Annamaria and Cavallaro, Lucia and Curreri, Francesco and Fiumara, Giacomo and De Meo,
#             Pasquale and Bagdasar, Ovidiu and Song, Wei and Liotta, Antonio},
#     year={2021},
#     eprint={2103.00457},
#     archivePrefix={arXiv},
#     primaryClass={cs.SI}
# }

__author__ = "Lucia Cavallaro, and Giacomo Fiumara, and Annamaria Ficara"
__version__ = "0.0.1"

import utilspackage.file_utils as utils
import networkx as nx
import random
import copy
import numpy as np

def compute_S(Graph):
    """
    Compute S needed for DeltaCon distance.
    :param Graph: (Graph obj: networkx.classes.graph.Graph) Input Graph
    :return S: (numpy.matrix) Return the S matrix
    """
    n = nx.number_of_nodes(Graph)
    d_max = max_degree(Graph)
    eps = 1 / (1 + d_max)

    # if the nodes' names are not in ascending order D matrix cannot be computed. Thus, it relabels nodes' names.
    if list(Graph.nodes) != [*range(0, n)]:
        [Graph, mapping] = utils.relabeling_graph(Graph)
        # mapping is the dictionary that keeps trace of the original nodes labels in case there is this need
    degree_g = nx.degree(Graph)
    AM = nx.to_numpy_matrix(Graph, weight=None)  # adj matrix eigenvalues
    D = np.zeros([n, n])  # degree matrix initialisation

    for node, degree in degree_g:
        D[node, node] = degree
    S = np.linalg.inv(np.identity(n) + eps * eps * D - eps * AM)
    return S

def compute_Matsusita_difference(n, S1, S2):
    """
    Compute Matsusita difference (also called root euclidean distance).
    :param n: (int) number of nodes of the graphs to be compared of the same size.
    :param S1: (numpy.matrix) The the S matrix of the first Input graph
    :param S2: (numpy.matrix) The the S matrix of the second Input graph
    :return result: ('numpy.float64') Return the Matsusita difference
    """
    counter = 0
    for k in range(n):
        for j in range(n):
            counter += (S1[k, j] - S2[k, j]) * (S1[k, j] - S2[k, j])
    result = np.sqrt(counter)
    return result

def compute_spectral_distances(Graph1, Graph2, matrices=None):
    """
    Compute three spectral distances between two graphs (i.e., Adjacency matrix, Laplacian, and Normalised Laplacian)
    If the flag real is set to True and the ENXA, ENXLA, and ENXNLA parameters of Graph1 are given, the function
    will skip their computation.
    :param Graph1: (Graph obj: networkx.classes.graph.Graph) Input Graph1
    :param Graph2: (Graph obj: networkx.classes.graph.Graph) Input Graph2
    :param matrices: (zip obj) zip of NetworkX adjacency,laplacian and normalizes laplacian spetra. None by default

    :return: (numpy.float64) Return the three spectral distances between the two graphs:
                             adjacency, laplacian and normalised laplacian
    """
    # If matrices!=None, unzip in ENXA ENXLA ENXNLA; otherwhise compute them.
    if matrices is None:
        # computing eigenvalues of the: adjacency matrix, laplacian and normalized laplacian of Graph1
        ENXA = nx.adjacency_spectrum(Graph1, weight=None)
        ENXLA = nx.laplacian_spectrum(Graph1, weight=None)
        ENXNLA = nx.normalized_laplacian_spectrum(Graph1, weight=None)
    else:
        ENXA, ENXLA, ENXNLA = zip(*matrices)
    # computing eigenvalues of the: adjacency matrix, laplacian and normalized laplacian of Graph2
    ENXM = nx.adjacency_spectrum(Graph2, weight=None)
    ENXLM = nx.laplacian_spectrum(Graph2, weight=None)
    ENXNLM = nx.normalized_laplacian_spectrum(Graph2, weight=None)
    # computing de spectral distances between the two graphs
    DistA = np.sqrt(np.sum(np.square(np.real(ENXA - ENXM))))
    DistL = np.sqrt(np.sum(np.square(np.real(ENXLA - ENXLM))))
    DistNL = np.sqrt(np.sum(np.square(np.real(ENXNLA - ENXNLM))))
    return DistA, DistL, DistNL

def distribution(Graph):
    """
    Given a networkx graph returns a list containing the nodes repeated as many times as their degree
    This distribution is used to select a node for Preferential Attachment
    Compute S needed for DeltaCon distance.
    :param Graph: (Graph obj: networkx.classes.graph.Graph) Input Graph
    :return distr: (list) Return a list containing the nodes repeated as many times as their degree
    """
    G_degree = list(Graph.degree())
    distr = []
    for nodeid, deg in G_degree:
        distr.extend([nodeid] * deg)
    return distr

def max_degree(Graph):
    """
    Compute the maximum degree of a Graph.
    :param Graph: (Graph obj: networkx.classes.graph.Graph) Input Graph
    :return dmax: (int) Return the maximum degree of a Graph
    """
    degree_g = nx.degree(Graph)
    dmax = 0
    for n, d in degree_g:
        if d > dmax:
            dmax = d
    return dmax

def network_links_pruning(Graph, fraction, adj=False):
    """
    Prune the network by removing a certain amount of edges.
    If node is true, the removed edges are incident on specific nodes
    If edges is true, edges are removed without the check of the incident nodes edges.
    The function return the pruned graph and the number of the removed edges.
    will skip their computation.
    :param Graph: (Graph obj: networkx.classes.graph.Graph) Input Graph
    :param fraction: (int) Number of nodes (or edges) to be removed at once.
    :param adj: (bool) If true, remove incident edges on a specific node from the network.
                       Otherwise, removes edges from the network.
    :return: Graph: (Graph obj: networkx.classes.graph.Graph) Pruned Graph
    :return: var: (int) Number of edges removed
    """
    Gm = copy.deepcopy(Graph)
    if adj:
        removed_nodes = 0
        indices = []
        while removed_nodes < fraction:
            list_of_nodes = list(Gm.nodes())
            index = random.randint(0, len(list_of_nodes) - 1)
            if Gm.neighbors(index) != 0 and index not in indices:
                Gm.remove_node(index)
                Gm.add_node(index)
                removed_nodes += 1
                indices.append(index)
        var = Gm.number_of_edges()
    else:
        for edge in range(fraction):
            list_of_edges = list(Gm.edges())
            index = random.randint(0, len(list_of_edges) - 1)
            Gm.remove_edge(*list_of_edges[index])
        var = Gm.number_of_edges()
    return Gm, var

def compute_statistics(tocompute, toround):
    """
    Given a numpy array, returns its rounded average and standard deviation as floats
    :param tocompute: ('numpy.ndarray') Input data to be computed the rounded average and standard deviation
    :param toround: (int) The decimals to be rounded
    :return out: ('numpy.float64') Return the rounded average
    :return err: ('numpy.float64') Return the rounded standard deviation
    """
    out, err = np.average(tocompute), np.std(tocompute)
    out, err = np.around(out, decimals=toround), np.around(err, decimals=toround)
    return out, err
