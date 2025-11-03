import time
from multiprocessing import Process, Event
from multiprocessing import shared_memory

letter=26
buff_size=letter+1 # include null

def writer(shm_name, ready_event: Event):
    shm=shared_memory.SharedMemory(name=shm_name)
    try:
        letters = ''.join(chr(ord('A') + i) for i in range(LETTERS))
        shm.buf[:len(letters)] = letters.encode()
        shm.buf[len(letters)] = ord('\n')
        print("[Writer] wrote", letters)
        ready_event.set()
    finally:
        shm.close()

def reader_to_file(shm_name, ready_event: Event, outpath="out_letters.txt"):
    ready_event.wait()
    shm = shared_memory.SharedMemory(name=shm_name)
    try:
        raw = bytes(shm.buf[:BUF_SIZE]).split(b'\n', 1)[0]
        text = raw.decode()
        with open(outpath, "w") as f:
            f.write(text + "\n")
        print("[Reader] wrote to file:", outpath)
    finally:
        shm.close()

if __name__=="__main__":
    shm=shared_memory.SharedMemory(create=True, size=buff_size)
    ready=Event()

    p_writer=Process(target=writer, args=(shm.name, ready))
    p_reader=Process(target=reader_to_file, args=(shm.name, ready))

    p_writer.start()
    p_reader.start()
    p_writer.join()
    p_reader.join()

    shm.close()
    shm.unlink()