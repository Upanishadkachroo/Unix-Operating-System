#!/bin/bash
# Display Disk Information

echo "=== Disk Partitions and Usage ==="
df -h
echo "=== Mounted File Systems ==="
lsblk
