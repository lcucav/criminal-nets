# Network Disruption

This project has been developed to disrupt complex networks.

_Compared to other types of social networks, criminal networks present particularly hard challenges, due to their strong resilience to disruption, which poses severe hurdles to Law-Enforcement Agencies (LEAs). Herein, we borrow methods and tools from Social Network Analysis (SNA) to (i) unveil the structure and organization of Sicilian Mafia gangs, based on two real-world datasets, and (ii) gain insights as to how to efficiently reduce the Largest Connected Component (LCC) of two networks derived from them. Mafia networks have peculiar features in terms of the links distribution and strength, which makes them very different from other social networks, and extremely robust to exogenous perturbations. Analysts also face difficulties in collecting reliable datasets that accurately describe the gangs’ internal structure and their relationships with the external world, which is why earlier studies are largely qualitative, elusive and incomplete. An added value of our work is the generation of two real-world datasets, based on raw data extracted from juridical acts, relating to a Mafia organization that operated in Sicily during the first decade of 2000s. We created two different networks, capturing phone calls and physical meetings, respectively. Our analysis simulated different intervention procedures: (i) arresting one criminal at a time (sequential node removal); and (ii) police raids (node block removal). In both the sequential, and the node block removal intervention procedures, the Betweenness centrality was the most effective strategy in prioritizing the nodes to be removed. For instance, when targeting the top 5% nodes with the largest Betweenness centrality, our simulations suggest a reduction of up to 70% in the size of the LCC. We also identified that, due the peculiar type of interactions in criminal networks (namely, the distribution of the interactions’ frequency), no significant differences exist between weighted and unweighted network analysis. Our work has significant practical applications for perturbing the operations of criminal and terrorist networks._


To re-use the dataset or the source code, plese do not forget to cite us [[1]](#1):
```
@misc{cavallaro2020disrupting,
    title={Disrupting Resilient Criminal Networks through Data Analysis: The case of Sicilian Mafia},
    author={Lucia Cavallaro and Annamaria Ficara and Pasquale De Meo and Giacomo Fiumara and Salvatore Catanese and Ovidiu Bagdasar and Antonio Liotta},
    year={2020},
    eprint={2003.05303},
    archivePrefix={arXiv},
    primaryClass={cs.SI}
}
```

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project has been developed to disrupt real complex networks. For further details, please refers to our work [[1]](#1).
	
## Technologies
Project is created with:
* Python version: 3.7.3

With the following libraries:
* NetworkX library version: 2.3
* Numpy library version: 1.16.4
* Pandas library version: 0.25.1

Additional libraries (to plot the results):
* Matplotlib library version: 3.1.1
* Seaborn library version: 0.9.0
	
## Setup
To run this project, run network-disruption.py. 
```
$ python network-disruption.py
```

* The main automatically will import the datasets from the "Datasets" folder, and will store the results obtained in the related sub-folder of the "Results" one.

To plot the results, run network-disruption-plots. 
```
$ python network-disruption-plots.py
```

* The main automatically will import the input DataFrame from the appropriate "Results" sub-folder, and will store the plots obtained in the related sub-folder of the "Results" one.

## References

<a id="1">[1]</a> 
Cavallaro, L., and Ficara, A., and De Meo, P., and Fiumara, G., and Catanese, S., and Bagdasar, O., and Liotta, A. (2020). 
Disrupting Resilient Criminal Networks through Data Analysis: The case of Sicilian Mafia.
PLOS ONE 15(8): e0236476. https://doi.org/10.1371/journal.pone.0236476 
