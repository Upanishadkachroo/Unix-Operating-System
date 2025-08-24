import os

def bidirectional_pipe():
    #create two pipes
    parent_to_child_r, parent_to_child_w = os.pipe()
    child_to_parent_r, child_to_parent_w = os.pipe()

    pid=os.fork()
    if pid > 0:
        # Parent
        os.close(parent_to_child_r)
        os.close(child_to_parent_w)

        os.write(parent_to_child_w, b"Hi Child, this is Parent")
        os.close(parent_to_child_w)

        response = os.read(child_to_parent_r, 1024)
        print("Parent received:", response.decode())
        os.close(child_to_parent_r)

    else:
        # Child
        os.close(parent_to_child_w)
        os.close(child_to_parent_r)

        msg = os.read(parent_to_child_r, 1024)
        print("Child received:", msg.decode())
        os.close(parent_to_child_r)

        os.write(child_to_parent_w, b"Hi Parent, this is Child")
        os.close(child_to_parent_w)

if __name__=="_main_":
    bidirectional_pipe()
