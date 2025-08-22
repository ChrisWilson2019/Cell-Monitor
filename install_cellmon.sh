#!/bin/bash
set -e
SCRIPT_DIR="$HOME/.config/nvim/scripts"
CONFIG_FILE="$HOME/.config/cellmon_config.json"
SCRIPT_FILE="$SCRIPT_DIR/cellular_monitor.py"

echo "Installing Cellular RF Monitor..."

# Install Python dependency
pip3 install --user paramiko || { echo "pip install failed"; exit 1; }

# Prompt for credentials
read -p "Enter device username: " USERNAME
read -sp "Enter device password: " PASSWORD
echo

# Save credentials in config file (user-only perms)
mkdir -p "$HOME/.config"
printf '{"username": "%s", "password": "%s"}\n' "$USERNAME" "$PASSWORD" > "$CONFIG_FILE"
chmod 600 "$CONFIG_FILE"
echo "Credentials saved to $CONFIG_FILE"

# Create script directory and copy script
mkdir -p "$SCRIPT_DIR"
cp ./cellular_monitor.py "$SCRIPT_FILE"
chmod +x "$SCRIPT_FILE"

# Add alias to bashrc if not present
if [ -n "$BASH_VERSION" ]; then
  SHELL_RC="$HOME/.bashrc"
elif [ -n "$ZSH_VERSION" ]; then
  SHELL_RC="$HOME/.zshrc"
else
  SHELL_RC="$HOME/.profile"
fi

if ! grep -q "alias cellmon=" "$SHELL_RC" 2>/dev/null; then
  echo "alias cellmon='python3 $SCRIPT_FILE'" >> "$SHELL_RC"
  echo "Alias 'cellmon' added to $SHELL_RC"
fi

echo "Installation complete!"
echo "Run: source $SHELL_RC"
echo "Then run: cellmon  (or just 'cellmon' and enter IP when prompted)"
