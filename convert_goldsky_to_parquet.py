import polars as pl
import os

# Define paths
csv_path = "goldsky/orderFilled.csv"
parquet_path = "goldsky/orderFilled.parquet"
archive_path = "archive.tar.xz"

print(f"Starting conversion of {csv_path} to {parquet_path}...")

# Check if CSV exists
if not os.path.exists(csv_path):
    print(f"Error: CSV file not found at {csv_path}. Exiting.")
    exit(1)

# Load the CSV
print(f"Loading {csv_path} (this may take a while for large files)...")
df = pl.read_csv(csv_path, schema_overrides={'makerAssetId': pl.Utf8, 'takerAssetId': pl.Utf8})
print(f"CSV loaded. Shape: {df.shape}")

# Write to Parquet
print(f"Writing to {parquet_path}...")
df.write_parquet(parquet_path)
print(f"Parquet file created.")

# Verify new file size and delete old files
if os.path.exists(parquet_path):
    original_csv_size = os.path.getsize(csv_path)
    parquet_file_size = os.path.getsize(parquet_path)

    print(f"Original CSV size: {original_csv_size / (1024**3):.2f} GB")
    print(f"Parquet file size: {parquet_file_size / (1024**3):.2f} GB")
    print(f"Space saved: {(original_csv_size - parquet_file_size) / (1024**3):.2f} GB")

    # Delete the original CSV and the archive to free up space
    print(f"Deleting original CSV: {csv_path}")
    os.remove(csv_path)
    print(f"Deleting archive: {archive_path}")
    os.remove(archive_path)
    print("Original CSV and archive deleted. Disk space reclaimed.")
else:
    print(f"Error: Parquet file not found after writing. Conversion failed.")

print("Conversion process complete.")
