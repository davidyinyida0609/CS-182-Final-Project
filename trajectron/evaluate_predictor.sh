declare -a data_names=("zara2" "zara1" "hotel" "univ" "eth")
for data_name in "${data_names[@]}";
do (CUDA_VISIBLE_DEVICES=1 python evaluate.py --model ../experiments/pedestrians/baseline/${data_name} --checkpoint 100 --data ../experiments/processed/${data_name}_test.pkl)
done;