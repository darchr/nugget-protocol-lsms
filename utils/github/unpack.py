from pathlib import Path
import json

workdir = Path().cwd()
file_path = Path(__file__).parent
if Path(file_path / "packaged_files.json").exists():
    with open(file_path / "packaged_files.json", "r") as f:
        all_packaged_files = json.load(f)["files"]
    Path(file_path / "packaged_files.json").unlink()
else:
    all_packaged_files = []

def build_file(package_path: Path):
    filename = str(package_path.name).replace("_splitted_package", "")
    total_size = len(list(package_path.iterdir()))
    with open(package_path / f"../{filename}", "wb") as f:
        for i in range(total_size):
            with open(package_path / f"{filename}_{i}", "rb") as chunk_file:
                f.write(chunk_file.read())
    print(f"Built {package_path}")
    for file in package_path.iterdir():
        file.unlink()
    package_path.rmdir()

def check_dir(dir_path: Path):
    for file in dir_path.iterdir():
        if file.is_dir():
            if "_splitted_package" in file.name:
                build_file(file)
            else:
                check_dir(file)

for packaged_file in all_packaged_files:
    if Path(workdir/packaged_file).exists():
        build_file(Path(workdir/packaged_file))
    else:
        print(f"Skipping {packaged_file} because it does not exist")

#check_dir(workdir)

print("Done building all packages")
