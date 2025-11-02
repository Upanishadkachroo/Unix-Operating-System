import os

def main():
    # Create two pipes
    parent_to_child = os.pipe()   # (r1, w1)
    child_to_parent = os.pipe()   # (r2, w2)

    pid = os.fork()

    if pid > 0:
        # ------------------ Parent Process ------------------
        os.close(parent_to_child[0])  # Close read end of pipe1
        os.close(child_to_parent[1])  # Close write end of pipe2

        # Take input from user
        num1 = input("Enter first number: ")
        num2 = input("Enter second number: ")
        data = f"{num1} {num2}\n"

        # Send data to child
        os.write(parent_to_child[1], data.encode())

        # Read result from child
        result = os.read(child_to_parent[0], 1024).decode()
        print(f"Sum received from child: {result.strip()}")

        # Close the pipes
        os.close(parent_to_child[1])
        os.close(child_to_parent[0])

    else:
        # ------------------ Child Process ------------------
        os.close(parent_to_child[1])  # Close write end of pipe1
        os.close(child_to_parent[0])  # Close read end of pipe2

        # Read data from parent
        data = os.read(parent_to_child[0], 1024).decode().strip()
        try:
            a, b = map(int, data.split())
            result = str(a + b) + "\n"
        except:
            result = "Invalid input\n"

        # Send result back to parent
        os.write(child_to_parent[1], result.encode())

        # Close pipes
        os.close(parent_to_child[0])
        os.close(child_to_parent[1])

        # Exit child process
        os._exit(0)

if __name__ == "__main__":
    main()

