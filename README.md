MCMC norm learning
==================
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4772978.svg)](https://doi.org/10.5281/zenodo.4772978)

This repository contains the source code used for experiments in the paper: #TODO:add doi for paper

<!-- TABLE OF CONTENTS -->
<h2 id="table-of-contents"> Table of Contents</h2>

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project"> ➤ About The Project</a></li>
    <li><a href="#prerequisites"> ➤ Installation</a></li>
    <li><a href="#folder-structure"> ➤ Folder Structure</a></li>
    <li><a href="#dataset"> ➤ Dataset</a></li>
    <li><a href="#roadmap"> ➤ Roadmap</a></li>
    <li><a href="#contributors"> ➤ Contributors</a></li>
  </ol>
</details>

The project covers the steps:
![image](https://user-images.githubusercontent.com/23236895/118816860-3eb9bb80-b8d0-11eb-8aac-38e9bf3a1960.png)






Project Organization
--------------------


    ├── LICENSE
    |
    ├── README.md               <- The top-level README for developers using this project.
    |
    ├── *_supp_material.pdf     <- Supplemetary material for paper published in IJCAI-21.
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
    │   └── nc_experiments.py   <- Binding script used to run various parts of experiment
    |
    ├── notebooks               <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                              the creator's initials, and a short `-` delimited description, e.g.
    │                              `1.0-jqp-initial-data-exploration`. The notebooks with tag 1.5 mark 
    |                              the files used for experiment shown in paper.
    |
    ├── **params_nc.yaml**      <- yaml file detailing parameters for experiments used
    │
    ├── requirements.txt        <- The requirements file for reproducing the analysis environment, e.g.
    │                              generated with `pip freeze > requirements.txt`
    │
    │
    └── venv/                   <- Virtual environment used for experiments
