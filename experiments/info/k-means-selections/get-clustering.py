from pathlib import Path
import pandas as pd
import argparse
import json
import sys

root_path = Path(Path.cwd()).absolute()
sys.path.append(root_path.as_posix())

bb_info_path = Path(root_path/"experiments/info/bb-info-output/basic-block-info.txt")
df_path = Path(root_path/"experiments/info/get-analysis-info/analysis-output.csv")
num_ideal_nuggets = 50
num_projection = 100
output_dir = Path(root_path/"experiments/info/k-means-selections")

from nugget_util.python_processing.analysis_functions import (
    get_all_bbv,
    form_bb_id_map,
    get_static_info,
    k_means_select_regions
)

def generate_k_means(nugget_info_path, analysis_df_path, num_ideal_nuggets, output_dir):
    global num_projection
    with open(analysis_df_path, "r") as f:
        df = pd.read_csv(f, header=0, dtype={'region': str, 'thread': int})

    bb_id_map = form_bb_id_map(df)

    all_bbv = get_all_bbv(df, bb_id_map)

    for index, row in enumerate(all_bbv):
        if sum(row) == 0:
            print(f"row {index} has all zeros")

    static_info = get_static_info(nugget_info_path)

    print(f"shape of all_bbv: {len(all_bbv)} {len(all_bbv[0])}")

    while len(all_bbv) <= num_ideal_nuggets * 4:
        num_ideal_nuggets /= 2
        num_ideal_nuggets = int(num_ideal_nuggets)

    if len(all_bbv[0]) <= num_projection:
        num_projection = len(all_bbv[0])
        num_projection = int(num_projection)

    num_projection = min(num_projection, len(all_bbv))

    kmeans_result = k_means_select_regions(
        num_ideal_nuggets,
        all_bbv,
        bb_id_map,
        static_info,
        num_projection
    )

    with open(Path(output_dir/"kmeans-result.json"), "w") as f:
        json.dump(kmeans_result, f, indent=4)

    rep_rid = kmeans_result["rep_rid"]

    with open(Path(output_dir/"selected-regions.txt"), "w") as f:
        for val in rep_rid.values():
            f.write(f"{val}\n")

    print("finished selecting regions")


generate_k_means(
    bb_info_path,
    df_path,
    num_ideal_nuggets,
    output_dir
)

print("Done")

