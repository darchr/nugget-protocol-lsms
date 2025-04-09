from pathlib import Path
import pandas as pd
import json
import random

random_seed = 627
random.seed(random_seed)

workdir = Path().cwd()
k_means_selection_data_dir = Path(workdir/f"experiments/info/k-means-selections")
naive_data_df_path = Path(workdir/f"experiments/analysis/papi-naive/naive_data.csv")
nugget_data_df_path = Path(workdir/f"experiments/analysis/nugget-data/nugget_data.csv")
random_selection_data_dir = Path(workdir/f"experiments/info/random-selections")


size = "C"
benchmarks = ["bt", "cg", "ep", "ft", "is", "lu", "mg", "sp"]
# benchmarks = ["sp"]
machines = ["summer", "saphir"]
naive_data = pd.read_csv(naive_data_df_path)
nugget_data = pd.read_csv(nugget_data_df_path)

# z_threshold = 1

final_data_df = pd.DataFrame(columns=[
    "benchmark", "machine", "rid", "actual_runtime", "predicted_runtime", 
    "prediction_error", "total_regions", "total_selected_regions", "average_runtime"
])


for i in range(len(benchmarks)):
    benchmarks[i] = f"{benchmarks[i]}_{size}"

for bench in benchmarks:
    with open(Path(k_means_selection_data_dir/f"{bench}/kmeans-result.json"), "r") as f:
        cluster_data = json.load(f)
    rep_rids = cluster_data["rep_rid"]
    num_samples = len(rep_rids)

    # all_rids = []
    # with open(Path(random_selection_data_dir/f"{bench}/selected-regions.txt"), "r") as f:
    #     for line in f.readlines():
    #         all_rids.append(int(line.strip()))

    # now we need to randomly select the same number of samples that k-means selected to 
    # form a random sample set to prove that we can't reach to the same accuracy without
    # the targeted selection with less samples that is not targeted

    unique_rids = nugget_data[(nugget_data["benchmark"] == bench)]["rid"].unique()
    unique_rids_list = list(unique_rids)

    selected_regions = random.sample(unique_rids_list, num_samples)

    for i in range(num_samples):
        selected_regions[i] = int(selected_regions[i])

    with open(Path(info_dir/f"{bench}/total_regions.txt")) as f:
        total_regions = int(f.readline().strip())

    for machine in machines:
        predicted_runtime = 0
        runtime = naive_data[(naive_data["machine"] == machine) & (naive_data["benchmark"] == bench)]["runtime(ns)"].mean()

        for rid in selected_regions:
            rid_data = nugget_data[
                (nugget_data["machine"] == machine) & 
                (nugget_data["benchmark"] == bench) & 
                (nugget_data["rid"] == rid)
            ]

            rid_runtime = rid_data["runtime(ns)"].mean()

            predicted_runtime += rid_runtime

            final_data_df = pd.concat([final_data_df, pd.DataFrame({
                "benchmark": [bench],
                "machine": [machine],
                "rid": [rid],
                "actual_runtime": [runtime],
                "predicted_runtime": [-1],
                "prediction_error": [-1],
                "total_regions": [total_regions],
                "total_selected_regions": [num_samples],
                "average_runtime": [rid_runtime]
            })
            ], ignore_index=True)

        predicted_runtime = (predicted_runtime / num_samples) * total_regions
        
        prediction_error = ((predicted_runtime - runtime) / runtime) * 100
        print(f"Benchmark: {bench}, Machine: {machine}, Actual Runtime: {runtime}, Predicted Runtime: {predicted_runtime}, Prediction Error: {prediction_error}%")

        final_data_df = pd.concat([final_data_df, pd.DataFrame({
            "benchmark": bench,
            "machine": machine,
            "rid": -1,
            "actual_runtime": runtime,
            "predicted_runtime": predicted_runtime,
            "prediction_error": prediction_error,
            "total_regions": total_regions,
            "total_selected_regions": num_samples,
            "average_runtime": -1
        },index=[0])], ignore_index=True)
        
final_data_df.to_csv(Path(workdir/f"experiments/analysis/matching-average-accuracy/smaller-num-random-selections-accuracy.csv"), index=False)
print("Data saved to smaller-num-random-selections-accuracy.csv")


