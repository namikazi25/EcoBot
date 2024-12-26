import dask.dataframe as dd

# Load the dataset using Dask
df = dd.read_parquet("hf://datasets/BGLab/BioTrove/**/*.parquet")

# # Inspect the dataset
# print(df.head())

# Take a small sample (e.g., 0.1% of the dataset)
subset = df.sample(frac=0.001).compute()  # Adjust `frac` for larger/smaller subsets

# Save the subset for testing
subset_path = "./Database/subset_test.csv"
subset.to_csv(subset_path, index=False)
print(f"Subset saved to {subset_path}")