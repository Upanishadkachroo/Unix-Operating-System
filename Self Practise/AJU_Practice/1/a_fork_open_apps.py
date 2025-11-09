import os
import time

print(f"Parent PID: {os.getpid()}")

# List of Linux applications to open
apps = [("Terminal", "xterm"), ("Editor", "gedit"), ("File Manager", "nautilus")]

for name, app in apps:
    pid = os.fork()
    if pid == 0:
        # Child process
        print(f"👶 Child ({name}) PID={os.getpid()} | Parent PID={os.getppid()}")
        try:
            os.execlp(app, app)  # replaces child process with new program
        except FileNotFoundError:
            print(f"⚠️ {app} not found on this system.")
            os._exit(1)
    else:
        print(f"🧠 Parent created child PID={pid} for {name}")
        time.sleep(1)  # give each process time to launch

# Wait for all children
while True:
    try:
        pid, status = os.wait()
        print(f"✅ Child PID={pid} terminated with status {status}")
    except ChildProcessError:
        break
