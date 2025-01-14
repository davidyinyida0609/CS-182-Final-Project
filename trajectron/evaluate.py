import sys
import os
import dill
import json
import argparse
import torch
import numpy as np
import pandas as pd

sys.path.append("../../trajectron")
from tqdm import tqdm
from model.model_registrar import ModelRegistrar
from model.trajectron import Trajectron
import evaluation

seed = 0
np.random.seed(seed)
torch.manual_seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

parser = argparse.ArgumentParser()
parser.add_argument("--model", help="model full path", type=str)
parser.add_argument("--checkpoint", help="model checkpoint to evaluate", type=str)
parser.add_argument("--data", help="full path to data file", type=str)
args = parser.parse_args()


def load_model(model_dir, env, ts=100):
    model_registrar = ModelRegistrar(model_dir, 'cpu')
    model_registrar.load_models(ts)
    with open(os.path.join(model_dir, 'config.json'), 'r') as config_json:
        hyperparams = json.load(config_json)

    trajectron = Trajectron(model_registrar, hyperparams, None, 'cpu')

    trajectron.set_environment(env)
    trajectron.set_annealing_params()
    return trajectron, hyperparams


if __name__ == "__main__":
    with open(args.data, 'rb') as f:
        env = dill.load(f, encoding='latin1')

    eval_stg, hyperparams = load_model(args.model, env, ts=args.checkpoint)

    if 'override_attention_radius' in hyperparams:
            for attention_radius_override in hyperparams['override_attention_radius']:
                node_type1, node_type2, attention_radius = attention_radius_override.split(' ')
                env.attention_radius[(node_type1, node_type2)] = float(attention_radius)

    scenes = env.scenes

    print("-- Preparing Node Graph")
    for scene in tqdm(scenes):
        scene.calculate_scene_graph(env.attention_radius,
                                    hyperparams['edge_addition_filter'],
                                    hyperparams['edge_removal_filter'])

    ph = hyperparams['prediction_horizon']
    max_hl = hyperparams['maximum_history_length']
    with torch.no_grad():
        print(f"-- Evaluating best of 20")
        ############### BEST OF 20 ###############
        eval_ade_batch_errors = np.array([])
        eval_fde_batch_errors = np.array([])
        
        for i, scene in enumerate(scenes):
            print(f"---- Evaluating Scene {i + 1}/{len(scenes)}")
            for t in tqdm(range(0, scene.timesteps, 10)):
                timesteps = np.arange(t, t + 10)
                predictions = eval_stg.predict(scene,
                                            timesteps,
                                            ph,
                                            num_samples=20,
                                            min_history_timesteps=7,
                                            min_future_timesteps=12,
                                            z_mode=False,
                                            gmm_mode=False,
                                            full_dist=False)

                if not predictions:
                    continue

                batch_error_dict = evaluation.compute_batch_statistics(predictions,
                                                                    scene.dt,
                                                                    max_hl=max_hl,
                                                                    ph=ph,
                                                                    node_type_enum=env.NodeType,
                                                                    map=None,
                                                                    best_of=True,
                                                                    prune_ph_to_future=True)
                for k in batch_error_dict:
                    eval_ade_batch_errors = np.hstack((eval_ade_batch_errors, batch_error_dict[k]['ade']))
                    eval_fde_batch_errors = np.hstack((eval_fde_batch_errors, batch_error_dict[k]['fde']))
        meanADE = np.mean(eval_ade_batch_errors)
        meanFDE = np.mean(eval_fde_batch_errors)
        with open(os.path.join(args.model, "best_of_20.json"), "w") as a:
            json.dump({"meanADE": meanADE, "meanFDE": meanFDE}, a)