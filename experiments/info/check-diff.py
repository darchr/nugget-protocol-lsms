from pathlib import Path
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Get files diff")
parser.add_argument("--file1", type=str, help="Path to the first file", required=True)
parser.add_argument("--file2", type=str, help="Path to the second file", required=True)
parser.add_argument("--output-file", type=str, help="Path to the output file", required=True)
args = parser.parse_args()

file1 = Path(args.file1)
file2 = Path(args.file2)
output_file = Path(args.output_file)

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Make sure both DataFrames have the same columns
common_columns = df1.columns.intersection(df2.columns)
df1 = df1[common_columns]
df2 = df2[common_columns]

# Reset indices to make sure they match
df1 = df1.reset_index(drop=True)
df2 = df2.reset_index(drop=True)

# Now compare the DataFrames
diff = df1.compare(df2)
diff.to_csv(output_file, index=False)
