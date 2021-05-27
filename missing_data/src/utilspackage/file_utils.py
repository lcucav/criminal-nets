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

import networkx as nx

def read_graph_from_file(filepath):
    """
    Read a Graph from a csv file.
    :param filepath: (str) String of the complete path file (including file name) without the file extension
    :return: (Graph obj: networkx.classes.graph.Graph) Return the Graph object
    """
    fin = open(filepath + '.csv', 'r')
    lines = fin.readlines()
    Graph = nx.Graph()
    for row in lines:
        r = row.split()
        n1, n2, w = int(r[0]), int(r[1]), int(r[2])
        Graph.add_edge(n1, n2, weight=w)
    return Graph

def relabeling_graph(Graph):
    """
    Relabel nodes of a Graph keeping the old nodes' labels in a dictionary.
    keys: the original nodes labels
    values: the new nodes labels in ascending order from 0
    :param Graph: (Graph obj: networkx.classes.graph.Graph) Input Graph
    :return mapping_dict: (dict) Return the dictionary that keeps trace of the original nodes labels
    :return G_relabel: (Graph obj: networkx.classes.graph.Graph) Return the Graph object
    """
    counter = 0
    mapping_dict = {}
    for i in Graph.nodes():
        mapping_dict[i] = counter
        counter += 1
    G_relabel = nx.relabel_nodes(Graph, mapping_dict)
    return G_relabel, mapping_dict

def ptable_to_csv(table, filename, headers=True):
    """Save PrettyTable results to a CSV file.

    Adapted from @AdamSmith https://stackoverflow.com/questions/32128226

    :param PrettyTable table: Table object to get data from.
    :param str filename: Filepath for the output CSV.
    :param bool headers: Whether to include the header row in the CSV.
    :return: None
    """
    raw = table.get_string()
    data = [tuple(filter(None, map(str.strip, splitline)))
            for line in raw.splitlines()
            for splitline in [line.split('|')] if len(splitline) > 1]
    if table.title is not None:
        data = data[1:]
    if not headers:
        data = data[1:]
    with open(filename, 'w') as f:
        for d in data:
            f.write('{}\n'.format(','.join(d)))
