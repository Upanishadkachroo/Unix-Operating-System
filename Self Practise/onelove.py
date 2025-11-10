#!/usr/bin/env python3
"""
os_scheduling_and_sync_demo.py

Contains demos for:
1) process creation/termination
2) thread creation/termination
3) non-preemptive schedulers: FCFS, SJF, SRTF (SRTF is preemptive actually implemented),
   Priority (non-preemptive)
4) preemptive schedulers: Round Robin (quantum 2), LJF (preemptive), LRTF
5) HRRN
6) Multilevel Feedback Queue (Q1: RR q=4, Q2: RR q=8, Q3: FCFS)
7) Multilevel Queue (two queues, fixed process membership)
8) Producer-consumer using semaphores (threading)
9) Reader-writer using semaphores (reader priority)
10) Deadlock detection (resource allocation graph cycle detection)
11) Deadlock prevention (Banker's algorithm)
12) Memory management: best fit, worst fit, first fit
13) Page replacement: FIFO, LRU, Optimal
14) Disk scheduling: FCFS, SCAN, C-SCAN

Run and follow the prompts. Code is compact and commented.
"""
import threading
import multiprocessing
import time
import os
from collections import deque, defaultdict, OrderedDict
import heapq
import random
import sys
from threading import Semaphore, Lock
from queue import Queue

# -----------------------------
# 1. Process creation & termination (multiprocessing)
# -----------------------------
def process_demo():
    def worker(i):
        print(f"[Process {os.getpid()}] started worker {i}")
        time.sleep(1)
        print(f"[Process {os.getpid()}] terminating worker {i}")

    n = int(input("Number of processes to spawn: "))
    procs = []
    for i in range(n):
        p = multiprocessing.Process(target=worker, args=(i,))
        p.start()
        procs.append(p)
        print(f"Spawned process pid={p.pid}")
    for p in procs:
        p.join()
        print(f"Process pid={p.pid} joined (exitcode={p.exitcode})")
    print("All child processes finished.")

# -----------------------------
# 2. Thread creation & termination
# -----------------------------
def thread_demo():
    def tworker(i):
        print(f"[Thread {threading.get_ident()}] starting {i}")
        time.sleep(0.7)
        print(f"[Thread {threading.get_ident()}] finishing {i}")

    n = int(input("Number of threads to create: "))
    threads = []
    for i in range(n):
        t = threading.Thread(target=tworker, args=(i,))
        t.start()
        threads.append(t)
        print(f"Started thread {t.name}")
    for t in threads:
        t.join()
        print(f"Joined thread {t.name}")
    print("All threads finished.")

# -----------------------------
# scheduling helpers
# -----------------------------
def calc_avg_times(processes):
    # processes: list of dicts with keys: pid, arrival, burst, start, completion
    n = len(processes)
    total_tat = 0
    total_wt = 0
    for p in processes:
        tat = p['completion'] - p['arrival']
        wt = tat - p['burst_original']
        total_tat += tat
        total_wt += wt
    return total_tat / n, total_wt / n

def print_proc_table(processes):
    print("PID\tArrival\tBurst\tStart\tCompletion\tTurnaround\tWaiting")
    for p in sorted(processes, key=lambda x: x['pid']):
        tat = p['completion'] - p['arrival']
        wt = tat - p['burst_original']
        print(f"{p['pid']}\t{p['arrival']}\t{p['burst_original']}\t{p.get('start', '-')}\t{p['completion']}\t{tat}\t{wt}")

def get_process_input():
    n = int(input("Number of processes: "))
    processes = []
    for i in range(n):
        arr = int(input(f"Arrival time of P{i}: "))
        burst = int(input(f"Burst time of P{i}: "))
        prio = int(input(f"Priority of P{i} (lower value = higher priority): "))
        processes.append({'pid': i, 'arrival': arr, 'burst': burst, 'burst_original': burst, 'priority': prio})
    return processes

# -----------------------------
# 3a FCFS (non-preemptive)
# -----------------------------
def fcfs(processes):
    procs = sorted(processes, key=lambda x: (x['arrival'], x['pid']))
    time_now = 0
    for p in procs:
        if time_now < p['arrival']:
            time_now = p['arrival']
        p['start'] = time_now
        time_now += p['burst']
        p['completion'] = time_now
    print_proc_table(procs)
    print("Avg TAT, WT:", calc_avg_times(procs))

