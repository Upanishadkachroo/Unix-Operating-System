import os
import stat

path = input("Enter directory path: ")

try:
    files = os.listdir(path)
    print(f"\nFile Types in Directory: {path}")
    print("-" * 50)
    print(f"{'Filename':<30} {'Type':<20}")
    print("-" * 50)

    for f in files:
        full_path = os.path.join(path, f)
        try:
            mode = os.stat(full_path).st_mode
            if stat.S_ISREG(mode):
                ftype = "Regular File"
            elif stat.S_ISDIR(mode):
                ftype = "Directory"
            elif stat.S_ISCHR(mode):
                ftype = "Character Device"
            elif stat.S_ISBLK(mode):
                ftype = "Block Device"
            elif stat.S_ISLNK(mode):
                ftype = "Symbolic Link"
            elif stat.S_ISSOCK(mode):
                ftype = "Socket"
            elif stat.S_ISFIFO(mode):
                ftype = "FIFO / Pipe"
            else:
                ftype = "Unknown"
            print(f"{f:<30} {ftype:<20}")
        except FileNotFoundError:
            continue

except Exception as e:
    print("Error:", e)
