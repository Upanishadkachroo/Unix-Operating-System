import os
import sys

def mini_shell():
    print("🔹 Simple Python Shell (type 'exit' to quit) 🔹")
    while True:
        try:
            cmd = input("shell> ").strip()
            if not cmd:
                continue
            if cmd.lower() == "exit":
                print("👋 Exiting shell.")
                break

            pid = os.fork()
            if pid == 0:
                # Child executes the command
                try:
                    args = cmd.split()
                    os.execvp(args[0], args)  # Use PATH to find command
                except FileNotFoundError:
                    print(f"❌ Command not found: {cmd}")
                os._exit(1)
            else:
                # Parent waits for child
                pid_done, status = os.waitpid(pid, 0)
                print(f"✅ Process {pid_done} finished with exit code {os.WEXITSTATUS(status)}\n")

        except KeyboardInterrupt:
            print("\n(Use 'exit' to quit safely.)")
        except EOFError:
            print("\nEOF detected. Exiting shell.")
            break

if __name__ == "__main__":
    mini_shell()
