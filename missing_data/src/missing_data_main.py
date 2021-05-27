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

"""Compute the spectral and matrix distances of a real criminal network with its edges-pruned versions"""

import utilspackage.file_utils as utils
import utilspackage.math_utils as math
import networkx as nx
import prettytable
import numpy as np

# Datasets setup
names = ['id', 'data']
formats = ['int32', 'int32']
dtype = dict(names=names, formats=formats)
filename = {'Montagna_phonecalls_edgelist': 'PhoneCalls',
            'Montagna_meetings_edgelist': 'Meetings',
            'Infinito_suspects': 'Infinito_Suspects',
            'Oversize_AW': 'Oversize_AW',
            'Oversize_JU': 'Oversize_JU',
            'Oversize_WR': 'Oversize_WR',
            'caviar_edgelist': 'Caviar',
            'philikidnap_terrorists': 'Philikidnap_Terrorists',
            'stockholm-gang-SN': 'Stockholm_Gang_SN'}

# Simulations Configuration
nrep = 100  # ToDo: to be adjusted
np.set_printoptions(precision=3, suppress=True)
torem = 0.15  # Fraction of edges to be removed 0.125
check = False  # if True, remove adjacent edges (i.e., remove the node and re-add as isolated).

if __name__ == '__main__':
    for file, name in filename.items():

        # Reading from the file and creation of the real graph
        path = '../../dataset/' + file
        G_real = utils.read_graph_from_file(path)
        nodes = nx.number_of_nodes(G_real)
        if list(G_real.nodes) != [*range(0, nodes)]:
            [G_real, mapping] = utils.relabeling_graph(G_real)

        # Printing Graph info
        print("\nOriginal Real Graph\nDataset: ", name)
        print(nx.info(G_real), "\n")

        # Definition of the number of edges to be removed (random or incident)
        if check is True:
            rem = "No. nodes"
            number_toberemoved = int(torem * G_real.number_of_nodes())
            print("Will be removed", number_toberemoved, "nodes")
            rtype = "node"
        else:
            rem = "No. edges"
            number_toberemoved = int(torem * G_real.number_of_edges())
            print("Will be removed", number_toberemoved, "edges")
            rtype = "edge"

        labels = [rem, "Dist. A", "Err. A", "Dist. LA", "Err. LA", "Dist. NLA", "Err. NLA", "S", "Err. S", "Sim."]
        t = prettytable.PrettyTable(labels)

        # Configuration parameters
        S = math.compute_S(G_real)  # Compute the fast belief propagation matrix  to compute the

        # Matrices computation of the original graph
        ENXA = nx.adjacency_spectrum(G_real, weight=None)
        ENXLA = nx.laplacian_spectrum(G_real, weight=None)
        ENXNLA = nx.normalized_laplacian_spectrum(G_real, weight=None)

        # Computation of the spectral and matrix distances
        var = 0
        for j in range(number_toberemoved):
            dist_A = np.zeros(nrep)
            dist_LA = np.zeros(nrep)
            dist_NLA = np.zeros(nrep)
            Diff = np.zeros(nrep)
            for i in range(nrep):
                Gm, var = math.network_links_pruning(G_real, j, adj=check)
                Sm = math.compute_S(Gm)
                Diff[i] = math.compute_Matsusita_difference(nodes, S, Sm)
                config = zip(ENXA, ENXLA, ENXNLA)
                dist_A[i], dist_LA[i], dist_NLA[i] = math.compute_spectral_distances(G_real, Gm, config)

            # Computation of statistics for Matsusita difference
            dave, derr = math.compute_statistics(Diff, 3)
            dsim = np.around(1 / (1 + dave), decimals=3)  # Compute the DeltaCon Similarity in [0,1] of the averaged res

            # Computation of statistics for spectral distances
            ave_da, std_da = math.compute_statistics(dist_A, 3)
            ave_dla, std_dla = math.compute_statistics(dist_LA, 3)
            ave_dnla, std_dnla = math.compute_statistics(dist_NLA, 3)

            # Saving statistics on a PrettyTable
            t.add_row([var, ave_da, std_da, ave_dla, std_dla, ave_dnla, std_dnla, dave, derr, dsim])
        print(t)
        utils.ptable_to_csv(t, "../results/{0}_dist_statistics_nrep{1}_fract{2}_{3}.csv".format(name, nrep, torem, rtype))
