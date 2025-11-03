import sysv_ipc

key=1234
mq=sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

# ipcs -q        # show active message queues
# ipcrm -q <msqid>  # remove message queue