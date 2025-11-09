#!/bin/bash
# Check file existence

read -p "Enter full file path: " file

if [ -f "$file" ]; then
    echo "File exists: $file"
else
    echo "File does not exist."
fi

# -f checks for regular file.

# Can also use:

# -d for directories.

# -e for any file type.