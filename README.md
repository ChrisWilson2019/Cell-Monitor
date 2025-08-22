# Cellular RF Monitor
A Python script that connects to a network device via SSH and displays key RF metrics (RSSI, RSRP, RSRQ, SNR) with color-coded values.

1. Download and Extract
- Assuming you have received the file cellmon.tar.gz
- Run the following commands:
        tar -xvzf cellmon.tar.gz
        cd cellmon

2. Install and Configure
-Run the installation script, which will:
-Install the required Python dependency (paramiko)
-Prompt for your device username and password
-Save credentials securely
-Create a convenient cellmon alias
        ./install_cellmon.sh

3. Activate the Alias
-After installation, source your shell configuration file:
        source ~/.bashrc   # or ~/.zshrc if using Zsh

4. Run the Monitor
- When ready, type:
        cellmon

- You'll be prompted for the device IP address:
        Enter device IP: X.X.X.X <--This will be the IP of the devcice
        The script will display RF metrics in color (RSSI, RSRP, RSRQ, SNR), updated every few seconds.

5. Stop the Monitor
- Press Ctrl+C to exit the monitor
