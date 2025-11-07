import sysv_ipc

key = 5000
mq = sysv_ipc.MessageQueue(key)

total = 0
while True:
    message, t = mq.receive()
    msg = message.decode()

    if msg == "END":
        break
    total += int(msg)

print(f"[Receiver] Sum of numbers: {total}")

# Cleanup
mq.remove()
