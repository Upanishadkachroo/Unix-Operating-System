import os

def tell_wait():
    global p2c, c2p
    p2c = os.pipe()
    c2p = os.pipe()

def tell_parent():
    os.write(c2p[1], b'x')

def wait_parent():
    os.read(p2c[0], 1)

def tell_child():
    os.write(p2c[1], b'x')

def wait_child():
    os.read(c2p[0], 1)

def main():
    tell_wait()
    pid = os.fork()

    if pid > 0:
        # Parent
        print("Parent: setup done.")
        tell_child()  # Let child run
        wait_child()  # Wait for child
        print("Parent: child finished!")
    else:
        # Child
        wait_parent()
        print("Child: running task...")
        tell_parent()
        os._exit(0)

if __name__ == "__main__":
    main()

