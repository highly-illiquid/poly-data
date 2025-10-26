# Tech Context

**Programming Language:** Python (version >= 3.8)

**Package Management:**
- `uv`: Primary package installer and resolver for Python dependencies.
- `pip`: Used for initial installation of `uv` if not installed via `curl` script.

**Version Control & Deployment:**
- `git`: For managing source code, pushing local changes to a remote repository (e.g., GitHub), and cloning/pulling updates on the VPS. Feature branches are used for new development.

**Data Storage: Partitioned Parquet Datalake**
- The entire data pipeline is built around partitioned Parquet datasets, creating a simple but powerful file-based datalake.
- **Raw Zone:** `markets_partitioned/` and `goldsky/orderFilled/` store raw data partitioned by date.
- **Processed Zone:** `processed/trades/` stores the final, enriched output, also as a partitioned dataset.
- This approach was chosen for high performance and memory efficiency on a resource-constrained VPS.
- The pipeline scripts are designed to be resilient to schema inconsistencies from the source APIs (e.g., missing columns, incorrect data types), which proved to be a major challenge.

**Data Transfer:**
- `rsync`: For efficient synchronization of processed data files from the VPS to the local machine.

**VPS Access & Management:**
- `ssh`: Secure shell for remote access to the VPS.
- `tmux` (or `screen`): Terminal multiplexer on the VPS to run long-duration processes in the background, allowing detachment and re-attachment.

**Shell Enhancements:**
- `unzip`: For extracting `.zip` archives (though `tar` is used for the main data snapshot).
- `Oh My Posh`: Custom prompt engine for enhanced shell aesthetics and information.
- `eza`: Modern replacement for `ls`, providing better defaults and features.
- `ble.sh`: Bash Line Editor, enhancing the interactive Bash experience.

**Key Python Libraries (from `pyproject.toml`):
- `pandas`
- `polars`
- `pyarrow`
- `requests`
- `gql[requests]`
- `flatten-json`

**Development Dependencies (optional, for local use):
- `jupyter`
- `notebook`
- `ipykernel`

**Operating System:**
- Local: macOS (darwin)
- VPS: Assumed to be a Linux distribution (e.g., Ubuntu, Debian) for `apt` commands.
