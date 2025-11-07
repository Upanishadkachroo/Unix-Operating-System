import sysv_ipc

def message_receiver():
    key = 1234  # Must match sender

    try:
        mq = sysv_ipc.MessageQueue(key)
        print(f"[Receiver] Connected to Message Queue with key={key}")
    except Exception as e:
        print("[Receiver] Could not find MessageQueue. Start sender first.", e)
        return

    # Receive message of type 1
    message, msg_type = mq.receive(type=1)
    print(f"[Receiver] Received message (type {msg_type}): {message.decode()}")

    # Optional: remove the message queue after reading
    mq.remove()
    print("[Receiver] Queue removed from system.")

if __name__ == "__main__":
    message_receiver()
