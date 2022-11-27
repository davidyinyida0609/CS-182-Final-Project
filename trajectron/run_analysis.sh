declare -a dirs=("baseline" "mixup")
for dir in "${dirs[@]}";
    do python analysis.py --log_dir ../experiments/pedestrians/${dir}
done;
