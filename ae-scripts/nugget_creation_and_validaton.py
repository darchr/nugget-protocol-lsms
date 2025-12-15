#!/usr/bin/env python3
"""Build and run nugget/naive binaries for selected benchmarks and aggregate measurements."""

import argparse
import csv
import json
import os
import shutil
import time
from collections import defaultdict
from pathlib import Path


def run_command(cmd, cwd: Path, env=None):
	import subprocess

	print(f"Running: {' '.join(cmd)} (cwd={cwd})")
	cwd.mkdir(parents=True, exist_ok=True)
	subprocess.run(cmd, cwd=cwd, env=env, check=True)


def run_subprocess(cmd, cwd: Path, env=None, stdout_path: Path | None = None, stderr_path: Path | None = None):
	import subprocess

	print(f"Running: {' '.join(cmd)} (cwd={cwd})")
	cwd.mkdir(parents=True, exist_ok=True)
	with (stdout_path.open("wb") if stdout_path else open(os.devnull, "wb")) as out, (
		stderr_path.open("wb") if stderr_path else open(os.devnull, "wb")
	) as err:
		subprocess.run(cmd, cwd=cwd, env=env, check=True, stdout=out, stderr=err)


def parse_benchmarks(text: str) -> list[str]:
	parts = [p.strip() for p in text.replace(";", " ").replace(",", " ").split() if p.strip()]
	return parts


