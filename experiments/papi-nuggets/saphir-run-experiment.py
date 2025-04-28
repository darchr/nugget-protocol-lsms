import argparse
import multiprocessing
import subprocess
import configparser
from pathlib import Path
import os
import shutil
import json
from datetime import datetime
import time  

def run_this(run_ball):
    global core_queue_global, failed_list_global

    core = core_queue_global.get()
    print("Running on core: ", core)
    cmd = run_ball["cmd"]
    dir = run_ball["dir"]
    env = run_ball["env"]
    input_dir = run_ball["input_dir"]
    dir = Path(dir)
    input_dir = Path(input_dir)

    input_files = []
    for file_path in input_dir.iterdir():
        if file_path.is_file():
            shutil.copy(file_path, dir / file_path.name)
            input_files.append(Path(dir / file_path.name))

    cpuset_name = "measurement/"  # Moved inside to ensure it's accessible
    # cset proc --exec --set=measurement/core_32 --
    command = ["cset", "proc","--exec", f"--set={cpuset_name}{str(core)}", "--" ] + cmd

    start_time = time.perf_counter()
    start_datetime = datetime.now()

    print(f"Running {' '.join(command)} in {dir}")
    with open(Path(dir)/"run.log", "w") as stdout:
        with open(Path(dir)/"run.err", "w") as stderr:
            try:
                result = subprocess.run(command, 
                                     cwd=dir, 
                                     env=env, 
                                     stdout=stdout, 
                                     stderr=stderr)
                end_time = time.perf_counter()
                duration = end_time - start_time

                with open(Path(dir)/"python-time.log", "w") as time_file:
                    time_file.write(f"Start time: {start_datetime}\n")
                    time_file.write(f"End time: {datetime.now()}\n")
                    time_file.write(f"Duration: {duration} seconds\n")

                # remove the input files after the run
                for file_path in input_files:
                    file_path.unlink()

                core_queue_global.put(core)

                if result.returncode != 0:
                    print(f"Command failed with return code: {result.returncode}")
                    # Print the last few lines of error output
                    with open(Path(dir)/"run.err", "r") as err_file:
                        err_content = err_file.readlines()
                        print("Last few lines of error output:")
                        for line in err_content[-5:]:
                            print(f"  {line.strip()}")
                        print("This is the command that failed:")
                        print(f"  {' '.join(command)}")
                        print(f"  in {dir}")
                    failed_list_global.append(f"  {' '.join(command)}")
                    return False
                return True
            except Exception as e:
                print(f"Exception while running command: {str(e)}")
                failed_list_global.append(f"  {' '.join(command)}")
                core_queue_global.put(core)
                return False
            
def init_worker(core_queue, failed_list):
    global core_queue_global, failed_list_global
    core_queue_global = core_queue
    failed_list_global = failed_list

def main():
    cores = [ "22_23", "24_25", "26_27", "28_29", "30_31", "32_33", "34_35",
              "38_39", "40_41", "42_43", "44_45", "46_47", "48_49", "50_51",
              "54_55", "56_57", "60_61", "62_63", "64_65", "66_67",
              "70_71", "72_73", "74_75", "76_77", "78_79"]
    max_threads = len(cores)

    core_queue = multiprocessing.Queue()
    for core in cores:
        core_queue.put(core)

    manager = multiprocessing.Manager()
    failed_list = manager.list()

    workdir = Path().cwd()

    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    env["LD_LIBRARY_PATH"] = "/scr/studyztp/compiler/llvm-dir/lib/aarch64-unknown-linux-gnu;"
    env["LD_LIBRARY_PATH"] += f"{workdir}/nugget_util/hook_helper/other_tools/papi/aarch64/lib"
    env["PAPI_EVENTS"] = "PAPI_BR_MSP,PAPI_TOT_INS,PAPI_L2_DCM,PAPI_L2_DCR,PAPI_TOT_CYC"
    workdir = Path().cwd()
    runs_range = (0, 1)
    experiments_dir = Path(workdir/"experiments/papi-nuggets/saphir-experiments")
    experiments_dir.mkdir(parents=True, exist_ok=True)

    all_run_balls = []

    all_nuggets = []
    # get all the nuggets
    with open(workdir/"experiments/info/k-means-selections/selected-regions.txt") as f:
        for line in f.readlines():
            all_nuggets.append(int(line.strip()))

    print("All nuggets: ", all_nuggets)

    input_dir = Path(workdir/"experiments/input")

    for nugget in all_nuggets:
        binary_path = Path(workdir/f"cbuild/llvm-exec/lsms_papi_nuggets_exe_{nugget}/lsms_papi_nuggets_exe_{nugget}")
        nugget_experiments_dir = Path(experiments_dir/f"{nugget}")
        nugget_experiments_dir.mkdir(parents=True, exist_ok=True)
        cmd = ["mpirun", "-n", "1", binary_path.as_posix(), "i_lsms"]
        for run in range(*runs_range):
            run_dir = Path(nugget_experiments_dir/f"run-{run}")
            if(run_dir.exists()):
                shutil.rmtree(run_dir)
            run_dir.mkdir(parents=True, exist_ok=False)
            run_ball = {
                "cmd": cmd,
                "dir": run_dir.as_posix(),
                "env": env.copy(),
                "input_dir": input_dir.as_posix()
            }
            all_run_balls.append(run_ball)

    # Use initializer to pass core_queue and failed_list globally
    with multiprocessing.Pool(max_threads, initializer=init_worker, initargs=(core_queue, failed_list)) as pool:
        pool.map(run_this, all_run_balls)

    print("Failed list: ", list(failed_list))
    print("Failed list length: ", len(failed_list))

    with open(experiments_dir / "failed_list.txt", "w") as failed_list_file:
        for failed in failed_list:
            failed_list_file.write(f"{failed}\n")

    print("Done running all experiments")

if __name__ == "__main__":
    main()

