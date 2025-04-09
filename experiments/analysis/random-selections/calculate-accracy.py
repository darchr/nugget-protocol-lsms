from pathlib import Path
import pandas as pd
import json

workdir = Path().cwd()
random_selection_data_dir = Path(workdir/f"experiments/info/ir-bb-analysis/comparison/random-selection")
naive_data_df_path = Path(workdir/f"experiments/analysis/papi-naive/naive_data.csv")
nugget_data_df_path = Path(workdir/f"experiments/analysis/nugget-data/nugget_data.csv")


machines = ["summer", "saphir"]
naive_data = pd.read_csv(naive_data_df_path)
nugget_data = pd.read_csv(nugget_data_df_path)

# z_threshold = 1

final_data_df = pd.DataFrame(columns=[
    "machine", "rid", "actual_runtime", "predicted_runtime", 
    "prediction_error", "total_regions", "total_selected_regions", "average_runtime"
])


all_rids = []
with open(Path(random_selection_data_dir/f"selected-regions.txt"), "r") as f:
    for line in f.readlines():
        all_rids.append(int(line.strip()))

total_selected_regions = len(all_rids)

with open(Path(random_selection_data_dir/f"total-regions.txt")) as f:
    total_regions = int(f.readline().strip())
    
for machine in machines:
    predicted_runtime = 0
    runtime = naive_data[(naive_data["machine"] == machine)]["runtime(ns)"].mean()

    for rid in all_rids:
        rid_data = nugget_data[
            (nugget_data["machine"] == machine) & 
            (nugget_data["rid"] == rid)
        ]

        rid_runtime = rid_data["runtime(ns)"].mean()

        predicted_runtime += rid_runtime

        final_data_df = pd.concat([final_data_df, pd.DataFrame({
            "machine": [machine],
            "rid": [rid],
            "actual_runtime": [runtime],
            "predicted_runtime": [-1],
            "prediction_error": [-1],
            "total_regions": [total_regions],
            "total_selected_regions": [total_selected_regions],
            "average_runtime": [rid_runtime]
        })
        ], ignore_index=True)

    predicted_runtime = (predicted_runtime / total_selected_regions) * total_regions
    
    prediction_error = ((predicted_runtime - runtime) / runtime) * 100

    print(f"Machine: {machine}, Actual Runtime: {runtime}, Predicted Runtime: {predicted_runtime}, Prediction Error: {prediction_error}%")
    final_data_df = pd.concat([final_data_df, pd.DataFrame({
        "machine": machine,
        "rid": -1,
        "actual_runtime": runtime,
        "predicted_runtime": predicted_runtime,
        "prediction_error": prediction_error,
        "total_regions": total_regions,
        "total_selected_regions": total_selected_regions,
        "average_runtime": -1
    },index=[0])], ignore_index=True)
        
final_data_df.to_csv(Path(workdir/"experiments/analysis/random-selections/random-selections-accuracy.csv"), index=False)

print("Data saved to random-selections-accuracy.csv")


