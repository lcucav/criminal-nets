# Network Missing Data

This project has been developed to evaluate the  complex networks.

To re-use the dataset or the source code, please cite us:
@article{ficaracavallaroetal2021missingdata,
    title={Criminal Networks Analysis in Missing Data scenarios through Graph Distances},
    author={Ficara, Annamaria and Cavallaro, Lucia and Curreri, Francesco and Fiumara, Giacomo and De Meo,
            Pasquale and Bagdasar, Ovidiu and Song, Wei and Liotta, Antonio},
    year={2021},
    eprint={2103.00457},
    archivePrefix={arXiv},
    primaryClass={cs.SI}
}


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
Ficara, A., and Cavallaro, L., and Curreri, F., and Fiumara, G., and De Meo, P., and Bagdasar, O., and Song, W., and Liotta, A. (2021). 
Criminal Networks Analysis in Missing Data scenarios through Graph Distances
https://arxiv.org/abs/2103.00457
