#!/usr/bin/env python3
import subprocess
import re
import os
from pathlib import Path
import json

def get_marker_address(executable: Path, marker: str) -> str:
    """
    Runs 'objdump -S <executable>' and searches for lines like:
      0000000000415fbe <End_Marker>:
    Returns the hexadecimal address as a string, or None if not found.
    """
    try:
        output = subprocess.check_output(
            ["objdump", "-S", str(executable)],
            universal_newlines=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running objdump on {executable}: {e}")
        return None

    # Build a regex pattern that matches the address at the beginning of the line.
    # The pattern is anchored to the start of the line with ^ and uses multiline mode.
    pattern = re.compile(r"^([0-9a-f]+)\s+<" + re.escape(marker) + r">:", re.MULTILINE)
    match = pattern.search(output)
    if match:
        return match.group(1)
    return None

def main():
    result_dict = {}

    # Use pathlib to look in the current directory for files matching the name pattern.
    current_dir = Path().cwd()
    cbuild_dir = Path(current_dir/"cbuild/llvm-exec")
    print(cbuild_dir)
    for dir in cbuild_dir.glob("m5_nugget_exe_*"):
        # Check that the file exists and is executable.
        for exe in Path(dir).glob("m5_nugget_exe_*"):
            if exe.is_file() and os.access(exe, os.X_OK):
                end_addr = get_marker_address(exe, "End_Marker")
                start_addr = get_marker_address(exe, "Start_Marker")
                result_dict[exe.name] = {
                    "end_marker_addr": end_addr,
                    "start_marker_addr": start_addr
                }
    for dir in cbuild_dir.glob("m5_nugget_intel_exe_*"):
        # Check that the file exists and is executable.
        for exe in Path(dir).glob("m5_nugget_intel_exe_*"):
            if exe.is_file() and os.access(exe, os.X_OK):
                end_addr = get_marker_address(exe, "End_Marker")
                start_addr = get_marker_address(exe, "Start_Marker")
                result_dict[exe.name] = {
                    "end_marker_addr": end_addr,
                    "start_marker_addr": start_addr
                }

    for dir in cbuild_dir.glob("m5_nugget_4_threads_exe_*"):
        # Check that the file exists and is executable.
        for exe in Path(dir).glob("m5_nugget_4_threads_exe_*"):
            if exe.is_file() and os.access(exe, os.X_OK):
                end_addr = get_marker_address(exe, "End_Marker")
                start_addr = get_marker_address(exe, "Start_Marker")
                result_dict[exe.name] = {
                    "end_marker_addr": end_addr,
                    "start_marker_addr": start_addr
                }

    with open("addr_map.json", "w") as f:
        json.dump(result_dict, f, indent=4)

if __name__ == "__main__":
    main()

