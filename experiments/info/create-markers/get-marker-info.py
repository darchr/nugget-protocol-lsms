from pathlib import Path
import pandas as pd
import shutil
import sys

import argparse

root_path = Path(Path.cwd()).absolute()
sys.path.append(root_path.as_posix())

analysis_csv = Path(root_path/"experiments/info/get-analysis-info/analysis-output.csv")
bb_info_path = Path(root_path/"experiments/info/bb-info-output/basic-block-info.txt")
out_marker_file = Path(root_path/"experiments/info/create-markers/marker-output.csv")
input_file_outdir = Path(root_path/"experiments/info/create-markers/marker-input-files")

k_means_selected_rid_file = Path(root_path/"experiments/info/k-means-selections/selected-regions.txt")

list_of_markers = []
if k_means_selected_rid_file.exists():
    with open(k_means_selected_rid_file, "r") as f:
        for line in f.readlines():
            rid = int(line.strip())
            list_of_markers.append(rid)

for i in range(len(list_of_markers)):
    list_of_markers[i] = int(list_of_markers[i])

from nugget_util.python_processing.analysis_functions import (
    form_bb_id_map,
    form_a_list_markers,
    create_input_for_pass,
    get_total_regions,
    get_static_info
)

region_length = 100_000_000
grace_perc = 0.98
num_warmup_region = 1

def produce_df_and_marker(analysis_df_path, out_marker_file, bb_info_path, input_file_outdir, list_of_markers):
    global region_length, grace_perc, num_warmup_region

    with open(analysis_df_path, "r") as f:
        df = pd.read_csv(f, header=0, dtype={'region': str, 'thread': int})

    bb_id_map = form_bb_id_map(df)
    total_num_regions = get_total_regions(df)

    print("finished getting df")

    target_markers = list_of_markers.copy()

    if input_file_outdir.exists():
        existing_markers = []
        for file in input_file_outdir.iterdir():
            file_name = file.name
            marker_id = int(file_name.split("-")[0])
            existing_markers.append(marker_id)
        for i in range(len(list_of_markers)):
            if list_of_markers[i] in existing_markers:
                target_markers.remove(list_of_markers[i])
    else:
        input_file_outdir.mkdir(parents=True, exist_ok=True)

    print("Target markers: ", target_markers)

    marker_df = form_a_list_markers(
        df, bb_id_map, num_warmup_region, grace_perc, region_length, target_markers)

    marker_df.to_csv(out_marker_file, index=False)

    print("finished getting markers")

    static_bb_info = get_static_info(bb_info_path)

    for i in target_markers:
        region_input_info = create_input_for_pass(
            marker_df, static_bb_info, i
        )
        with open(Path(input_file_outdir/f"{i}-marker.txt"), "w") as f:
            for item in region_input_info:
                    f.write(f"{item}\n")

    print("Done")

if __name__ == "__main__":
    print("Running in main")

    print("Arguments:")
    print("analysis_csv:", analysis_csv)
    print("bb_info_path:", bb_info_path)
    print("out_marker_file:", out_marker_file)
    print("input_file_outdir:", input_file_outdir)
    print("list_of_markers:", list_of_markers)
    produce_df_and_marker(analysis_csv, out_marker_file, bb_info_path, input_file_outdir, list_of_markers)
    
