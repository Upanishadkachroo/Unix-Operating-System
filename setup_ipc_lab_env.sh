#!/bin/bash
# =============================================
# IPC Lab Environment Setup Script
# Author: Rythm
# Description: Installs all required tools,
# Python packages, and dependencies
# for IPC, Message Queues, Shared Memory,
# and Socket Programming experiments.
# =============================================

# Function for pretty printing
print_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

print_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

# Check root privileges
if [ "$EUID" -ne 0 ]; then
    print_error "Please run this script as root (sudo ./setup_ipc_lab_env.sh)"
    exit 1
fi

print_info "Updating system packages..."
apt update -y && apt upgrade -y

# ---------------------------------------------
# 🧩 Core system tools
# ---------------------------------------------
print_info "Installing core development tools..."
apt install -y build-essential gcc g++ make git vim curl wget unzip net-tools

# ---------------------------------------------
# 🧠 Python setup
# ---------------------------------------------
print_info "Installing Python and pip..."
apt install -y python3 python3-pip python3-venv

# ---------------------------------------------
# 🧮 Python libraries for IPC and experiments
# ---------------------------------------------
print_info "Installing Python libraries..."
pip install --upgrade pip
pip install sysv_ipc psutil numpy matplotlib

# sysv_ipc → for message queues, semaphores, shared memory
# psutil → for system info
# numpy, matplotlib → for data visualization in performance analysis

# ---------------------------------------------
# 🧠 Shared Memory, Semaphores, and IPC Tools
# ---------------------------------------------
print_info "Installing IPC utilities..."
apt install -y iproute2 iputils-ping ipcs procps

# ipcs → inspect shared memory, semaphores, message queues
# iproute2, iputils → for network/socket experiments

# ---------------------------------------------
# 🧵 Networking tools (for TCP/UDP experiments)
# ---------------------------------------------
print_info "Installing networking tools..."
apt install -y netcat-openbsd lsof telnet traceroute nmap

# netcat (nc) → test sockets manually
# lsof → check open ports and sockets

# ---------------------------------------------
# 🐚 Shell utilities for your shell scripting experiments
# ---------------------------------------------
print_info "Installing useful shell packages..."
apt install -y bc finger lftp

# bc → for calculator script
# finger → for user info script
# lftp → for FTP download experiments

# ---------------------------------------------
# 🧰 Optional: create a virtual environment
# ---------------------------------------------
read -p "Do you want to create a Python virtual environment for your IPC lab? (y/n): " choice
if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
    print_info "Creating virtual environment 'ipc_lab_env'..."
    python3 -m venv ~/ipc_lab_env
    echo "To activate later: source ~/ipc_lab_env/bin/activate"
fi

# ---------------------------------------------
# ✅ Verification section
# ---------------------------------------------
print_info "Verifying installations..."
python3 -c "import sysv_ipc; import psutil; print('[Python] sysv_ipc and psutil imported successfully!')"

if command -v ipcs &> /dev/null; then
    print_success "System V IPC tools installed successfully."
else
    print_error "ipcs command missing!"
fi

if command -v nc &> /dev/null; then
    print_success "Netcat installed successfully."
fi

if command -v gcc &> /dev/null; then
    print_success "C compiler installed successfully."
fi

print_success "All dependencies installed successfully! 🎉"
echo
echo "You are now ready to run:"
echo "  ✅ Shared Memory Programs (Python/C)"
echo "  ✅ Message Queue (sysv_ipc) Experiments"
echo "  ✅ Socket & Chat Applications"
echo "  ✅ Shell Automation Scripts"
echo
echo "To verify message queues or shared memory manually, use:"
echo "    ipcs -q   # message queues"
echo "    ipcs -m   # shared memory segments"
echo "    ipcs -s   # semaphores"
echo
echo "To remove all IPC objects (use carefully):"
echo "    ipcrm -a"

