import os

def main():
    r_fd, w_fd=os.pipe()

    pid=os.fork()

    if pid>0:
        os.close(r_fd)
        message="hello from parent"
        os.write(w_fd, message.encode())
        print(f"parent ({os.getpid()} sent message: {message}")
        os.close(w_fd)

    else:
        os.close(w_fd)
        data=os.read(r_fd, 1024)
        print(f"child process ({os.getpid()} read message: {data.decode()}")
        os.close(r_fd)

if __name__=="__main__":
    main()
