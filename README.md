MCMC norm learning
==================
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4772978.svg)](https://doi.org/10.5281/zenodo.4772978) [![DVC](https://img.shields.io/badge/-Data_Version_Control-white.svg?logo=data-version-control&style=social)](https://dvc.org/?utm_campaign=badge) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

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

**The supplementary material for IJCAI paper can be found at [Learning_Norms_with_MCMC_supp_material.pdf](https://github.com/ashish1610dhiman/learning_norms_with_mcmc_from_pcfg_IJCAI21/blob/non_compliance/Learning_Norms_with_MCMC_supp_material.pdf)**


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
$ pip install -r requirements.txt

# Or install depenencies in a conda env
$ conda create --name <env_name> --file requirements.txt
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
    ├── data_nc/*               <- Folder with dvc files for various experiments with p_nn > 0
    |
    ├── data/*                  <- Folder with dvc files for various experiments with p_nn = 0
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
    │                              the creator's initials, and a short `_` delimited description. The notebooks with tag 1.5 mark 
    |                              the files used for experiment shown in paper.
    |
    ├── params_nc.yaml          <- yaml file detailing parameters for experiments used
    │
    └── requirements.txt        <- The requirements file for reproducing the analysis environment
  


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- DATASET -->
<h2 id="dataset"> Dataset</h2>

The project uses [dvc](https://dvc.org/doc) for tracking data. There are two data folders in the repository:
1. data/: houses dvc files for data produced with older experiments
2. data_nc/: dvc files for data produced with **IJCAI submission experiments**. The dvc files follow naming as per the iteration of experiement, or exp_nc{i}: for i ∈ {1,2,... , 5}

**[exp_nc5.dvc](https://github.com/ashish1610dhiman/learning_norms_with_mcmc_from_pcfg_IJCAI21/blob/non_compliance/data_nc/exp_nc5.dvc) is the file corresponding to experiment presented in paper**

Use the following commands to download the data corresponding to a dvc file:

```bash
# fetch the data
$ dvc fetch exp_nc5.dvc

# checkout the branch
$ dvc checkout
```



![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- ROADMAP -->
<h2 id="roadmap"> Roadmap</h2>

As outlined in the <a href="#about-the-project"> About The Project</a> above, MCMC Norm learning pipleine involves the following steps:  

1. Initialise a Environment and task
2. Generate obervations
3. Generate MCMC chains
4. Analyse MCMC chains
5. Run Convergence tests on MCMC chains
6. Get Top Norms from chains

The above steps are outlined in the binding script [nc_experiments.py](https://github.com/ashish1610dhiman/learning_norms_with_mcmc_from_pcfg_IJCAI21/blob/non_compliance/scripts/nc_experiments.py).

Jupyter notebook is then used as awrapper over nc_experiments.py, to run different experiment iterations. The naming scheme of notebooks is mentioned above in <a href="#folder-structure"> Project Organsisation</a></li>.

**[1.5_nc_exp5.ipynb](https://github.com/ashish1610dhiman/learning_norms_with_mcmc_from_pcfg_IJCAI21/blob/non_compliance/notebooks/1.5_nc_exp5.ipynb) is the notebook used to run experiment presented in paper**

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- CONTRIBUTORS -->
<h2 id="contributors"> Contributors</h2>

1. Stephen Cranefield  
  Department of Information Science, University of Otago  
  [![Google Scholar](https://img.icons8.com/color/48/000000/google-scholar--v3.png) Google Scholar](hhttps://scholar.google.com/citations?user=IVcTzugAAAAJ)  
    

2. Ashish Dhiman  
  Connect on [![Linkedin](https://i.stack.imgur.com/gVE0j.png) LinkedIn](https://www.linkedin.com/in/ashish1610dhiman/)