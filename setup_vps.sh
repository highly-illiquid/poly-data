#!/bin/bash
set -e

# --- Configuration ---
GITHUB_REPO_URL="https://github.com/highly-illiquid/poly-data.git" # REPLACE WITH YOUR ACTUAL GITHUB REPO URL
PROJECT_DIR="poly-data" # Name of the directory created by git clone
DATA_SNAPSHOT_URL="https://polydata-archive.s3.us-east-1.amazonaws.com/archive.tar.xz"
ARCHIVE_FILE="archive.tar.xz"

echo "Starting VPS setup for ${PROJECT_DIR}..."

# --- Step 1: Update System Packages ---
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# --- Step 2: Install Essential Tools ---
echo "Installing git, python3, and python3-pip..."
sudo apt install git python3 python3-pip unzip -y

# Install eza
echo "Installing eza..."
sudo apt update
sudo apt install -y gpg
sudo mkdir -p /etc/apt/keyrings
wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc | sudo gpg --dearmor -o /etc/apt/keyrings/gierens.gpg
echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" | sudo tee /etc/apt/sources.list.d/gierens.list
sudo chmod 644 /etc/apt/keyrings/gierens.gpg /etc/apt/sources.list.d/gierens.list
sudo apt update
sudo apt install -y eza

# Install ble.sh
echo "Installing ble.sh..."
git clone --recursive https://github.com/akinomyoga/ble.sh.git ~/.local/share/blesh-repo
cd ~/.local/share/blesh-repo
make install
cd - # Go back to previous directory

# Install Oh My Posh
echo "Installing Oh My Posh..."
curl -s https://ohmyposh.dev/install.sh | bash -s

# Configure Oh My Posh for Bash
echo "Configuring Oh My Posh for Bash..."
echo 'eval "$(oh-my-posh init bash)"' >> ~/.bashrc

# Configure eza alias for Bash
echo "Configuring eza alias..."
echo "alias ls='eza -lh --group-directories-first --icons --time-style=long-iso'" >> ~/.bashrc

# Configure ble.sh for Bash
echo "Configuring ble.sh..."
echo "source ~/.local/share/blesh/ble.sh" >> ~/.bashrc

# Install zoxide
echo "Installing zoxide..."
curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh

# Configure zoxide for Bash
echo "Configuring zoxide..."
echo 'eval "$(zoxide init bash)"' >> ~/.bashrc
echo 'alias cd="z"' >> ~/.bashrc

# --- Step 3: Install UV (Python Package Manager) ---
echo "Installing uv..."
if ! command -v uv &> /dev/null
then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add uv to PATH for the current session. For persistent path, user needs to add to .bashrc
    source "$HOME/.cargo/env"
    echo "uv installed. Note: For persistent uv access, you might need to add 'source \$HOME/.cargo/env' to your shell's startup file (e.g., ~/.bashrc)."
else
    echo "uv is already installed."
fi

# --- Step 4: Clone the Project Repository ---
echo "Cloning the project repository from ${GITHUB_REPO_URL}..."
git clone "${GITHUB_REPO_URL}"
cd "${PROJECT_DIR}"

# --- Step 5: Download and Extract Initial Data Snapshot ---
echo "Downloading initial data snapshot from ${DATA_SNAPSHOT_URL}..."
wget "${DATA_SNAPSHOT_URL}"

echo "Extracting data snapshot..."
tar -xf "${ARCHIVE_FILE}"

# --- Step 6: Install Python Dependencies ---
echo "Installing Python dependencies using uv..."
uv sync

echo "VPS setup complete for ${PROJECT_DIR}!"
echo "You can now run your data pipeline using: tmux new -s data_pipeline && uv run python update_all.py"
