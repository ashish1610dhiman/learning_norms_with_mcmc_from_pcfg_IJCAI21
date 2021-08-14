MCMC norm learning
==================
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4772978.svg)](https://doi.org/10.5281/zenodo.4772978)

<!-- TABLE OF CONTENTS -->
<h2 id="table-of-contents"> Table of Contents</h2>

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project"> ➤ About The Project</a></li>
    <li><a href="#prerequisites"> ➤ Prerequisites</a></li>
    <li><a href="#folder-structure"> ➤ Project Organsisation</a></li>
    <li><a href="#dataset"> ➤ Dataset</a></li>
    <li><a href="#roadmap"> ➤ Roadmap</a></li>
    <li><a href="#contributors"> ➤ Contributors</a></li>
  </ol>
</details>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)
  
<!-- ABOUT THE PROJECT -->
<h2 id="about-the-project"> About The Project</h2>

This repository contains the source code used for experiments in the paper: #TODO:add doi for paper

The project covers the steps as given in the schematic below:
![image](https://user-images.githubusercontent.com/23236895/118816860-3eb9bb80-b8d0-11eb-8aac-38e9bf3a1960.png)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)



<!-- PREREQUISITES -->
<h2 id="prerequisites"> Prerequisites</h2>
<!--This project is written in Python programming language. <br>-->

To clone and run this application, you'll need to follow the below-mentioned steps:

```bash
# Clone this repository
$ git clone https://github.com/ashish1610dhiman/learning_norms_with_mcmc_from_pcfg_IJCAI21

# Go into the repository
$ cd learning_norms_with_mcmc_from_pcfg_IJCAI21

# Install depenencies using pip
pip install -r requirements.txt

# Install depenencies using conda
conda create --name <env_name> --file requirements.txt
```

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- FOLDER STRUCTURE -->
<h2 id="folder-structure"> Project Organization</h2>



--------------------


    ├── LICENSE
    |
    ├── README.md               <- The top-level README.
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
    ├── params_nc.yaml          <- yaml file detailing parameters for experiments used
    │
    └── requirements.txt        <- The requirements file for reproducing the analysis environment
  


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- DATASET -->
<h2 id="dataset"> Dataset</h2>

#TODO add data intro/structure and how to checkout with dvc

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- ROADMAP -->
<h2 id="roadmap"> Roadmap</h2>

#TODO add experiment structure, and notebooks used, and yaml param files


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- CONTRIBUTORS -->
<h2 id="contributors"> Contributors</h2>
#TODO add intro