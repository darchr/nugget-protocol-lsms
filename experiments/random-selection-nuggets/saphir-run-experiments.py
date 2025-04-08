import argparse
import multiprocessing
import subprocess
import configparser
from pathlib import Path
import os
import shutil

def run_this(run_ball):
    global core_queue_global, failed_list_global

    core = core_queue_global.get()
    print("Running on core: ", core)
    command = run_ball["command"]
    run_dir = run_ball["run_dir"]
    run_log_file = run_ball["run.log"]
    run_err_file = run_ball["run.err"]
    input_dir = run_ball["input_dir"]

    cpuset_name = "measurement2/"  # Moved inside to ensure it's accessible
    # cset proc --exec --set=measurement/core_32 --
    command = ["cset", "proc","--exec", f"--set={cpuset_name}{str(core)}", "--" ] + command

    run_dir.mkdir(parents=True, exist_ok=False)

    input_dir = Path(input_dir)
    
    input_files = []
    for file_path in input_dir.iterdir():
        if file_path.is_file():
            shutil.copy(file_path, run_dir / file_path.name)
            input_files.append(Path(run_dir / file_path.name))

    print(f"running {command} in {run_dir} with core {core}")

    env = os.environ.copy()  # Ensure environment variables are available
    with open(run_dir / run_log_file, "w") as log_file, open(run_dir / run_err_file, "w") as err_file:
        result = subprocess.run(command, cwd=run_dir, stdout=log_file, stderr=err_file, env=env)

    if result.returncode != 0:
        print("Error running command: ", command)
        print("Error at core: ", core)
        failed_list_global.append([core, command])
    else:
        print(f"Command {command} ran successfully on core {core}")

    for file_path in input_files:
        file_path.unlink()

    core_queue_global.put(core)

def init_worker(core_queue, failed_list):
    global core_queue_global, failed_list_global
    core_queue_global = core_queue
    failed_list_global = failed_list

def main():
    papi_events = "PAPI_BR_MSP,PAPI_TOT_INS,PAPI_L2_DCM,PAPI_L2_DCR,PAPI_TOT_CYC"
    env = os.environ.copy()
    env['PAPI_EVENTS'] = papi_events
    env["OMP_NUM_THREADS"] = "1"
    env["LD_LIBRARY_PATH"] = "/scr/studyztp/compiler/llvm-dir/lib/aarch64-unknown-linux-gnu"

    workdir = Path().cwd()

    cores = ['100_101', '102_103', '104_105', '106_107', '108_109', '110_111', '112_113',
        '114_115', '116_117', '118_119', '120_121', '122_123', '124_125', '126_127',
        '128_129', '130_131', '132_133', '134_135', '136_137', '138_139', '140_141',
        '142_143', '144_145', '146_147', '148_149', '150_151', '152_153', '154_155',
        '156_157', '158_159']
    
    max_threads = len(cores)

    core_queue = multiprocessing.Queue()
    for core in cores:
        core_queue.put(core)

    manager = multiprocessing.Manager()
    failed_list = manager.list()

    input_dir = Path(workdir/"experiments/input")
    experiment_dir = Path(workdir/"experiments/papi-nugget-data/saphir-experiment")
    experiment_dir.mkdir(parents=True, exist_ok=True)
    nugget_list = []
    nugget_list_path = Path(workdir/"experiments/info/ir-bb-analysis/comparison/random-selection/selected-regions.txt")
    with open(nugget_list_path, "r") as f:
        for line in f.readlines():
            nugget_list.append(int(line.strip()))
            
    nugget_executable_base_name = "saphir_papi_nuggets_exe_"
    nugget_executable_base_path = Path(workdir/"cbuild/llvm-exec")

    all_run_balls = []
    for rid in nugget_list:
        nugget_exe = Path(nugget_executable_base_path / f"{nugget_executable_base_name}{rid}/{nugget_executable_base_name}{rid}")
        command = ["mpirun", "-n", "1", nugget_exe.as_posix(), "i_lsms"]
        run_dir = Path(experiment_dir / f"{rid}/run0")

        if run_dir.exists():
            if Path(run_dir/"papi_hl_output").exists():
                continue

        run_ball = {
            "command": command,
            "run_dir": run_dir,
            "run.log": "run.log",
            "run.err": "run.err",
            "input_dir": input_dir.as_posix()
        }
        all_run_balls.append(run_ball)

    # Use initializer to pass core_queue and failed_list globally
    with multiprocessing.Pool(max_threads, initializer=init_worker, initargs=(core_queue, failed_list)) as pool:
        pool.map(run_this, all_run_balls)

    print("Failed list: ", list(failed_list))
    print("Failed list length: ", len(failed_list))

    with open(experiment_dir / "failed_list.txt", "w") as failed_list_file:
        for failed in failed_list:
            failed_list_file.write(f"{failed}\n")

    print("Done running all experiments")

if __name__ == "__main__":
    main()

