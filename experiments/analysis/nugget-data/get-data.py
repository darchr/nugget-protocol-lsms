# this script will fetch all the nugget data from experiments folder and save them into a csv file using dataframe

from pathlib import Path
import pandas as pd
import json 

def read_data(dir: Path):
    json_file = None
    for file in dir.iterdir():
        json_file = file
    with open(json_file, "r") as opened_json_file:
        data = json.load(opened_json_file)
    return data["threads"]["0"]["regions"]["0"]

def get_all_runs(dir):
    results = {}
    failed_list = []
    for run in dir.iterdir():
        run_id_name = run.name
        run_id_name = int(str(run_id_name).split("n")[1])
        run_result_path = Path(run/"papi_hl_output")
        if not run_result_path.exists():
            failed_list.append(run_result_path.as_posix())
        else:
            run_result = read_data(run_result_path)
            results[run_id_name] = run_result
    return results, failed_list

def get_all_rid(dir):
    results = {}
    failed_list = []
    for rid in dir.iterdir():
        if not rid.is_dir():
            continue
        rid_name = int(rid.name)
        rid_results, fetch_failed_list = get_all_runs(rid)
        failed_list.extend(fetch_failed_list)
        results[rid_name] = rid_results
    return results, failed_list

def get_all_machine(dir):
    results = {}
    failed_list = []
    for machine in dir.iterdir():
        machine_name = str(machine.name).split("-")[0]
        machine_results, fetch_failed_list = get_all_rid(machine)
        failed_list.extend(fetch_failed_list)
        results[machine_name] = machine_results
    return results, failed_list

failed_list = []

output_dir = Path("/home/studyztp/test_ground/experiments/nugget-micro/nugget-protocol-lsms/experiments/analysis/nugget-data")
data_dir = Path("/home/studyztp/test_ground/experiments/nugget-micro/nugget-protocol-lsms/experiments/papi-nugget-data")
# data_dir = Path("/home/studyztp/test_ground/experiments/nugget-micro/nugget-protocol-NPB/experiments/time-nuggets-experiments_0_9")
results, failed_list = get_all_machine(data_dir)

# convert the results to a dataframe

df = pd.DataFrame(columns=["machine", "rid", "run_id", "runtime(ns)"])

for machine, machine_results in results.items():
    for rid, rid_results in machine_results.items():
        for run_id, run_result in rid_results.items():
            runtime = run_result["real_time_nsec"]
            data = pd.DataFrame([{
                "machine": machine,
                "rid": rid,
                "run_id": run_id,
                "runtime(ns)": runtime
            }])
            df = pd.concat([df, data], ignore_index=True)
# save the dataframe to a csv file
df.to_csv(Path(output_dir/"nugget_data.csv"), index=False)
print("Data saved to nugget_data.csv")

print("Failed list:")
for failed in failed_list:
    print(failed)
print("Total failed files: ", len(failed_list))
# print the total number of files
