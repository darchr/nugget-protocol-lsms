from pathlib import Path
import sys

root_path = Path(Path.cwd()).absolute()
sys.path.append(root_path.as_posix())

from nugget_util.python_processing.analysis_functions import (
    form_dataframe_from_csv,
)

output_dir = Path(root_path/"experiments/info/get-analysis-info")
analysis_csv_file_path = Path(f"{root_path}/experiments/ir-bb-analysis/run-0/analysis-output.csv")

region_length = 100_000_000

df = form_dataframe_from_csv(analysis_csv_file_path)
df.to_csv(Path(output_dir/"analysis-output.csv"), index=False)

print("finished getting df")

print("Done")
