import os
import time

def parent_child_pipe():
    # Create a pipe
    r, w = os.pipe()

    pid = os.fork()  # fork a new process

    if pid > 0:
        # Parent process
        os.close(r)  # close read end from parent side
        message = b"Hello from parent"
        print("[Parent] Writing message into pipe...")
        os.write(w, message)
        print("[Parent] Message sent through pipe ")
        os.close(w)  # close write end after completing

    else:
        # Child process
        os.close(w)  # close write end from child side
        print("[Child] Waiting to read message from pipe...")
        read_bytes = os.read(r, 1024)
        print("[Child] Message received from pipe :", read_bytes.decode())
        os.close(r)  # close read end
        print("[Child] Pipe read complete")

if __name__ == "_main_":
    parent_child_pipe()
