import os
import time

def child_task(name, exec_type):
    print(f"\n👶 Child {name} started with PID={os.getpid()}")
    
    if exec_type == "execlp":
        print("➡️ Using execlp() to run 'ls -l'")
        os.execlp("ls", "ls", "-l")

    elif exec_type == "execvp":
        print("➡️ Using execvp() to run 'echo Hello from execvp'")
        os.execvp("echo", ["echo", "Hello from execvp!"])

    elif exec_type == "execv":
        print("➡️ Using execv() to run '/bin/date'")
        os.execv("/bin/date", ["date"])

    elif exec_type == "execve":
        print("➡️ Using execve() to run '/usr/bin/env' with custom environment")
        env = {"USER": "Student", "MODE": "Learning", "PATH": os.environ["PATH"]}
        os.execve("/usr/bin/env", ["env"], env)

    else:
        print("Unknown exec type")
        os._exit(1)


exec_types = ["execlp", "execvp", "execv", "execve"]

for exec_type in exec_types:
    pid = os.fork()
    if pid == 0:
        # Child process executes specific variant
        child_task(exec_type, exec_type)
    else:
        print(f"🧠 Parent created child {pid} using {exec_type}")
        pid_done, status = os.waitpid(pid, 0)
        print(f"✅ Child {pid_done} finished.\n")
        time.sleep(1)
