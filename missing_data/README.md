# Network Missing Data

This project has been developed to analyse complex networks similarities.

_Data collected in criminal investigations may suffer from issues like: (i) incompleteness, due to the covert nature of criminal organizations; (ii) incorrectness, caused by either unintentional data collection errors or intentional deception by criminals; (iii) inconsistency, when the same information is collected into law enforcement databases multiple times, or in different formats. In this paper we analyze nine real criminal networks of different nature (i.e., Mafia networks, criminal street gangs and terrorist organizations) in order to quantify the impact of incomplete data, and to determine which network type is most affected by it. The networks are firstly pruned using two specific methods: (i) random edge removal, simulating the scenario in which the Law Enforcement Agencies fail to intercept some calls, or to spot sporadic meetings among suspects; (ii) node removal, modeling the situation in which some suspects cannot be intercepted or investigated. Finally we compute spectral distances (i.e., Adjacency, Laplacian and normalized Laplacian Spectral Distances) and matrix distances (i.e., Root Euclidean Distance) between the complete and pruned networks, which we compare using statistical analysis. Our investigation identifies two main features: first, the overall understanding of the criminal networks remains high even with incomplete data on criminal interactions (i.e., when 10% of edges are removed); second, removing even a small fraction of suspects not investigated (i.e., 2% of nodes are removed) may lead to significant misinterpretation of the overall network._

To re-use the dataset or the source code, please plese do not forget to cite us [[1]](#1):

```
@article{10.1371/journal.pone.0255067,
	doi = {10.1371/journal.pone.0255067},
    	author = {Ficara, Annamaria AND Cavallaro, Lucia AND Curreri, Francesco AND Fiumara, Giacomo AND De Meo, Pasquale AND Bagdasar, Ovidiu AND Song, Wei AND Liotta, Antonio},
    	journal = {PLOS ONE},
    	publisher = {Public Library of Science},
    	title = {Criminal networks analysis in missing data scenarios through graph distances},
    	year = {2021},
    	month = {08},
    	volume = {16},
    	url = {https://doi.org/10.1371/journal.pone.0255067},
    	pages = {1-18},
    	number = {8},
}
```


## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Packages](#packages)

## General info
This project has been developed to to quantify the impact of incomplete data and to determine which real complex network is most affected by it. For further details, please refers to our work [[1]](#1).
	
## Technologies
Project is created with:
* Python version: 3.7.3

With the following libraries:
* NetworkX library version: 2.3
* Numpy library version: 1.16.4
* Pandas library version: 0.25.1

Additional libraries:
* PrettyTable library version: 2.0.0
	
## Setup
To run this project, run missing_data_main.py. 
```
$ python missing_data_main.py
```

* The main automatically will import the datasets from the "Datasets" folder, and will store the results obtained in the related sub-folder of the "Results" one.

## Packages
The computational functions are in the utilspackage sub-folder and are grouped as follows:
* file_utils.py : Cointains the functions to manipulate the graphs source files
* math_utils.py : Cointains the functions to manipulate the graphs themselves

## References

<a id="1">[1]</a> 
Ficara, A., and Cavallaro, L., and Curreri, F., and Fiumara, G., and De Meo, P., and Bagdasar, O., and Song, W., and Liotta, A. (2021) 
Criminal networks analysis in missing data scenarios through graph distances.
PLOS ONE 16(8): e0255067. https://doi.org/10.1371/journal.pone.0255067 
