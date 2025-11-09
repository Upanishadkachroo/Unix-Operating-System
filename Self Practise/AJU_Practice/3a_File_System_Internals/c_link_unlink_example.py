import os
import stat

original = input("Enter existing file path: ")
link_name = input("Enter name for new hard link: ")

try:
    os.link(original, link_name)
    print(f"\nHard link created: {link_name}")

    stat_orig = os.stat(original)
    stat_link = os.stat(link_name)

    print("\nComparing Inode and Link Count:")
    print("-" * 40)
    print(f"Original File Inode : {stat_orig.st_ino}")
    print(f"Linked File Inode   : {stat_link.st_ino}")
    print(f"Original Links      : {stat_orig.st_nlink}")
    print(f"Linked File Links   : {stat_link.st_nlink}")

    if stat_orig.st_ino == stat_link.st_ino:
        print("\n✅ Both files share the same inode → Hard link confirmed.")
    else:
        print("\n❌ Different inodes → Not a hard link.")

    # Uncomment the next line to remove the link (simulate unlink())
    # os.unlink(link_name)
    # print(f"{link_name} removed successfully.")

except Exception as e:
    print("Error:", e)
