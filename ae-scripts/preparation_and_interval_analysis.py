#!/usr/bin/env python3
"""Automation for building and running NPB IR BB analysis binaries."""

import argparse
import os
import shutil
import subprocess
import time
from pathlib import Path
import sys

def run_command(cmd, cwd, env=None, stdout=None, stderr=None):
    print(f"Running: {' '.join(map(str, cmd))} (cwd={cwd})")
    subprocess.run(cmd, cwd=cwd, env=env, check=True, stdout=stdout, stderr=stderr)


def build_targets(lsms_root: Path, region_length: int, architecture: str):
    ae_cbuild = lsms_root / "ae-cbuild"
    ae_cbuild.mkdir(parents=True, exist_ok=True)
    ae_cmake = lsms_root / "ae-cmake"

    if not Path(ae_cbuild/f"llvm-bc/lsms_ir_bb_analysis_bc/lsms_ir_bb_analysis_bc.bc").is_file():
        ir_bb_bc_env = os.environ.copy()
        ir_bb_bc_env["NUGGET_PROCESS_TYPE"] = "lsms-ir-bb-analysis-bc"
        ir_bb_bc_env["REGION_LENGTH"] = str(region_length)
        ir_bb_bc_env["NUGGET_CONFIG_FILE"] = str(
            lsms_root
            / "ae-cmake"
            / "ir-bb-analysis"
            / "cmake"
            / "ir-bb-analysis-bc.cmake"
        )

        run_command(["cmake", f"-DCMAKE_TOOLCHAIN_FILE={ae_cmake}/lsms-toolchain-generic-cpu.cmake", f"{lsms_root}/lsms" ], cwd=ae_cbuild, env=ir_bb_bc_env)
        run_command(["cmake", "--build", ".", "--target=lsms_ir_bb_analysis_bc"], cwd=ae_cbuild)

    if not Path(ae_cbuild/f"llvm-exec/lsms_ir_bb_analysis_{architecture}_exe/lsms_ir_bb_analysis_{architecture}_exe").is_file():
        ir_bb_exe_env = os.environ.copy()
        ir_bb_exe_env["NUGGET_PROCESS_TYPE"] = "lsms-ir-bb-analysis-exe"
        ir_bb_exe_env["NUGGET_CONFIG_FILE"] = str(
            lsms_root
            / "ae-cmake"
            / "ir-bb-analysis"
            / "cmake"
            / "ir-bb-analysis-exe.cmake"
        )

        run_command(["cmake", f"-DCMAKE_TOOLCHAIN_FILE={ae_cmake}/lsms-toolchain-generic-cpu.cmake", f"{lsms_root}/lsms" ], cwd=ae_cbuild, env=ir_bb_exe_env)
        run_command(["cmake", "--build", ".", f"--target=lsms_ir_bb_analysis_{architecture}_exe"], cwd=ae_cbuild)

    return ae_cbuild

def run_analyses(lsms_root: Path, llvm_exe_dir: Path, input_directory: Path, input_command: str, architecture: str):
    binary = Path(llvm_exe_dir/f"lsms_ir_bb_analysis_{architecture}_exe/lsms_ir_bb_analysis_{architecture}_exe")

    ae_experiments = lsms_root / "ae-experiments"
    analysis_dir = ae_experiments / "analysis" 
    analysis_dir.mkdir(parents=True, exist_ok=True)

    target_dir = analysis_dir / input_command / architecture
    target_dir.mkdir(parents=True, exist_ok=True)

    shutil.copytree(input_directory, target_dir, dirs_exist_ok=True)

    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"

    stdout_path = target_dir / "stdout.log"
    stderr_path = target_dir / "stderr.log"
    exec_time_path = target_dir / "execution_time.txt"

    with stdout_path.open("wb") as out, stderr_path.open("wb") as err:
        start = time.perf_counter()
        # Run from the per-binary output folder so any files the binary emits land there
        run_command(["mpirun", "-np", "1", str(binary)] + input_command.split(" "), cwd=target_dir, env=env, stdout=out, stderr=err)
        duration = time.perf_counter() - start

    exec_time_path.write_text(f"{duration:.3f}\n")

    # copy the bb-info-output to the target_dir
    src = (llvm_exe_dir / ".." / "bb-info-output" / "basic-block-info.txt").resolve()
    dst = target_dir / "basic-block-info.txt"
    if not src.is_file():
        raise FileNotFoundError(f"Expected basic-block-info.txt at {src}")
    shutil.copy2(src, dst)

def parse_args():
    parser = argparse.ArgumentParser(description="Build and run NPB IR BB analysis binaries.")
    parser.add_argument(
        "--project-dir",
        "-d",
        help="Path to project root containing nugget-protocol-NPB",
    )
    parser.add_argument(
        "--input-directory",
        "-r",
        default="ae-scripts/input",
        help="Relative path to input directory from project root. (default: 'ae-scripts/input')",
    )
    parser.add_argument(
        "--input-command",
        "-c",
        default="i_lsms",
        help="Input command to run LSMS. (default: 'i_lsms')",
    )
    parser.add_argument(
        "--region-length",
        "-l",
        type=int,
        default=100_000_000,
        help="Region length for basic block profiling. (default: 100,000,000)",
    )
    parser.add_argument(
        "--architecture",
        "-a",
        type=str,
        default=os.uname().machine,
        help="Target architecture for the build (default: detected architecture)"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    project_dir = Path(args.project_dir).expanduser().resolve()
    lsms_root = project_dir / "nugget-protocol-lsms"

    if not lsms_root.is_dir():
        raise FileNotFoundError(f"Expected nugget-protocol-lsms under {project_dir}")
    
    architecture = args.architecture
    print(f"Building for architecture: {architecture}")

    ae_cbuild = build_targets(lsms_root, args.region_length, architecture)
    llvm_exec_dir = ae_cbuild / "llvm-exec"

    if not llvm_exec_dir.is_dir():
        raise FileNotFoundError(f"Expected llvm-exec directory at {llvm_exec_dir}")
    
    input_directory = Path(lsms_root/args.input_directory)
    if not input_directory.is_dir():
        raise FileNotFoundError(f"Expected input directory at {input_directory}")

    run_analyses(lsms_root, llvm_exec_dir, input_directory=input_directory, input_command=args.input_command, architecture=architecture)

    print(f"Project directory: {project_dir.as_posix()}; Input Directory: {input_directory.as_posix()};"
          f" Input Command: {args.input_command}; Region Length: {args.region_length}\n\n")
    
    print("Experiments Finished.\n")

if __name__ == "__main__":
    main()
