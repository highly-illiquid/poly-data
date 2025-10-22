# Tech Context

**Programming Language:** Python (version >= 3.8)

**Package Management:**
- `uv`: Primary package installer and resolver for Python dependencies.
- `pip`: Used for initial installation of `uv` if not installed via `curl` script.

**Version Control & Deployment:**
- `git`: For managing source code, pushing local changes to a remote repository (e.g., GitHub), and cloning/pulling updates on the VPS.

**Data Transfer:**
- `rsync`: For efficient synchronization of processed data files from the VPS to the local machine.

**VPS Access & Management:**
- `ssh`: Secure shell for remote access to the VPS.
- `tmux` (or `screen`): Terminal multiplexer on the VPS to run long-duration processes in the background, allowing detachment and re-attachment.

**Key Python Libraries (from `pyproject.toml`):
- `pandas`
- `polars`
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