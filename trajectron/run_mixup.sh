#!/bin/bash

# change this!
declare -a data_names=("zara1" "univ" "zara2" "eth" "hotel")
declare -a confs=("attention_radius_3")

for conf in "${confs[@]}";
do for data_name in "${data_names[@]}";
do 
    (CUDA_VISIBLE_DEVICES=0 python train_mixup.py --eval_every 100 --save_every 100 --vis_every 1 --data_dir ../experiments/processed --train_data_dict ${data_name}_train.pkl --eval_data_dict ${data_name}_test.pkl --offline_scene_graph yes --preprocess_workers 5 --log_dir ../experiments/pedestrians/baseline --log_tag _${data_name}_${conf} --train_epochs 100 --augment --conf ../experiments/pedestrians/models/${data_name}_${conf}/config.json)
done;
done;