# -----------------------------
# 3b SJF (non-preemptive)
# -----------------------------
def sjf_nonpreemptive(processes):
    processes = sorted(processes, key=lambda x: (x['arrival'], x['pid']))
    n = len(processes)
    completed = 0
    time_now = 0
    procs = [dict(p) for p in processes]
    ready = []
    idx = 0
    while completed < n:
        while idx < n and procs[idx]['arrival'] <= time_now:
            heapq.heappush(ready, (procs[idx]['burst'], procs[idx]['arrival'], procs[idx]['pid'], procs[idx]))
            idx += 1
        if not ready:
            time_now = procs[idx]['arrival']
            continue
        _, _, _, p = heapq.heappop(ready)
        p['start'] = time_now
        time_now += p['burst']
        p['completion'] = time_now
        completed += 1
    print_proc_table(sorted(procs, key=lambda x: x['pid']))
    print("Avg TAT, WT:", calc_avg_times(procs))

# -----------------------------
# 3c SRTF (preemptive shortest remaining time first)
# -----------------------------
def srtf(processes):
    n = len(processes)
    procs = sorted([dict(p) for p in processes], key=lambda x: x['arrival'])
    time_now = 0
    completed = 0
    ready = []
    idx = 0
    last_pid = None
    while completed < n:
        while idx < n and procs[idx]['arrival'] <= time_now:
            p = procs[idx]
            heapq.heappush(ready, (p['burst'], p['arrival'], p['pid'], p))
            idx += 1
        if not ready:
            time_now = procs[idx]['arrival']
            continue
        rem, _, _, p = heapq.heappop(ready)
        if 'start' not in p:
            p['start'] = time_now
        # execute 1 time unit
        p['burst'] -= 1
        time_now += 1
        if p['burst'] == 0:
            p['completion'] = time_now
            completed += 1
        else:
            heapq.heappush(ready, (p['burst'], p['arrival'], p['pid'], p))
    print_proc_table(sorted(procs, key=lambda x: x['pid']))
    print("Avg TAT, WT:", calc_avg_times(procs))

# -----------------------------
# 3d Priority non-preemptive
# -----------------------------
def priority_nonpreemptive(processes):
    procs = sorted(processes, key=lambda x: (x['arrival'], x['pid']))
    n = len(procs)
    completed = 0
    time_now = 0
    ready = []
    idx = 0
    procs = [dict(p) for p in procs]
    while completed < n:
        while idx < n and procs[idx]['arrival'] <= time_now:
            p = procs[idx]
            heapq.heappush(ready, (p['priority'], p['arrival'], p['pid'], p))
            idx += 1
        if not ready:
            time_now = procs[idx]['arrival']
            continue
        _, _, _, p = heapq.heappop(ready)
        p['start'] = time_now
        time_now += p['burst']
        p['completion'] = time_now
        completed += 1
    print_proc_table(sorted(procs, key=lambda x: x['pid']))
    print("Avg TAT, WT:", calc_avg_times(procs))

# -----------------------------
# 4a Round Robin (quantum 2 by default)
# -----------------------------
def round_robin(processes, quantum=2):
    procs = sorted([dict(p) for p in processes], key=lambda x: (x['arrival'], x['pid']))
    n = len(procs)
    time_now = 0
    queue = deque()
    idx = 0
    completed = 0
    in_queue = set()
    while completed < n:
        while idx < n and procs[idx]['arrival'] <= time_now:
            queue.append(procs[idx])
            in_queue.add(procs[idx]['pid'])
            idx += 1
        if not queue:
            time_now = procs[idx]['arrival']
            continue
        p = queue.popleft()
        if 'start' not in p:
            p['start'] = time_now
        exec_time = min(quantum, p['burst'])
        p['burst'] -= exec_time
        time_now += exec_time
        # add newly arrived during execution
        while idx < n and procs[idx]['arrival'] <= time_now:
            queue.append(procs[idx]); in_queue.add(procs[idx]['pid']); idx += 1
        if p['burst'] == 0:
            p['completion'] = time_now
            completed += 1
        else:
            queue.append(p)
    print_proc_table(sorted(procs, key=lambda x: x['pid']))
    print("Avg TAT, WT:", calc_avg_times(procs))