def build_all(lsms_root: Path, experiment_name: str, grace: float, architecture: str, selection_architecture: str):
	build_dir = lsms_root / "ae-cbuild"
	build_dir.mkdir(parents=True, exist_ok=True)

	k_means_sample_file = lsms_root / "ae-experiments" / "sample-selection" / "k-means" / f"{experiment_name}" / selection_architecture / "selected-regions.txt"
	random_sample_file = lsms_root / "ae-experiments" / "sample-selection" / "random" / f"{experiment_name}" / selection_architecture / "selected-regions.txt"
	markers_root = lsms_root / "ae-experiments" / "create-markers" / f"{grace}" / f"{experiment_name}" / selection_architecture / "input-files"
	bb_info_file = lsms_root / "ae-experiments" / "analysis" / f"{experiment_name}" / architecture / "basic-block-info.txt"
	source_bc_dir = lsms_root / "ae-cbuild" / "llvm-bc"
	ae_cmake = lsms_root / "ae-cmake"

	def cmake_env(extra: dict) -> dict:
		base = os.environ.copy()
		base.update(extra)
		return base

	# k-means nugget bc
	run_command(
		["cmake", f"-DCMAKE_TOOLCHAIN_FILE={ae_cmake}/lsms-toolchain-generic-cpu.cmake", f"{lsms_root}/lsms"],
		cwd=build_dir,
		env=cmake_env(
			{
				"NUGGET_PROCESS_TYPE": "lsms-nugget-bc",
				"NUGGET_CONFIG_FILE": str(
					lsms_root / "ae-cmake"/ "papi-nugget" / "cmake" / "papi-nugget-bc.cmake"
				),
				"ALL_NUGGET_RIDS_FILE": str(k_means_sample_file),
				"MARKER_DIR": str(markers_root),
				"BB_INFO_INPUT_PATH": str(bb_info_file),
				"SOURCE_BC_FILE_PATH": str(source_bc_dir),
			}
		),
	)
	run_command(["cmake", "--build", ".", "--target=papi_nugget_bc"], cwd=build_dir)

	# nugget exe
	run_command(
		["cmake", f"-DCMAKE_TOOLCHAIN_FILE={ae_cmake}/lsms-toolchain-generic-cpu.cmake", f"{lsms_root}/lsms"],
		cwd=build_dir,
		env=cmake_env(
			{
				"NUGGET_PROCESS_TYPE": "lsms-nugget-exe",
				"NUGGET_CONFIG_FILE": str(
					lsms_root / "ae-cmake"/ "papi-nugget" / "cmake" / "papi-nugget-exe.cmake"
				),
				"ALL_NUGGET_RIDS_FILE": str(k_means_sample_file),
			}
		),
	)
	run_command(["cmake", "--build", ".", f"--target=papi_nugget_{architecture}_exe"], cwd=build_dir)

    # random nugget bc
	run_command(
		["cmake", f"-DCMAKE_TOOLCHAIN_FILE={ae_cmake}/lsms-toolchain-generic-cpu.cmake", f"{lsms_root}/lsms"],
		cwd=build_dir,
		env=cmake_env(
			{
				"NUGGET_PROCESS_TYPE": "lsms-nugget-bc",
				"NUGGET_CONFIG_FILE": str(
					lsms_root / "ae-cmake"/ "papi-nugget" / "cmake" / "papi-nugget-bc.cmake"
				),
				"ALL_NUGGET_RIDS_FILE": str(random_sample_file),
				"MARKER_DIR": str(markers_root),
				"BB_INFO_INPUT_PATH": str(bb_info_file),
				"SOURCE_BC_FILE_PATH": str(source_bc_dir),
			}
		),
	)
	run_command(["cmake", "--build", ".", "--target=papi_nugget_bc"], cwd=build_dir)

	# nugget exe
	run_command(
		["cmake", f"-DCMAKE_TOOLCHAIN_FILE={ae_cmake}/lsms-toolchain-generic-cpu.cmake", f"{lsms_root}/lsms"],
		cwd=build_dir,
		env=cmake_env(
			{
				"NUGGET_PROCESS_TYPE": "lsms-nugget-exe",
				"NUGGET_CONFIG_FILE": str(
					lsms_root / "ae-cmake"/ "papi-nugget" / "cmake" / "papi-nugget-exe.cmake"
				),
				"ALL_NUGGET_RIDS_FILE": str(random_sample_file),
			}
		),
	)
	run_command(["cmake", "--build", ".", f"--target=papi_nugget_{architecture}_exe"], cwd=build_dir)
	# naive bc
	run_command(
		["cmake", f"-DCMAKE_TOOLCHAIN_FILE={ae_cmake}/lsms-toolchain-generic-cpu.cmake", f"{lsms_root}/lsms"],
		cwd=build_dir,
		env=cmake_env(
			{
				"NUGGET_PROCESS_TYPE": "lsms-naive-bc",
				"NUGGET_CONFIG_FILE": str(
					lsms_root / "ae-cmake"/ "papi-naive" / "cmake" / "papi-naive-bc.cmake"
				),
				"SOURCE_BC_FILE_PATH": Path(build_dir/"llvm-bc").as_posix(),
			}
		),
	)
	run_command(["cmake", "--build", ".", "--target=lsms_papi_naive_bc"], cwd=build_dir)

	# naive exe
	run_command(
		["cmake", f"-DCMAKE_TOOLCHAIN_FILE={ae_cmake}/lsms-toolchain-generic-cpu.cmake", f"{lsms_root}/lsms"],
		cwd=build_dir,
		env=cmake_env(
			{
				"NUGGET_PROCESS_TYPE": "lsms-naive-exe",
				"NUGGET_CONFIG_FILE": str(
					lsms_root / "ae-cmake"/ "papi-naive" / "cmake" / "papi-naive-exe.cmake"
				),
				"BC_FILE_PATH": Path(build_dir/"llvm-bc/lsms_papi_naive_bc/lsms_papi_naive_bc.bc").as_posix(),
			}
		),
	)
	run_command(["cmake", "--build", ".", f"--target=lsms_papi_naive_{architecture}_exe"], cwd=build_dir)

