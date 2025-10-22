# Active Context

**Current Focus:** Setting up the VPS environment for the Polymarket data pipeline.

**Recent Changes:**
- Initial plan for VPS setup, code transfer, dependency installation, pipeline execution, and data transfer was formulated.
- Decision to use `git` for code transfer from local to VPS, replacing the initial `rsync` suggestion for code.
- `rsync` will still be used for efficient data transfer from VPS back to the local machine.

**Next Steps:** Proceed with the detailed instructions for VPS setup, including installing necessary software, cloning the repository, installing dependencies, and running the data pipeline.

**Important Patterns and Preferences:**
- Use `uv` for Python package management.
- Use `git` for code deployment to VPS.
- Use `rsync` for data synchronization from VPS to local.
- Utilize `tmux` on the VPS for running long-duration processes in the background.