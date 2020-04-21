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

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

names = ['id', 'data']
formats = ['int32', 'int32']
dtype = dict(names=names, formats=formats)

filename = {'Montagna_meetings_edgelist': 'meeting', 'Montagna_phonecalls_edgelist': 'phone_calls'}
nrem = 5  # top valued nodes to be removed


def plot_creation(tosave, dflcc, typerem, input_name, w):
    """
    Network Disruption Plot.

    :param tosave: (string) name path.
    :param dflcc: (pandas.core.frame.DataFrame) Largest Connected Component Dataframe.
    :param typerem: (string) Type of node removal. It can be 'sequential' or 'block'
    :param input_name: (string) Name of Input Dataset. It can be 'Meeting' or 'PhoneCalls'
    :param w: (string) it can be 'Weighted' or 'Unweighted'
    (Dataframe composed by: Iter_Num, LCC size after node removal according to the Centrality_Metrics).
    """
    colnames = list(dflcc.columns)
    # Uncomment below to test what it is plotting by putting a title on the plot itself. If so, change function inputs.
    # plt.title(r" {0} Dataset: {1}, {2} Removals, nrem:{3} ".format(files_name[files_key], w, typerem, nrem),
    #          fontsize=22, color='gray')
    sns.set_style("white")
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['figure.figsize'] = [20, 10]
    plt.rcParams["axes.labelweight"] = "bold"

    xlabel = colnames[1]
    idx1 = (list(range(0, 20, 5)))  # per vedere in dettaglio i valori iniziali
    idx2 = (list(range(20, (int(df["No"].tail(1))), 10)))  # per fissare a priori le ascisse con valori interi
    idx = idx1 + idx2
    idx.append(int(df["No"].tail(1)))  # per stampare anche l'ultimo valore
    plt.grid(True, linestyle=':')
    for ylab in colnames[2:]:
        ax = sns.lineplot(x=xlabel, y=ylab, markers=True, dashes=False, data=dflcc, label=ylab, lw=4, marker="o")
    # noinspection PyUnboundLocalVariable
    ax.set_xticks(idx)
    ax.set_xlabel(r'$i$', fontsize=24)
    ax.set_ylabel(r'$\rho_i$', fontsize=24)
    ax.legend(fontsize=24)  # , prop=legend_properties)
    ax.tick_params(labelsize=24)
    # Uncomment below for a detailed plot of first 30 iterations, discarding the others.
    # ax.set(xlim=(0, 30))
    fig = plt.gcf()
    fig.set_size_inches((11, 9), forward=False)
    fig.savefig(tosave + '{0}_{1}_{2}-plos.eps'.format(input_name, typerem, w, nrem),
                dpi=300, format='eps')
    fig.clf()


if __name__ == '__main__':
    w_enable = [None, 'weight']
    cases = {1: 'sequential', 2: 'block'}
    for file, name in filename.items():
        for ww in w_enable:
            for k, v in cases.items():
                if ww is None:
                    w_en = 'Unweighted'
                else:
                    w_en = 'Weighted'
                path = ('../results/{0}/{1}/'.format(v, name))
                df = pd.read_csv(path + 'df_{0}_{1}nrem.csv'.format(w_en, nrem))
                plot_creation(path, df, v, name, w_en)
