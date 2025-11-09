import os
import stat

path = input("Enter file path: ")

try:
    fd = os.open(path, os.O_RDONLY)  # open file descriptor
    file_stat = os.fstat(fd)

    print(f"\nFile statistics for: {path}")
    print("-" * 40)
    print(f"Inode Number : {file_stat.st_ino}")
    print(f"UID          : {file_stat.st_uid}")
    print(f"GID          : {file_stat.st_gid}")
    print(f"File Access Permission (FAP): {oct(file_stat.st_mode)}")

    mode = file_stat.st_mode
    print("File Type    :", end=" ")

    if stat.S_ISREG(mode):
        print("Regular File")
    elif stat.S_ISDIR(mode):
        print("Directory")
    elif stat.S_ISCHR(mode):
        print("Character Device")
    elif stat.S_ISBLK(mode):
        print("Block Device")
    elif stat.S_ISLNK(mode):
        print("Symbolic Link")
    else:
        print("Other")

    os.close(fd)

except FileNotFoundError:
    print("Error: File not found.")
