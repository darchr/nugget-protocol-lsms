from pathlib import Path
import pandas as pd
import json

workdir = Path().cwd()
k_means_selection_data_dir = Path(workdir/f"experiments/info/ir-bb-analysis/comparison/saphir-k-means-selection")
naive_data_df_path = Path(workdir/f"experiments/analysis/papi-naive/naive_data.csv")
nugget_data_df_path = Path(workdir/f"experiments/analysis/nugget-data/nugget_data.csv")
# nugget_data_df_path = Path(workdir/f"experiments/analysis/nugget-data/nugget_data_0_9.csv")

machines = ["summer", "saphir"]
naive_data = pd.read_csv(naive_data_df_path)
nugget_data = pd.read_csv(nugget_data_df_path)

# z_threshold = 1

final_data_df = pd.DataFrame(columns=[
    "benchmark", "machine", "rid", "actual_runtime", "predicted_runtime", 
    "prediction_error", "cluster_weight", "average_runtime", "method"
])


with open(Path(k_means_selection_data_dir/f"kmeans-result.json"), "r") as f:
    cluster_data = json.load(f)
rep_rids = cluster_data["rep_rid"]
cluster_weights = cluster_data["clusters_weights"]

for machine in machines:
    predicted_runtime = 0
    runtime = naive_data[(naive_data["machine"] == machine)]["runtime(ns)"].mean()

    for cid, weight in cluster_weights.items():
        rid = rep_rids[cid]
        rid_data = nugget_data[
            (nugget_data["machine"] == machine) & 
            (nugget_data["rid"] == rid)
        ]

        cluster_runtime = rid_data["runtime(ns)"].mean()

        predicted_runtime += weight * cluster_runtime

        final_data_df = pd.concat([final_data_df, pd.DataFrame({
            "machine": [machine],
            "rid": [rid],
            "actual_runtime": [runtime],
            "predicted_runtime": [-1],
            "prediction_error": [-1],
            "cluster_weight": [weight],
            "average_runtime": [cluster_runtime]
        })
        ], ignore_index=True)
    
    prediction_error = ((predicted_runtime - runtime) / runtime) * 100

    final_data_df = pd.concat([final_data_df, pd.DataFrame({
        "machine": machine,
        "rid": -1,
        "actual_runtime": runtime,
        "predicted_runtime": predicted_runtime,
        "prediction_error": prediction_error,
        "cluster_weight": -1,
        "average_runtime": -1
        },index=[0])], ignore_index=True)
        
final_data_df.to_csv(Path(workdir/f"experiments/analysis/k-means-accuracy/k-means-accuracy.csv"), index=False)
print("Data saved to k-means-accuracy.csv")


