# Active Context

**Current Focus:** Resolving VPS disk space issue to enable successful data extraction and pipeline setup.

**Recent Changes:**
- The `setup_vps.sh` script has been significantly enhanced to include:
    - Installation of `unzip`.
    - Installation and configuration of `Oh My Posh`.
    - Installation and configuration of `eza` (modern `ls` replacement).
    - Installation and configuration of `ble.sh` (Bash Line Editor).
- Identified critical blocker: VPS disk is full, preventing complete data extraction.
- Decision made to delete incomplete `poly-data` directory and `archive.tar.xz` file, then free up sufficient disk space before retrying data extraction.

**Next Steps:** User needs to free up disk space on the VPS. Once space is available, the user will re-clone the repository and re-attempt the data snapshot extraction.

**Important Patterns and Preferences:**
- Use `uv` for Python package management.
- Use `git` for code deployment to VPS.
- Use `rsync` for data synchronization from VPS to local.
- Utilize `tmux` on the VPS for running long-duration processes in the background.
- Enhanced shell experience with `Oh My Posh`, `eza`, and `ble.sh`.