# -----------------------------
# 4b LJF preemptive (Longest job first preemptive -> longest remaining)
# -----------------------------
def ljf_preemptive(processes):
    # implement as selecting process with largest remaining time each time unit
    n = len(processes)
    procs = sorted([dict(p) for p in processes], key=lambda x: x['arrival'])
    time_now = 0
    idx = 0
    completed = 0
    # max-heap via negative burst
    ready = []
    while completed < n:
        while idx < n and procs[idx]['arrival'] <= time_now:
            p = procs[idx]
            heapq.heappush(ready, (-p['burst'], p['arrival'], p['pid'], p))
            idx += 1
        if not ready:
            time_now = procs[idx]['arrival']
            continue
        neg_rem, _, _, p = heapq.heappop(ready)
        if 'start' not in p:
            p['start'] = time_now
        # execute 1 unit
        p['burst'] -= 1
        time_now += 1
        if p['burst'] == 0:
            p['completion'] = time_now
            completed += 1
        else:
            heapq.heappush(ready, (-p['burst'], p['arrival'], p['pid'], p))
    print_proc_table(sorted(procs, key=lambda x: x['pid']))
    print("Avg TAT, WT:", calc_avg_times(procs))

# -----------------------------
# 4c LRTF (Longest remaining time first) - same as LJF preemptive
# -----------------------------
def lrtf(processes):
    ljf_preemptive(processes)

# -----------------------------
# 5 HRRN
# -----------------------------
def hrrn(processes):
    procs = sorted([dict(p) for p in processes], key=lambda x: (x['arrival'], x['pid']))
    n = len(procs)
    completed = 0
    time_now = 0
    ready = []
    idx = 0
    while completed < n:
        while idx < n and procs[idx]['arrival'] <= time_now:
            ready.append(procs[idx]); idx += 1
        if not ready:
            time_now = procs[idx]['arrival']
            continue
        # calculate response ratio = (waiting + service)/service = (time_now - arrival + burst)/burst
        best = max(ready, key=lambda p: ((time_now - p['arrival'] + p['burst'])/p['burst']))
        ready.remove(best)
        best['start'] = time_now
        time_now += best['burst']
        best['completion'] = time_now
        completed += 1
    print_proc_table(sorted(procs, key=lambda x: x['pid']))
    print("Avg TAT, WT:", calc_avg_times(procs))

# -----------------------------
# 6 Multilevel Feedback Queue
# -----------------------------
def mlfq(processes):
    # Q1 RR q=4, Q2 RR q=8, Q3 FCFS
    q1 = deque()
    q2 = deque()
    q3 = deque()
    procs = sorted([dict(p) for p in processes], key=lambda x: x['arrival'])
    time_now = 0
    idx = 0
    completed = 0
    n = len(procs)
    while completed < n:
        while idx < n and procs[idx]['arrival'] <= time_now:
            q1.append(procs[idx]); idx += 1
        executed = False
        for queue, quantum in [(q1,4),(q2,8),(q3,None)]:
            if not queue: continue
            p = queue.popleft()
            if 'start' not in p:
                p['start'] = time_now
            if quantum is None:
                # FCFS until finish
                time_now += p['burst']
                p['burst'] = 0
                p['completion'] = time_now
                completed += 1
            else:
                exec_t = min(quantum, p['burst'])
                p['burst'] -= exec_t
                time_now += exec_t
                # newly arrived may append to q1
                while idx < n and procs[idx]['arrival'] <= time_now:
                    q1.append(procs[idx]); idx += 1
                if p['burst'] == 0:
                    p['completion'] = time_now
                    completed += 1
                else:
                    # demote
                    if queue is q1:
                        q2.append(p)
                    elif queue is q2:
                        q3.append(p)
            executed = True
            break
        if not executed:
            if idx < n:
                time_now = procs[idx]['arrival']
            else:
                break
    print_proc_table(sorted(procs, key=lambda x: x['pid']))
    print("Avg TAT, WT:", calc_avg_times(procs))