def measure_binary(bin_path: Path, workdir: Path, perf_combos: list[list[str]], input_directory: Path, input_command: str) -> dict[str, float]:
	env = os.environ.copy()
	env["OMP_NUM_THREADS"] = "1"

	event_values: dict[str, list[float]] = defaultdict(list)

	for index, combo in enumerate(perf_combos):
		combo_workdir = workdir / f"combo_{index}"
		combo_workdir.mkdir(parents=True, exist_ok=True)
		copied_paths = []
		for item in input_directory.iterdir():
			dest = combo_workdir / item.name
			if item.is_dir():
				shutil.copytree(item, dest, dirs_exist_ok=True)
			else:
				shutil.copy2(item, dest)
			copied_paths.append(dest)
		env["PAPI_EVENTS"] = ",".join(combo)
		stdout_path = combo_workdir / "stdout.log"
		stderr_path = combo_workdir / "stderr.log"
		start = time.perf_counter()
		run_subprocess([str(bin_path), input_command], cwd=combo_workdir, env=env, stdout_path=stdout_path, stderr_path=stderr_path)
		duration = time.perf_counter() - start
		(combo_workdir / "execution_time.txt").write_text(f"{duration:.6f}\n")
		if (not Path(combo_workdir / "papi_hl_output").exists()):
			raise RuntimeError(f"Expected papi_hl_output folder in {combo_workdir / 'papi_hl_output'} after running {bin_path}")
		# get the autogenerated papi json file
		papi_json_files = list((combo_workdir / "papi_hl_output").glob("*.json"))
		if not papi_json_files:
			raise RuntimeError(f"Expected papi json output file in {combo_workdir / 'papi_hl_output'} after running {bin_path}")
		papi_json_file = papi_json_files[0]
		with papi_json_file.open("r") as f:
			data = json.load(f)
		data = data["threads"]["0"]["regions"]["0"]
		for event, value in data.items():
			if event not in {"name", "parent_region_id", "cycles"}:
				event_values[event].append(float(value))

		for path in reversed(copied_paths):
			if path.is_dir():
				shutil.rmtree(path, ignore_errors=True)
			else:
				path.unlink(missing_ok=True)

	# average per event across combos
	averaged = {event: (sum(vals) / len(vals)) for event, vals in event_values.items() if vals}
	return averaged

def find_nugget_binaries(llvm_exec: Path, architecture: str):
	nuggets = []
	for p in llvm_exec.glob(f"papi_nugget_{architecture}_exe_*"):
		parts = p.name.split("_")
		rid = parts[4]
		exe_path = p / p.name if p.is_dir() else p
		nuggets.append((rid, exe_path))
	nuggets.sort(key=lambda x: int(x[0]))
	return nuggets

def load_kmeans_clusters(kmeans_root: Path) -> dict[str, dict[str, float]]:
	"""Return per-benchmark cluster info: {bench: {cluster_id: {rid, weight}}}."""
	kmeans_path = kmeans_root / "kmeans-result.json"
	if not kmeans_path.is_file():
		raise FileNotFoundError(f"Unable to find kmeans-result.json at {kmeans_path}")
	with kmeans_path.open("r") as f:
		data = json.load(f)
	rep = data.get("rep_rid", {})
	weights = data.get("clusters_weights", {})
	clusters: dict[str, dict[str, float]] = {}
	for cluster, rid in rep.items():
		cid = str(cluster)
		clusters[cid] = {"rid": str(rid), "weight": float(weights.get(cid, 0.0))}
	print(clusters)
	return clusters


def load_random_regions(random_root: Path) -> list[str]:
	txt_path = random_root / "selected-regions.txt"
	if not txt_path.is_file():
		RuntimeError(f"Unable to find selected-regions.txt for random at {txt_path}")
	random_rids = []
	with txt_path.open("r") as f:
		for line in f:
			rid = line.strip()
			if rid:
				random_rids.append(rid)
	return list(set(random_rids))

def load_perf_combo(path):
    combos = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or not (line.startswith("[") and line.endswith("]")):
                continue
            items = [token.strip() for token in line[1:-1].split(",")]
            if items:
                combos.append(items)
    return combos

