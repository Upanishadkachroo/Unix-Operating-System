import os

def main():
    r_fd, w_fd=os.pipe()
    
    pid=os.fork()

    if pid!=0:
        os.close(r_fd)
        childid=2
        os.write(w_fd, childid.to_bytes(4, byteorder='little'))
        print(f"parent ({os.getpid()}) send childid: {childid}")
        os.close(w_fd)

    else:
        os.close(w_fd)
        data=os.read(r_fd, 4)
        childid=int.from_bytes(data, byteorder='little')
        print(f"child ({os.getpid()}) recieved childid: {childid}")

        os.close(r_fd)

if __name__=="__main__":
    main()
