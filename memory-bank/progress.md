# Progress

**What Works:**
- A comprehensive `setup_vps.sh` script has been developed, automating:
    - System updates and essential tool installations (`git`, `python3`, `pip`, `unzip`).
    - Shell enhancements (`Oh My Posh`, `eza`, `ble.sh`).
    - `uv` installation and Python dependency management.
    - Project repository cloning.
    - Data snapshot download and extraction (pending disk space).
- The plan incorporates best practices for code management (`git`) and efficient data transfer (`rsync`).
- The project's dependencies and operational procedures have been identified from `README.md` and `pyproject.toml`.

**What's Left to Build:**
- Successful execution of the data snapshot extraction on the VPS.
- Verification of data collection and processing.
- Regular data synchronization from VPS to local.

**Current Status:**
- Planning phase for VPS setup and initial configuration is complete.
- `setup_vps.sh` script is finalized and pushed to the remote repository.
- **Blocked:** Waiting for the user to free up sufficient disk space on the VPS to allow for complete data extraction.

**Known Issues:**
- **Critical:** VPS disk is full (38GB total, 38GB used), preventing the complete extraction of the data snapshot (`archive.tar.xz`). The `poly-data` directory currently contains an incomplete 27GB of data from a failed extraction.

**Evolution of Project Decisions:**
- Initial decision to use `rsync` for code transfer was revised to `git` for better version control and deployment practices.
- Added `unzip`, `Oh My Posh`, `eza`, and `ble.sh` to the VPS setup script for enhanced shell experience and utility.