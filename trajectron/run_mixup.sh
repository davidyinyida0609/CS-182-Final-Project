#!/bin/bash

declare -a data_names=("univ")
declare -a confs=("attention_radius_3" "vel")
declare -a dists=("uniform" "beta")

for conf in "${confs[@]}";
do for data_name in "${data_names[@]}";
do for dist in "${dists[@]}";
do 
    (CUDA_VISIBLE_DEVICES=3 python train_mixup.py --eval_every 1 --save_every 100 --vis_every 1 --dist ${dist}  --data_dir ../experiments/processed --train_data_dict ${data_name}_train.pkl --eval_data_dict ${data_name}_val.pkl --offline_scene_graph yes --preprocess_workers 5 --log_dir ../experiments/pedestrians/mixup_${dist}_${conf} --log_tag ${data_name} --train_epochs 100 --augment --conf ../experiments/pedestrians/models/${data_name}_${conf}/config.json)
done;
done;
done;