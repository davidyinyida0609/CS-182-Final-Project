from dis import dis
import imp
import os
from argument_parser import args
import json
import pandas as pd
model_dir = args.log_dir
flag = model_dir != 'baseline'
modes = set(['best_of_20'])
columns = ['name', "meanADE", "meanFDE"]
data_names = set(['hotel', 'univ', 'zara1', 'zara2', 'eth'])
metrics = {mode: {name: list() for name in columns} for mode in modes}
for dirpath, dirnames, filenames in os.walk(model_dir):
    for filename in filenames:
        if filename[-4:] != "json":
            continue
        mode = filename.split(os.sep)[-1][:-5]
        if mode not in modes:
            continue
        file_path = os.path.join(dirpath, filename)
        with open(file_path, 'r') as f:
            metric = json.load(f)
        name = dirpath.split(os.sep)[-1]
        metric['name'] = name
        for k in columns:
            metrics[mode][k].append(metric[k])
for mode in metrics:
    df = pd.DataFrame(metrics[mode])
    from IPython.display import display
    print(f"The result of the model under the folder {model_dir} is shown as follows:")
    display(df)
    df.to_csv(os.path.join(model_dir, f'{mode}.csv'), index=False)

    
    




