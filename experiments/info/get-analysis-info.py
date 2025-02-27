from pathlib import Path
import pandas as pd
import shutil
import sys

import argparse

# root_path = Path(Path.cwd()/"../../").absolute()
# sys.path.append(root_path.as_posix())
# print(sys.path)

root_path = Path(Path.cwd()).absolute()
sys.path.append(root_path.as_posix())


parser = argparse.ArgumentParser(description="Get analysis info")
parser.add_argument("--csv-file-input", type=str, help="Path to the csv file", required=True)
parser.add_argument("--bb-file-input", type=str, help="Path to the bb file", required=True)
parser.add_argument("--output-analysis-file", type=str, help="Path to the output file", required=True)
parser.add_argument("--output-marker-file", type=str, help="Path to the output marker file", required=True)
parser.add_argument("--input-file-outdir", type=str, help="Path to the output marker file", required=True)
args = parser.parse_args()

csv_file_path = Path(args.csv_file_input)
bb_file_path = Path(args.bb_file_input) 
out_analysis_file = Path(args.output_analysis_file)
out_marker_file = Path(args.output_marker_file)
input_file_outdir = Path(args.input_file_outdir)

from nugget_util.python_processing.analysis_functions import (
    form_dataframe_from_csv,
    form_bb_id_map,
    form_all_markers,
    create_input_for_pass,
    get_total_regions,
    get_static_info
)

# Note that for all parameters used in creating and selecting the nuggets
# the following values were used:
region_length = 100_000_000
grace_perc = 0.98
num_warmup_region = 1
csv_path = csv_file_path
bb_info_path = bb_file_path
# 
# The reason why the parameters are not passed as arguments is because this set
# of parameters is used to create the nuggets used for this particular
# experiment. It is important to fixed them so that the nuggets can be
# recreated.
# 

# if not Path(Path.cwd()/"analysis-output.csv").exists():
#     shutil.copy(csv_path, Path.cwd())
# if not Path(Path.cwd()/"basic-block-info.txt").exists():
#     shutil.copy(bb_info_path, Path.cwd())

df = form_dataframe_from_csv(csv_path)
df.to_csv(out_analysis_file, index=False)

bb_id_map = form_bb_id_map(df)
total_num_regions = get_total_regions(df)

print("finished getting df")

marker_df = form_all_markers(
    df, bb_id_map, num_warmup_region, grace_perc, region_length)

marker_df.to_csv(out_marker_file, index=False)

print("finished getting markers")

static_bb_info = get_static_info(bb_info_path)

input_file_outdir.mkdir(parents=True, exist_ok=True)

for i in range(total_num_regions):
    region_input_info = create_input_for_pass(
        marker_df, static_bb_info, i
    )
    with open(Path(input_file_outdir/f"{i}-marker.txt"), "w") as f:
        for item in region_input_info:
                f.write(f"{item}\n")

print("Done")
