# Network Disruption

This project has been developed to disrupt complex networks.

To re-use the dataset or the source code, please cite us:

@misc{cavallaro2020disrupting,
    title={Disrupting Resilient Criminal Networks through Data Analysis: The case of Sicilian Mafia},
    author={Lucia Cavallaro and Annamaria Ficara and Pasquale De Meo and Giacomo Fiumara and Salvatore Catanese and Ovidiu Bagdasar and Antonio Liotta},
    year={2020},
    eprint={2003.05303},
    archivePrefix={arXiv},
    primaryClass={cs.SI}
}

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
http://arxiv.org/abs/2003.05303v1
