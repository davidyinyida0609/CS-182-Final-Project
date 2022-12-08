# Mixup in Agent Forecasting #
This codebase is the implementation for the final project in Fall 2022 CS 182 Final Project.
Our paper is [Mixup in Agent Forecasting](CS_182_Final_Project_Paper.pdf).

The majority of the codebase is from [Trajectron++](https://github.com/StanfordASL/Trajectron-plus-plus). Its paper link is 
[Trajectron++: Dynamically-Feasible Trajectory Forecasting With Heterogeneous Data](https://arxiv.org/abs/2001.03093)

by Tim Salzmann\*, Boris Ivanovic\*, Punarjay Chakravarty, and Marco Pavone (\* denotes equal contribution).
## Cloning ##
When cloning this repository, make sure you clone the submodules as well, with the following command:
```
git clone --recurse-submodules <repository cloning URL>
```
Alternatively, you can clone the repository as normal and then load submodules later with:
```
git submodule init # Initializing our local configuration file
git submodule update # Fetching all of the data from the submodules at the specified commits
```

## Environment Setup ##
First, we'll create a conda environment to hold the dependencies.
```
conda create --name trajectron++ python=3.6 -y
source activate trajectron++
pip install -r requirements.txt
```

## Data Setup ##
We've already included preprocessed data splits for the ETH and UCY Pedestrian datasets in this repository, you can see them in `experiments/pedestrians/raw`. In order to process them into a data format that our model can work with, execute the follwing.
```
cd experiments/pedestrians
python process_data.py # This will take around 10-15 minutes, depending on your computer.
```
## Replicate Experiments ##
We have already written all the bash code you need to run in order to obtain the baseline and two different kinds of mixup models. You need first go into `trajectron` directory.
To train all the baseline results, run
```
bash run_baseline.sh
```
To train all the mixup results on train set, run
```
bash run_mixup.sh
```
You can find all trained model in `experiments/pdestrians`.
There are two types of Trajectron++ baseline models. One is with dynamic integration, whose model suffix is attention_radius_3, and the other is without, whose suffix is vel.

To evaluate all the trained models (both baseline ones and mixup ones) on test set, run
```
bash evaluate_predictor.sh
```
To analyze the results from all the models, run
```
bash run_analysis.sh
```
It will then display the folder name of that generic model along with the result in a table. You can also retrieve that result in the file called `{folder_name}/best_of_20.csv`.

If you want understand the hyperparameters in the training bash code, I strongly recommend take a look at [Trajectron++ codebase](https://github.com/StanfordASL/Trajectron-plus-plus)
