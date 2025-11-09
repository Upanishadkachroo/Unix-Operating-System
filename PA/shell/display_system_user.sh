#!/bin/bash
# Display system users

echo "=== Currently Logged-In Users ==="
who

echo "=== All System Users ==="
cut -d: -f1 /etc/passwd
