import os

def parent2child(filename):
    r, w=os.pipe()

    pid=os.fork()

    if pid>0:
        os.close(r)
        with open(filename, "r") as f:
            data=f.read()
        os.write(w, data.encode())
        os.close(w)
        os.wait()
    else:
        os.close(w)
        data=os.read(r, 1024).decode()
        print("child recieved data:\n", data)
        os.close(r)
        os.exit(0)

if __name__=="__main__":
    parent2child("example.txt")