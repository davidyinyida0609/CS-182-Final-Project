declare -a dirs=("baseline_attention_radius_3" "mixup_uniform_attention_radius_3" "baseline_vel" "mixup_uniform_vel")
for dir in "${dirs[@]}";
    do python analysis.py --log_dir ../experiments/pedestrians/${dir}
done;
