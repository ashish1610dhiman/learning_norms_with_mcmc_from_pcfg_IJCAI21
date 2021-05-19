MCMC norm learning
==================
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4771919.svg)](https://doi.org/10.5281/zenodo.4771919)

This repository contains the source code used for experiments in the paper: #TODO:add doi for paper

The project covers the steps:
![image](https://user-images.githubusercontent.com/23236895/118816860-3eb9bb80-b8d0-11eb-8aac-38e9bf3a1960.png)




Project Organization
--------------------


    ├── LICENSE
    |
    ├── README.md               <- The top-level README for developers using this project.
    |
    ├── data_nc/*               <- Folder with dvc files for various experiments with $p_nn$ > 0
    |
    ├── data/*                  <- Folder with dvc files for various experiments with $p_nn$ = 0
    |
    ├── src/
    │   ├── mcmc_norm_*         <- Code files for grammar/Metropolis Hastings Algorithm/convergence
    |   |                          and preciscion-recall
    │   └── *.py                <- Small Helper files
    │
    ├── scripts/                <- Scripts used for variouis instances of the process depicted in 
    |   |                          schematic above.
    │   └── **nc_experiments.py**   <- Binding script used to run various parts of experiment
    |
    ├── notebooks               <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                              the creator's initials, and a short `-` delimited description, e.g.
    │                              `1.0-jqp-initial-data-exploration`. **The notebooks with tag 1.5 mark 
    |                              the files used for experiment shown in paper.**
    |
    ├── **params_nc.yaml**      <- yaml file detailing parameters for experiments used
    │
    ├── requirements.txt        <- The requirements file for reproducing the analysis environment, e.g.
    │                              generated with `pip freeze > requirements.txt`
    │
    │
    └── venv/                   <- Virtual environment used for experiments
