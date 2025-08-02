import os

def main():
    print("Beginning")
    counter = 0
    pid = os.fork()

    if pid == 0:
        # Child process
        for i in range(5):
            counter += 1
            print(f"Child process = {counter}")
        print("Child Ended")
    elif pid > 0:
        # Parent process
        for i in range(5):
            counter += 1
            print(f"Parent process = {counter}")
        print("Parent Ended")
    else:
        print("fork() failed")
        return 1

if __name__ == "__main__":
    main()

