from dis import dis
import imp
import os
from argument_parser import args
import json
import pandas as pd
model_dir = args.log_dir
flag = model_dir != 'baseline'
columns = ['name', "minADE", "minFDE"]
data_names = set(['hotel', 'univ', 'zara1', 'zara2', 'eth'])
keys = set(["20"])
metrics = {k: {name: list() for name in columns} for k in keys}
for dirpath, dirnames, filenames in os.walk(model_dir):
    for filename in filenames:
        if filename[-4:] != "json":
            continue
        info = filename.split('_')
        if len(info) != 4:
            continue
        key = info[2]
        assert key in keys
        file_path = os.path.join(dirpath, filename)
        with open(file_path, 'r') as f:
            metric = json.load(f)
        name = dirpath.split('/')[-1]
        metric['name'] = name
        for k in columns:
            metrics[key][k].append(metric[k])
for key in metrics:
    df = pd.DataFrame(metrics[key])
    from IPython.display import display
    display(df)
    df.to_csv(os.path.join(model_dir, f'best_of_{key}.csv'), index=False)

    
    




