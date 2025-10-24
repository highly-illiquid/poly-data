import polars as pl
import os

def convert_csv_to_parquet(csv_path, parquet_path, schema_overrides=None):
    print(f"Starting conversion of {csv_path} to {parquet_path}...")

    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}. Skipping.")
        return

    print(f"Loading {csv_path} lazily (memory-efficient)...")
    lf = pl.scan_csv(csv_path, schema_overrides=schema_overrides)

    print(f"Writing to {parquet_path} in a streaming fashion...")
    lf.sink_parquet(parquet_path)
    print(f"Parquet file created.")

    if os.path.exists(parquet_path):
        original_csv_size = os.path.getsize(csv_path)
        parquet_file_size = os.path.getsize(parquet_path)

        print(f"Original CSV size: {original_csv_size / (1024**3):.2f} GB")
        print(f"Parquet file size: {parquet_file_size / (1024**3):.2f} GB")
        print(f"Space saved: {(original_csv_size - parquet_file_size) / (1024**3):.2f} GB")

        print(f"Deleting original CSV: {csv_path}")
        os.remove(csv_path)
        print("Original CSV deleted. Disk space reclaimed.")
    else:
        print(f"Error: Parquet file not found after writing for {csv_path}. Conversion failed.")

# --- Main Conversion Logic ---
# Convert goldsky/orderFilled.csv
convert_csv_to_parquet(
    csv_path="goldsky/orderFilled.csv",
    parquet_path="goldsky/orderFilled.parquet",
    schema_overrides={'makerAssetId': pl.Utf8, 'takerAssetId': pl.Utf8}
)

# Convert processed/trades.csv
convert_csv_to_parquet(
    csv_path="processed/trades.csv",
    parquet_path="processed/trades.parquet"
)

print("All specified CSV conversions complete.")
