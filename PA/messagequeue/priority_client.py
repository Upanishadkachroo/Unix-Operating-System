import sysv_ipc

key = 3000
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

print("Client ready. Enter messages with priority (1–10). Type 'exit' to quit.")

while True:
    text = input("Message: ")
    if text.lower() == "exit":
        break
    try:
        priority = int(input("Priority (1–10): "))
    except ValueError:
        print("Invalid priority. Try again.")
        continue
    mq.send(text.encode(), type=priority)
    print(f"[Client] Sent '{text}' with priority {priority}")
