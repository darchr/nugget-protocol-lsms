from pathlib import Path
import pandas as pd
import argparse
import json
import sys
import random

random.seed(627)

root_path = Path(Path.cwd()).absolute()
sys.path.append(root_path.as_posix())

parse = argparse.ArgumentParser()
parse.add_argument("--num_ideal_nuggets", type=int, default=50)
parse.add_argument("--nugget_info_path", type=str, required=True)
parse.add_argument("--analysis_df_path", type=str, required=True)
parse.add_argument("--output_dir", type=str, required=True)
args = parse.parse_args()

from nugget_util.python_processing.analysis_functions import (
    get_all_bbv,
    form_bb_id_map,
    get_static_info,
    k_means_select_regions
)

num_ideal_nuggets = args.num_ideal_nuggets
nugget_info_path = Path(args.nugget_info_path)
analysis_df_path = Path(args.analysis_df_path)
output_dir = Path(args.output_dir)

output_dir.mkdir(parents=True, exist_ok=True)

with open(analysis_df_path, "r") as f:
    df = pd.read_csv(f, header=0, dtype={'region': str, 'thread': int})

bb_id_map = form_bb_id_map(df)

all_bbv = get_all_bbv(df, bb_id_map)

random_selected_samples = random.sample(range(0, len(all_bbv)), num_ideal_nuggets)

with open(Path(output_dir/"selected-regions.txt"), "w") as f:
    for sample in random_selected_samples:
        f.write(f"{sample}\n")

print("Done")