# -----------------------------
# 7 Multilevel Queue (static membership)
# -----------------------------
def multilevel_queue(processes):
    # The prompt suggests P0,P1,P4 in Q1 and P2,P3 in Q2
    # We'll allow user to enter membership manually if number of processes differ.
    procs = sorted([dict(p) for p in processes], key=lambda x: x['pid'])
    q1_pids = input("Enter PIDs for Queue1 (comma sep) e.g. 0,1,4 : ").strip()
    q1 = set()
    if q1_pids:
        q1 = set(int(x.strip()) for x in q1_pids.split(',') if x.strip()!='')
    q2 = set(p['pid'] for p in procs if p['pid'] not in q1)
    time_now = 0
    completed = 0
    n = len(procs)
    # Q1 has priority and uses FCFS; then Q2 uses FCFS
    # process as arrivals permit
    remaining = {p['pid']: dict(p) for p in procs}
    while completed < n:
        # try to schedule from Q1 first
        candidates = [p for p in remaining.values() if p['pid'] in q1 and p['arrival'] <= time_now]
        if candidates:
            p = min(candidates, key=lambda x: x['arrival'])
            if 'start' not in p: p['start'] = max(time_now, p['arrival'])
            time_now = max(time_now, p['arrival']) + p['burst']
            p['completion'] = time_now
            completed += 1
            del remaining[p['pid']]
            continue
        # else Q2
        candidates = [p for p in remaining.values() if p['arrival'] <= time_now]
        if candidates:
            p = min(candidates, key=lambda x: x['arrival'])
            if 'start' not in p: p['start'] = max(time_now, p['arrival'])
            time_now = max(time_now, p['arrival']) + p['burst']
            p['completion'] = time_now
            completed += 1
            del remaining[p['pid']]
            continue
        # nothing ready
        if remaining:
            time_now = min(p['arrival'] for p in remaining.values())
    procs_final = [remaining.get(i) or next((x for x in procs if x['pid']==i), None) for i in range(len(procs))]
    # collect completions from procs list
    for p in procs:
        if 'completion' not in p:
            # must extract from stored
            pass
    print_proc_table(sorted(procs, key=lambda x: x['pid']))
    print("Avg TAT, WT:", calc_avg_times(procs))