def main():
	parser = argparse.ArgumentParser(description="Create and validate nuggets/naive binaries and measure runtime.")
	parser.add_argument("--project_dir", "-d", required=True, help="Path to project root containing nugget-protocol-NPB")
	parser.add_argument("--grace-perc", type=float, default=0.98, help="Grace percentage used in markers. (default: 0.98)")
	parser.add_argument("--input-command", "-c", default="i_lsms", help="Input command to run LSMS. (default: 'i_lsms')")
	parser.add_argument("--input-directory", "-r", default="ae-scripts/input", help="Relative path to input directory from project root. (default: 'ae-scripts/input')")
	parser.add_argument("--papi-combo-file-path", "-p", type=str, required=True, help="Path to papi event combination coverage file.")
	parser.add_argument("--skip-build", action="store_true", help="Skip the build step if set.")
	parser.add_argument("--architecture", "-a", type=str, default=os.uname().machine, help="Target architecture for the build (default: detected architecture)")
	parser.add_argument("--selection-architecture", "-s", type=str, default=os.uname().machine, help="Architecture string used in binary names for sample selection. (default: detected architecture)")
	args = parser.parse_args()

	project_dir = Path(args.project_dir).expanduser().resolve()
	lsms_root = project_dir / "nugget-protocol-lsms"
	if not lsms_root.is_dir():
		raise FileNotFoundError(f"Expected nugget-protocol-lsms under {project_dir}")
	input_command = args.input_command
	input_directory = Path(lsms_root / args.input_directory)
	if not input_directory.is_dir():
		raise FileNotFoundError(f"Expected input directory at {input_directory}")
	papi_combo_file = Path(args.papi_combo_file_path)
	if not papi_combo_file.is_file():
		raise FileNotFoundError(f"Expected papi combo file at {papi_combo_file}")
	perf_combos = load_perf_combo(papi_combo_file)

	architecture = args.architecture
	print(f"Architecture: {architecture}")
	selection_architecture = args.selection_architecture
	print(f"Selection Architecture: {selection_architecture}")
	
	grace = args.grace_perc
	if not args.skip_build:
		build_all(lsms_root, input_command, grace, architecture, selection_architecture)

	llvm_exec = lsms_root / "ae-cbuild" / "llvm-exec"
	if not llvm_exec.is_dir():
		raise FileNotFoundError(f"Expected llvm-exec at {llvm_exec}")

	nugget_out_root = lsms_root / "ae-experiments" / "nugget-measurement" / input_command / architecture 
	naive_out_root = lsms_root / "ae-experiments" / "naive-measurement" / input_command / architecture
	nugget_out_root.mkdir(parents=True, exist_ok=True)
	naive_out_root.mkdir(parents=True, exist_ok=True)

	kmeans_root = lsms_root / "ae-experiments" / "sample-selection" / "k-means" / input_command / selection_architecture
	random_root = lsms_root / "ae-experiments" / "sample-selection" / "random" / input_command / selection_architecture
	bench_clusters = load_kmeans_clusters(kmeans_root)
	random_rids = load_random_regions(random_root)
	print(random_rids)

	measurements = []
	# Run naive binaries first to provide baselines
	naive_stats = measure_binary(Path(llvm_exec/ f"lsms_papi_naive_{architecture}_exe"/ f"lsms_papi_naive_{architecture}_exe"), naive_out_root, perf_combos, input_directory, input_command)
	entry = {
		"type": "naive",
		"region_id": "",
		"cluster_id": "",
		"runtime_nseconds": naive_stats["real_time_nsec"],
		"baseline_naive_nseconds": naive_stats["real_time_nsec"],
	}
	naive_time = naive_stats["real_time_nsec"]
	entry.update(naive_stats)
	measurements.append(entry)

	# Run nugget binaries and collect runtimes per rid
	runtime_by_rid: dict[str, float] = {}
	for rid, bin_path in find_nugget_binaries(llvm_exec, architecture):
		out_dir = nugget_out_root / rid
		rid_stats = measure_binary(bin_path, out_dir, perf_combos, input_directory, input_command)
		runtime_by_rid[rid] = rid_stats["real_time_nsec"]
		baseline = naive_time
		cluster_id = ""
		for cid, meta in bench_clusters.items():
			if meta.get("rid") == rid:
				cluster_id = cid
				break
		entry = {
			"type": "nugget",
			"region_id": rid,
			"cluster_id": cluster_id,
			"runtime_nseconds": rid_stats["real_time_nsec"],
			"baseline_naive_nseconds": baseline if baseline is not None else ""
		}
		entry.update(rid_stats)
		measurements.append(entry)

	# Compute program-level predicted runtime using cluster weights * measured rep runtimes
	program_pred = 0.0
	total_regions = 0
	required_rids = [meta.get("rid") for meta in bench_clusters.values() if meta.get("rid") is not None]
	if not required_rids:
		raise RuntimeError("No representative regions found in k-means clusters to form predictions.")
	if any(runtime_by_rid.get(rid) is None for rid in required_rids):
		# Cannot form a prediction until every representative nugget is measured
		raise RuntimeError("Not all representative regions have measurements; cannot form k-means prediction.")
	pred_total = 0.0
	total_regions = 0.0
	for cid, meta in bench_clusters.items():
		rid = meta.get("rid")
		if rid is None:
			continue
		weight = meta.get("weight", 0.0)
		total_regions += weight
		runtime = runtime_by_rid.get(rid)
		pred_total += weight * runtime
	program_pred = pred_total if pred_total > 0 else None
	random_pred = 0.0
	if not random_rids:
		raise RuntimeError("No random regions found to form predictions.")
	runtimes = []
	for rid in random_rids:
		runtime = runtime_by_rid.get(rid)
		if runtime is None:
			raise RuntimeError(f"Missing measurement for random region {rid}; cannot form random prediction.")
		runtimes.append(runtime)
	if len(runtimes) != len(random_rids):
		raise RuntimeError("Not all random regions have measurements; cannot form random prediction.")
	mean_runtime = sum(runtimes) / len(runtimes)
	scale = total_regions
	if scale is None or scale <= 0:
		raise RuntimeError("Invalid scale for random prediction; cannot form random prediction.")
	random_pred = mean_runtime * scale
	# Write CSV
	csv_path = lsms_root / "ae-experiments" / "nugget-measurement" / input_command / architecture / "measurements.csv"
	csv_path.parent.mkdir(parents=True, exist_ok=True)
	fieldnames = measurements[0].keys()
	with csv_path.open("w", newline="") as f:
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		for row in measurements:
			row_out = dict(row)
			writer.writerow(row_out)

	# Write prediction error CSV for k-means and random methods
	pred_csv_path = lsms_root / "ae-experiments" / "nugget-measurement" / input_command / architecture / "prediction-error.csv"
	pred_csv_path.parent.mkdir(parents=True, exist_ok=True)
	pred_fieldnames = [
		"sample_selection_method",
		"predicted_time_nseconds",
		"baseline_time_nseconds",
		"prediction_error(%)",
	]
	with pred_csv_path.open("w", newline="") as f:
		writer = csv.DictWriter(f, fieldnames=pred_fieldnames)
		writer.writeheader()
		baseline = naive_time
		# k-means prediction
		km_pred = program_pred
		if km_pred is not None and baseline is not None and baseline > 0:
			km_err = ((km_pred - baseline) / baseline) * 100
			writer.writerow(
				{
					"sample_selection_method": "k-means",
					"predicted_time_nseconds": km_pred,
					"baseline_time_nseconds": baseline,
					"prediction_error(%)": km_err,
				}
			)
		# random prediction
		r_pred = random_pred
		if r_pred is not None and baseline is not None and baseline > 0:
			r_err = ((r_pred - baseline) / baseline) * 100
			writer.writerow(
				{
					"sample_selection_method": "random",
					"predicted_time_nseconds": r_pred,
					"baseline_time_nseconds": baseline,
					"prediction_error(%)": r_err,
				}
			)

	print(f"Wrote measurements to {csv_path}")
	print(f"Wrote prediction errors to {pred_csv_path}")


if __name__ == "__main__":
	main()
