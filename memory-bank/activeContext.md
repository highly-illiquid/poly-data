# Active Context

**Current Focus:** Finalizing the end-to-end, memory-safe, partitioned parquet data pipeline.

**Recent Changes:**
- **`update_markets.py`:** Re-architected to fetch newest markets first, avoiding an inefficient loop through all historical data. Made resilient to inconsistent API schemas (missing columns, wrong data types).
- **`migrate_orderfilled.py`:** Created a low-memory, one-time migration script using a row-group-by-row-group PyArrow approach to convert a large legacy Parquet file into the new partitioned format.
- **`process_live.py`:** Completely re-architected to be memory-safe on a resource-constrained VPS. It now processes files in small chunks instead of attempting to `concat` a large list of lazy frames, which was causing memory spikes. The script is now robust against the schema inconsistencies discovered in the raw data.
- **Data Structure:** Corrected a major structural issue where raw data was being incorrectly saved into the `processed/` directory. The project now follows a clean datalake structure (`raw/`, `processed/`).

**Next Steps:**
- Run the final, re-architected `process_live.py` script to generate the clean `processed/trades` dataset.
- Once the pipeline is confirmed to run successfully end-to-end, the project can move to the analysis phase.

**Important Patterns and Preferences:**
- **Memory First:** All data processing must be designed with low memory usage as a primary constraint. Prefer streaming, chunking, or lazy operations where possible, but be aware that some lazy operations like `pl.concat` can still have high memory overhead.
- **Defensive Coding:** Assume all external data sources are unstable. Code must be resilient to schema changes, missing columns, and incorrect data types.