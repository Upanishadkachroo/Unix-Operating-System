#!/bin/bash
# ============================================
# Script: clear_usb_history.sh
# Purpose: Safely remove USB (pendrive) history logs from Ubuntu/Linux system
# ============================================

# Ensure script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "⚠️  Please run this script using sudo:"
  echo "   sudo ./clear_usb_history.sh"
  exit 1
fi

echo "============================================"
echo "🔍 USB History Cleanup Tool"
echo "============================================"
read -p "This will permanently delete USB-related logs. Continue? (y/n): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
  echo "❌ Operation cancelled."
  exit 0
fi

echo "🧹 Clearing systemd (journal) logs..."
journalctl --rotate
journalctl --vacuum-time=1s

echo "🧹 Clearing /var/log entries..."
truncate -s 0 /var/log/syslog 2>/dev/null
truncate -s 0 /var/log/kern.log 2>/dev/null
truncate -s 0 /var/log/messages 2>/dev/null

echo "🧹 Clearing udev runtime data..."
rm -rf /run/udev/data/*

echo "🧹 Clearing user-specific recent and cache data..."
USER_HOME=$(eval echo ~${SUDO_USER})
rm -f "$USER_HOME/.local/share/recently-used.xbel"
rm -rf "$USER_HOME/.cache/"*
rm -rf "$USER_HOME/.local/share/gvfs-metadata/"*

echo "🧹 Clearing bash history..."
rm -f "$USER_HOME/.bash_history"
sudo -u "$SUDO_USER" bash -c "history -c"

echo "✅ All possible USB and shell history cleared."
echo "💡 Tip: Reboot your system for full effect (sudo reboot)."
echo "============================================"


##use sudo command to run