# -----------------------------
# 8 Producer-Consumer using semaphores
# -----------------------------
def producer_consumer_demo():
    buffer = []
    BUFFER_SIZE = int(input("Buffer size: "))
    mutex = Semaphore(1)
    empty = Semaphore(BUFFER_SIZE)
    full = Semaphore(0)
    def producer(id, items):
        for item in items:
            empty.acquire()
            mutex.acquire()
            buffer.append(item)
            print(f"Producer {id} produced {item}. Buffer size: {len(buffer)}")
            mutex.release()
            full.release()
            time.sleep(0.2)
    def consumer(id, count):
        for _ in range(count):
            full.acquire()
            mutex.acquire()
            item = buffer.pop(0)
            print(f"Consumer {id} consumed {item}. Buffer size: {len(buffer)}")
            mutex.release()
            empty.release()
            time.sleep(0.3)
    pcount = int(input("Number of producers: "))
    ccount = int(input("Number of consumers: "))
    items_per_producer = int(input("Items per producer: "))
    prod_threads = []
    cons_threads = []
    for i in range(pcount):
        t = threading.Thread(target=producer, args=(i, [f"P{i}-item{j}" for j in range(items_per_producer)]))
        t.start(); prod_threads.append(t)
    for i in range(ccount):
        t = threading.Thread(target=consumer, args=(i, (pcount*items_per_producer)//ccount))
        t.start(); cons_threads.append(t)
    for t in prod_threads: t.join()
    for t in cons_threads: t.join()
    print("Producer-consumer demo finished.")

# -----------------------------
# 9 Reader-Writer using semaphores (reader preference)
# -----------------------------
def reader_writer_demo():
    rw_mutex = Semaphore(1)
    mutex = Semaphore(1)
    read_count = {'value': 0}
    shared_data = {'value': 0}
    def reader(id, loops=3):
        for _ in range(loops):
            mutex.acquire()
            read_count['value'] += 1
            if read_count['value'] == 1:
                rw_mutex.acquire()
            mutex.release()
            # reading
            print(f"Reader {id} reads value {shared_data['value']}")
            time.sleep(0.2)
            mutex.acquire()
            read_count['value'] -= 1
            if read_count['value'] == 0:
                rw_mutex.release()
            mutex.release()
            time.sleep(0.1)
    def writer(id, loops=3):
        for _ in range(loops):
            rw_mutex.acquire()
            shared_data['value'] += 1
            print(f"Writer {id} updated value to {shared_data['value']}")
            time.sleep(0.4)
            rw_mutex.release()
            time.sleep(0.1)
    rnum = int(input("Number of readers: "))
    wnum = int(input("Number of writers: "))
    threads = []
    for i in range(rnum):
        t = threading.Thread(target=reader, args=(i,))
        t.start(); threads.append(t)
    for i in range(wnum):
        t = threading.Thread(target=writer, args=(i,))
        t.start(); threads.append(t)
    for t in threads: t.join()
    print("Reader-Writer demo finished.")

# -----------------------------
# 10 Deadlock detection (RAG cycle detection)
# -----------------------------
def deadlock_detection_demo():
    # Build resource allocation graph from user
    # nodes: P0..Pn and R0..Rm; edges: P->R (request) and R->P (assignment)
    print("Deadlock detection using simple resource allocation graph (cycle detection).")
    nP = int(input("Number of processes: "))
    nR = int(input("Number of resource types: "))
    # read assignments: for each resource, which process holds it (or -1)
    alloc = defaultdict(list)  # R -> [P]
    req = defaultdict(list)    # P -> [R]
    for r in range(nR):
        holders = input(f"List PIDs holding R{r} (comma sep, or blank): ").strip()
        if holders:
            for h in holders.split(','):
                alloc[f"R{r}"].append(f"P{int(h.strip())}")
    for p in range(nP):
        wants = input(f"List resource IDs P{p} is requesting (comma sep like 0,1 or blank): ").strip()
        if wants:
            for w in wants.split(','):
                req[f"P{p}"].append(f"R{int(w.strip())}")
    # build directed graph edges: P->R for request; R->P for allocation
    graph = defaultdict(list)
    nodes = set()
    for p, rs in req.items():
        nodes.add(p)
        for r in rs:
            graph[p].append(r); nodes.add(r)
    for r, ps in alloc.items():
        nodes.add(r)
        for p in ps:
            graph[r].append(p); nodes.add(p)
    # detect cycle via DFS
    visited = set()
    stack = set()
    def dfs(u):
        visited.add(u); stack.add(u)
        for v in graph[u]:
            if v not in visited:
                if dfs(v): return True
            elif v in stack:
                return True
        stack.remove(u)
        return False
    dead = False
    for node in nodes:
        if node not in visited:
            if dfs(node):
                dead = True
                break
    if dead:
        print("Deadlock detected (cycle present in resource allocation graph).")
    else:
        print("No deadlock detected.")

# -----------------------------
# 11 Deadlock prevention: Banker's Algorithm (safety check)
# -----------------------------
def bankers_demo():
    print("Banker's algorithm safety check.")
    P = int(input("Number of processes: "))
    R = int(input("Number of resource types: "))
    print("Enter Allocation matrix rows for each P (space separated counts per resource):")
    Allocation = []
    for i in range(P):
        row = list(map(int, input(f"A[{i}]: ").split()))
        Allocation.append(row)
    print("Enter Max matrix rows for each P:")
    Max = []
    for i in range(P):
        row = list(map(int, input(f"Max[{i}]: ").split()))
        Max.append(row)
    Available = list(map(int, input("Enter Available vector (space separated): ").split()))
    Need = [[Max[i][j]-Allocation[i][j] for j in range(R)] for i in range(P)]
    finish = [False]*P
    safe_seq = []
    while True:
        found = False
        for i in range(P):
            if not finish[i] and all(Need[i][j]<=Available[j] for j in range(R)):
                for j in range(R):
                    Available[j] += Allocation[i][j]
                finish[i] = True
                safe_seq.append(i)
                found = True
        if not found:
            break
    if all(finish):
        print("System is in safe state. Safe sequence:", safe_seq)
    else:
        print("System is NOT in safe state. Deadlock or unsafe allocation possible.")

# -----------------------------
# 12 Memory management: best/worst/first fit
# -----------------------------
def memory_management_demo():
    mem_size = int(input("Total memory size (units): "))
    blocks = list(map(int, input("Enter partition sizes (space separated): ").split()))
    procs = list(map(int, input("Enter process sizes (space separated): ").split()))
    def first_fit(blocks, procs):
        alloc = [-1]*len(procs)
        bcopy = blocks[:]
        for i, p in enumerate(procs):
            for j, b in enumerate(bcopy):
                if b >= p:
                    alloc[i] = j
                    bcopy[j] -= p
                    break
        return alloc, bcopy
    def best_fit(blocks, procs):
        alloc = [-1]*len(procs)
        bcopy = blocks[:]
        for i, p in enumerate(procs):
            best_j = -1; best_size = 10**18
            for j, b in enumerate(bcopy):
                if b >= p and b < best_size:
                    best_size = b; best_j = j
            if best_j != -1:
                alloc[i] = best_j
                bcopy[best_j] -= p
        return alloc, bcopy
    def worst_fit(blocks, procs):
        alloc = [-1]*len(procs)
        bcopy = blocks[:]
        for i, p in enumerate(procs):
            worst_j = -1; worst_size = -1
            for j, b in enumerate(bcopy):
                if b >= p and b > worst_size:
                    worst_size = b; worst_j = j
            if worst_j != -1:
                alloc[i] = worst_j
                bcopy[worst_j] -= p
        return alloc, bcopy
    for name, fn in [("First Fit", first_fit), ("Best Fit", best_fit), ("Worst Fit", worst_fit)]:
        alloc, rem = fn(blocks, procs)
        print(f"\n{name}:")
        for i, a in enumerate(alloc):
            if a==-1: print(f"Process {i} (size {procs[i]}) -> Not allocated")
            else: print(f"Process {i} (size {procs[i]}) -> Block {a}")
        print("Remaining block sizes:", rem)

# -----------------------------
# 13 Page replacement: FIFO, LRU, Optimal
# -----------------------------
def page_replacement_demo():
    ref_string = list(map(int, input("Enter page reference string (space separated): ").split()))
    frames = int(input("Number of frames: "))
    def fifo(ref, frames):
        q = deque()
        s = set()
        faults = 0
        for p in ref:
            if p not in s:
                faults += 1
                if len(q) < frames:
                    q.append(p); s.add(p)
                else:
                    old = q.popleft(); s.remove(old)
                    q.append(p); s.add(p)
        return faults
    def lru(ref, frames):
        s = set()
        order = OrderedDict()
        faults = 0
        for p in ref:
            if p not in s:
                faults += 1
                if len(s) < frames:
                    s.add(p)
                else:
                    # remove least recently used
                    old = next(iter(order))
                    order.pop(old)
                    s.remove(old)
                    s.add(p)
            else:
                # update order
                if p in order: order.pop(p)
            order[p] = True
        return faults
    def optimal(ref, frames):
        faults = 0
        mem = []
        for i, p in enumerate(ref):
            if p in mem:
                continue
            faults += 1
            if len(mem) < frames:
                mem.append(p)
            else:
                # choose page whose next use is farthest
                next_uses = []
                for m in mem:
                    try:
                        idx = ref.index(m, i+1)
                    except ValueError:
                        idx = float('inf')
                    next_uses.append((idx, m))
                # evict max idx
                evict = max(next_uses)[1]
                mem[mem.index(evict)] = p
        return faults
    print("FIFO faults:", fifo(ref_string, frames))
    print("LRU faults:", lru(ref_string, frames))
    print("Optimal faults:", optimal(ref_string, frames))

# -----------------------------
# 14 Disk scheduling: FCFS, SCAN, C-SCAN
# -----------------------------
def disk_scheduling_demo():
    requests = list(map(int, input("Enter requests (space separated): ").split()))
    head = int(input("Enter initial head position: "))
    def fcfs(req, head):
        dist = 0
        cur = head
        for r in req:
            dist += abs(r-cur); cur = r
        return dist
    def scan(req, head, disk_size):
        left = sorted([r for r in req if r < head])
        right = sorted([r for r in req if r >= head])
        dist = 0; cur = head
        # assume head moves toward higher end first
        for r in right:
            dist += abs(r-cur); cur = r
        # go to end
        dist += abs((disk_size-1)-cur); cur = disk_size-1
        # then service left in reverse
        for r in reversed(left):
            dist += abs(r-cur); cur = r
        return dist
    def c_scan(req, head, disk_size):
        left = sorted([r for r in req if r < head])
        right = sorted([r for r in req if r >= head])
        dist = 0; cur = head
        for r in right:
            dist += abs(r-cur); cur = r
        # go to end
        dist += abs((disk_size-1)-cur)
        # jump to 0 (no servicing during jump, but distance considered)
        dist += disk_size-1
        cur = 0
        for r in left:
            dist += abs(r-cur); cur = r
        return dist
    disk_size = int(input("Disk size (number of cylinders): "))
    print("FCFS total head movement:", fcfs(requests, head))
    print("SCAN total head movement:", scan(requests, head, disk_size))
    print("C-SCAN total head movement:", c_scan(requests, head, disk_size))

# -----------------------------
# Utility to run scheduling menu
# -----------------------------
def scheduling_menu():
    print("Enter processes details for scheduling demos.")
    processes = get_process_input()
    # create deep copies when needed
    while True:
        print("\nScheduling demos:")
        print("1 FCFS\n2 SJF (non-preemptive)\n3 SRTF (preemptive)\n4 Priority (non-preemptive)\n5 Round Robin (quantum=2)\n6 LJF (preemptive)\n7 LRTF\n8 HRRN\n9 MLFQ\n10 Multilevel Queue\n0 Back to main menu")
        c = input("Choice: ").strip()
        cp = [dict(p) for p in processes]
        if c=='1': fcfs(cp)
        elif c=='2': sjf_nonpreemptive(cp)
        elif c=='3': srtf(cp)
        elif c=='4': priority_nonpreemptive(cp)
        elif c=='5': round_robin(cp, quantum=2)
        elif c=='6': ljf_preemptive(cp)
        elif c=='7': lrtf(cp)
        elif c=='8': hrrn(cp)
        elif c=='9': mlfq(cp)
        elif c=='10': multilevel_queue(cp)
        elif c=='0': break
        else: print("Invalid")

# -----------------------------
# Main menu
# -----------------------------
def main():
    while True:
        print("\n=== OS & Scheduling Demos ===")
        print("1 Process creation & termination")
        print("2 Thread creation & termination")
        print("3 CPU Scheduling (menu)")
        print("4 Preemptive scheduling (RR/LJF/LRTF) - use scheduling menu too")
        print("5 HRRN (use scheduling menu)")
        print("6 Multilevel Feedback Queue (use scheduling menu)")
        print("7 Multilevel Queue (use scheduling menu)")
        print("8 Producer-Consumer (semaphores)")
        print("9 Reader-Writer (semaphores)")
        print("10 Deadlock detection (RAG)")
        print("11 Deadlock prevention (Banker's)")
        print("12 Memory management (Best/Worst/First fit)")
        print("13 Page replacement (FIFO/LRU/Optimal)")
        print("14 Disk scheduling (FCFS/SCAN/C-SCAN)")
        print("0 Exit")
        ch = input("Choice: ").strip()
        if ch=='1': process_demo()
        elif ch=='2': thread_demo()
        elif ch=='3': scheduling_menu()
        elif ch=='4': scheduling_menu()
        elif ch=='5': scheduling_menu()
        elif ch=='6': scheduling_menu()
        elif ch=='7': scheduling_menu()
        elif ch=='8': producer_consumer_demo()
        elif ch=='9': reader_writer_demo()
        elif ch=='10': deadlock_detection_demo()
        elif ch=='11': bankers_demo()
        elif ch=='12': memory_management_demo()
        elif ch=='13': page_replacement_demo()
        elif ch=='14': disk_scheduling_demo()
        elif ch=='0': print("Exit."); break
        else: print("Invalid choice.")

if __name__ == "__main__":
    main()

