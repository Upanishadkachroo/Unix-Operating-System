import os
import stat
import time

# Take file/directory name with full path
path = input("Enter the file or directory path: ")

try:
    file_stat = os.stat(path)

    print(f"\nFile Statistics for: {path}")
    print("-" * 40)
    print(f"Inode Number: {file_stat.st_ino}")
    print(f"Device: {file_stat.st_dev}")
    print(f"Mode (Permissions): {oct(file_stat.st_mode)}")
    print(f"Number of Hard Links: {file_stat.st_nlink}")
    print(f"User ID of Owner: {file_stat.st_uid}")
    print(f"Group ID of Owner: {file_stat.st_gid}")
    print(f"File Size: {file_stat.st_size} bytes")
    print(f"Last Accessed: {time.ctime(file_stat.st_atime)}")
    print(f"Last Modified: {time.ctime(file_stat.st_mtime)}")
    print(f"Last Status Change: {time.ctime(file_stat.st_ctime)}")

except FileNotFoundError:
    print("Error: File or directory not found.")
