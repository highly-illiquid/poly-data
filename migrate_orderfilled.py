
import os
import polars as pl
import pyarrow.parquet as pq
import time

SOURCE_FILE = "goldsky/orderFilled.parquet"
TARGET_DIR = "goldsky/orderFilled"

def migrate_orderfilled():
    """
    Converts a single large orderFilled.parquet file into a partitioned dataset
    using a low-memory, row-group-by-row-group approach.
    """
    print(f"Starting migration of {SOURCE_FILE} to partitioned dataset in {TARGET_DIR}...")

    if not os.path.exists(SOURCE_FILE):
        print(f"Error: Source file not found at {SOURCE_FILE}. Aborting.")
        return

    try:
        source_parquet_file = pq.ParquetFile(SOURCE_FILE)
        num_row_groups = source_parquet_file.num_row_groups
        print(f"Source file contains {num_row_groups} row groups.")

        for i in range(num_row_groups):
            print(f"Processing row group {i + 1} of {num_row_groups}...")
            
            # Read one row group into a PyArrow Table
            table = source_parquet_file.read_row_group(i)
            
            # Convert to Polars DataFrame for manipulation
            batch_df = pl.from_arrow(table)
            
            # Add date columns
            processed_batch_df = batch_df.with_columns([
                pl.from_epoch(pl.col('timestamp'), time_unit='s').dt.year().alias('year'),
                pl.from_epoch(pl.col('timestamp'), time_unit='s').dt.month().alias('month'),
                pl.from_epoch(pl.col('timestamp'), time_unit='s').dt.day().alias('day'),
            ])
            
            # Convert back to PyArrow Table for writing
            processed_table = processed_batch_df.to_arrow()
            
            # Write to partitioned dataset
            pq.write_to_dataset(
                processed_table,
                root_path=TARGET_DIR,
                partition_cols=['year', 'month', 'day'],
                existing_data_behavior='overwrite_or_ignore'
            )

        print("\nMigration complete.")
        
        original_size = os.path.getsize(SOURCE_FILE)
        print(f"Successfully migrated data.")
        print(f"You can now optionally delete the original file to save space: {SOURCE_FILE} ({original_size / 1e9:.2f} GB)")
        print(f"To do so, run: rm {SOURCE_FILE}")

    except Exception as e:
        print(f"An error occurred during migration: {e}")


if __name__ == "__main__":
    start_time = time.time()
    migrate_orderfilled()
    end_time = time.time()
    print(f"Total migration time: {end_time - start_time:.2f} seconds")
