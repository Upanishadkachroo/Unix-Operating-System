# cleanup.py
import sysv_ipc
mq = sysv_ipc.MessageQueue(5678)
mq.remove()
print("Message Queue removed.")

