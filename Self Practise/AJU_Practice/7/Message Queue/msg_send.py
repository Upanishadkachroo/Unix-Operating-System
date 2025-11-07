import sysv_ipc

def message_sender():
    key = 1234  # Must match receiver
    message_text = "Did you get this?"

    # Create or attach to message queue
    try:
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
        print(f"[Sender] Message Queue created with key={key}")
    except Exception as e:
        print("[Sender] Error creating MessageQueue:", e)
        return

    # Send message (type = 1)
    mq.send(message_text.encode(), type=1)
    print(f"[Sender] Message sent: {message_text}")

if __name__ == "__main__":
    message_sender()
