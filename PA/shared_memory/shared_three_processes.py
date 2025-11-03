from multiprocessing import Process, Manager, Event

def proc_input(shared_lists, ready_sort: Event):
    s=input("Enter numbers separated by space: ").strip()
    nums=[]

    if s:
        nums=[int(x) for x in s.split()]
        shared_lists[:]=nums
        print("[Input] wrote numbers:", shared_lists)
        ready_sort.set()

def proc_sort(shared_lists, ready_sort: Event, ready_output: Event):
    ready_sort.wait()
    nums=list(shared_lists)
    nums.sort()
    shared_lists[:] = nums
    print("[Sort] sorted numbers:", shared_lists)
    ready.display.set()

def proc_display(shared_lists, ready_output: Event):
    ready_output.wait()
    print("[Display] sorted numbers are:", list(shared_lists))

if __name__=="__main__":
    mgr=Manager()
    shared_lists=mgr.list()
    ev_sort=Event()
    ev_display=Event()

    p1=Process(target=proc_input, args=(shared_lists, ev_sort))
    p2 = Process(target=proc_sort, args=(shared_list, ev_sort, ev_display))
    p3 = Process(target=proc_display, args=(shared_list, ev_display))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()