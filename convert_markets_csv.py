import polars as pl
import os

csv_path = "markets.csv"
parquet_path = "markets.parquet"

print(f"Converting {csv_path} to {parquet_path}...")

if os.path.exists(csv_path):
    # Schema overrides for long token IDs, as used in get_markets
    schema_overrides = {
        "token1": pl.Utf8,
        "token2": pl.Utf8,
    }
    df = pl.read_csv(csv_path, schema_overrides=schema_overrides)
    df.write_parquet(parquet_path)
    print(f"Conversion complete. Parquet file created at {parquet_path}.")
    print(f"Deleting original CSV: {csv_path}")
    os.remove(csv_path)
else:
    print(f"Error: {csv_path} not found. Skipping conversion.")

print("Markets CSV conversion process complete.")
