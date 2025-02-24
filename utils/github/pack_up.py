from pathlib import Path
import json

# package every file that is larger than 100 MB

size_limit = 90 * 1024 * 1024  # 90 MB

workdir = Path().cwd()
file_dir = Path(__file__).parent

included_files = [
f"{workdir.as_posix()}/cbuild/llvm-bc/lsms_ir_bb_analysis_include_library_bc/lsms_ir_bb_analysis_include_library_bc.bc",
f"{workdir.as_posix()}/cbuild/llvm-bc/lsms_ir_bb_analysis_include_library_bc_source_bc/lsms_ir_bb_analysis_include_library_bc_source_bc.bc",
f"{workdir.as_posix()}/cbuild/llvm-bc/lsms_ir_bb_analysis_include_library_exe_source_bc_shrunk_bc/lsms_ir_bb_analysis_include_library_exe_source_bc_shrunk_bc.bc"
] 

all_packaged_files = []

def split_file(file_path: Path):
    file_size = file_path.stat().st_size
    chunk_count = (file_size // size_limit) + 1
    package_output = Path(file_path.parent / f"{file_path.name}_splitted_package")
    package_output.mkdir(exist_ok=False)
    with open(file_path, "rb") as f:
        for i in range(chunk_count):
            chunk = f.read(size_limit)
            with open(package_output / f"{file_path.name}_{i}", "wb") as chunk_file:
                chunk_file.write(chunk)
    print(f"Split {file_path} into {package_output}")
    file_path.unlink()
    print(f"Removed {file_path}")
    return (package_output.relative_to(workdir)).as_posix()

def check_dir(dir_path: Path):
    for file in dir_path.iterdir():
        if file.is_dir():
            if file.name in excluded_folders:
                print(f"Skipping {file}")
                continue
            check_dir(file)
        else:
            if file.stat().st_size > size_limit:
                print(f"Packaging {file}")
                packaged_file = split_file(file)
                all_packaged_files.append(packaged_file)
                # package the file
                # shutil.move(file, workdir / "large_files" / file.name)

for file in included_files:
    packaged_file = split_file(Path(file))
    all_packaged_files.append(packaged_file)

#check_dir(workdir)

with open(file_dir / "packaged_files.json", "w") as f:
    json.dump({"files": all_packaged_files}, f)
print("Done packaging all files larger than 100 MB")

