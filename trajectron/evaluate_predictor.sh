declare -a data_names=("univ")
#"zara2" "zara1" "hotel" "univ" "eth"
declare -a dirs=("mixup_uniform_vel" "mixup_uniform_attention_radius_3")
for dir in "${dirs[@]}";
do for data_name in "${data_names[@]}";
do (CUDA_VISIBLE_DEVICES=0 python evaluate.py --model ../experiments/pedestrians/${dir}/${data_name} --checkpoint 100 --data ../experiments/processed/${data_name}_test.pkl)
done;
done;