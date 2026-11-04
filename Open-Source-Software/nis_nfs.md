# Practical: Installation, Configuration and Demonstration of NIS and NFS Server



Linux practical examination

Ubuntu 24.04 LTS



This practical covers two important Linux network services:

1. NIS (Network Information Service): Provides centralized user and group information across multiple Linux machines.
2. NFS (Network File System): Allows a Linux machine to share directories over a network so that other Linux machines can access them as if they were local directories.

We will configure both services on Ubuntu Linux, connect a client machine and demonstrate centralized authentication and remote directory sharing.

# PART A — NIS SERVER

## 1. Aim

To install, configure and demonstrate an NIS Server on Ubuntu Linux for centralized management of users, groups and authentication information across multiple Linux machines.

## 2. What is NIS?

NIS (Network Information Service) is a directory service developed by Sun Microsystems that allows multiple computers in a network to share centralized administrative information.

It was originally called Yellow Pages (YP).

NIS allows a system administrator to maintain user accounts, passwords, groups and other configuration information centrally rather than creating separate accounts on every computer.

For example:

Suppose a college computer laboratory has:

- 1 central Linux server.
- 20 Linux client computers.
- 100 student accounts.

Without NIS, administrators may need to create and maintain student accounts separately on all 20 computers.

With NIS, user information is maintained centrally on the NIS server, and client machines can retrieve that information from the server.

[Networking Operating Systems CO 32010 Objectives 2 Processes](https://images.openai.com/static-rsc-4/Q88uQZVWHkBt12RScUSVjcCd7FBqrYJ3DcYHWbxEenjsSxrb_UBsOqQibdDoWgBHaM3zFP3DspeMiExiyGj8Vt4iuz-BJFClp1Ew5whF9eFTwHbiCVcoxVRSmpxYzbWN2DJdwIbNiCboC5Qu7eZsg183yZMdSQYoUGIlJXSn9pA?purpose=inline)

[present5.com](https://present5.com/networking-operating-systems-co-32010-objectives-2-processes/?utm_source=chatgpt.com)

### Important characteristics of NIS

| Property                   | Description                                             |
| -------------------------- | ------------------------------------------------------- |
| Full form                  | Network Information Service                             |
| Original name              | Yellow Pages (YP)                                       |
| Architecture               | Client-server                                           |
| Purpose                    | Centralized network information management              |
| Transport                  | Primarily RPC over TCP/UDP                              |
| Common RPC port            | 111 (portmapper); NIS services use additional RPC ports |
| Main database              | NIS maps                                                |
| Authentication information | passwd, shadow, group maps                              |
| Configuration              | `/etc/yp.conf`, `/etc/nsswitch.conf`                    |
| Security                   | Legacy and insecure                                     |

Important: NIS is a legacy protocol. It does not provide modern secure authentication or encryption. Use LDAP/Kerberos or another supported centralized identity system for production environments.

## 3. NIS architecture

NIS generally consists of three components.

### 1. NIS Master Server

- Maintains the original NIS databases.
- Creates and updates NIS maps.
- Provides information to clients.
- Can distribute updates to slave servers.

### 2. NIS Slave Server

- Maintains replicated copies of NIS maps.
- Provides redundancy.
- Can serve client requests if the master is unavailable.

### 3. NIS Client

- Requests information from the NIS server.
- Uses centrally maintained user and group information.
- Can authenticate users using NIS-backed account information.

[PPT - Security of NIS (YP) PowerPoint Presentation, free download - ID:1292333](https://images.openai.com/static-rsc-4/eOLyYnrE6i_kS_J1fox1pxsCBmuJOiXp6FyJQDr9bdoyfQ-GMOCfysBfNHjrak4_YPIA_bDSzJydsW5jjPsMpZEsDtj7heudgvkstDdXYm3paFBl_v3dy0yMNvxJclzhRLMSB_I-yIG4rGayIfBFcD8asVqlQe-gr7lgRR-h5JA?purpose=inline)

[slideserve.com](https://www.slideserve.com/azia/security-of-nis-yp?utm_source=chatgpt.com)

For this practical, we will configure one NIS master server and one NIS client.

## 4. Requirements

| Component         | Role               |
| ----------------- | ------------------ |
| Machine 1         | NIS Server         |
| Machine 2         | NIS Client         |
| Operating system  | Ubuntu Linux 24.04 |
| Server hostname   | nis-server         |
| Client hostname   | nis-client         |
| Example server IP | 192.168.1.10       |
| Example client IP | 192.168.1.20       |
| NIS domain        | labnis             |

Use your actual IP addresses and hostnames in the lab.

Important: NIS domain is different from an Internet domain name. It is a logical name used to identify an NIS network.

## 5. Installation of NIS Server

Perform the following operations on the server machine.

### Step 1: Update the package repository

```
sudo apt update
```

### Step 2: Install NIS packages

```
sudo apt install nis -y
```

Depending on the Ubuntu release and package dependencies, the installation provides the NIS utilities, server and client components.

Check the installed packages:

```
dpkg -l | grep -E 'nis|ypserv|ypbind'
```

### Step 3: Configure the NIS domain name

Set the NIS domain name:

```
sudo nano /etc/defaultdomain
```

Add:

```
labnis
```

Save and exit.

Set the active NIS domain:

```
sudo domainname labnis
```

Verify:

```
domainname
```

Expected output:

```
labnis
```

What is the purpose of domainname?

It displays or sets the NIS domain name used by the system.

### Step 4: Configure the NIS server

Open:

```
sudo nano /etc/default/nis
```

Find the server configuration settings. Depending on the installed package version, set the relevant values as follows:

```
NISSERVER=master
NISCLIENT=false
```

This configures the machine as the NIS master server.

### Step 5: Configure the NIS server configuration file

Open:

```
sudo nano /etc/ypserv.securenets
```

This file controls which network addresses can communicate with the NIS server.

For a lab network, add the following example entry:

```
255.255.255.0 192.168.1.0
```

This permits clients on the `192.168.1.0/24` network.

For a local testing environment, loopback may also be allowed:

```
255.0.0.0 127.0.0.0
```

Do not expose NIS to untrusted networks.

### Step 6: Configure the NIS domain in the server

Open:

```
sudo nano /etc/yp.conf
```

For the master server, the client-style server discovery entries are not normally required. The important settings are the domain name and server configuration already established.

### Step 7: Create a NIS user

Create a normal Linux user that will be shared through NIS:

```
sudo adduser nisuser
```

Set a password when prompted.

Check the account:

```
id nisuser
```

This user will later be accessible from the NIS client.

## 6. Initialize the NIS database

This is a very important step.

NIS does not directly distribute `/etc/passwd` and `/etc/group` files. It converts selected system information into searchable NIS maps.

### Step 1: Initialize NIS maps

Execute:

```
sudo ypinit -m
```

This initializes the NIS master server.

You may see a prompt asking for NIS slave servers.

For this practical, press `Ctrl + D` if no slave server is being configured.

Confirm the configuration when prompted.

### Step 2: Understand NIS maps

NIS generates databases from system configuration files.

| Source file     | NIS map                                 |
| --------------- | --------------------------------------- |
| `/etc/passwd`   | `passwd.byname`, `passwd.byuid`         |
| `/etc/group`    | `group.byname`, `group.bygid`           |
| `/etc/hosts`    | `hosts.byname`, `hosts.byaddr`          |
| `/etc/networks` | `networks.byname`, `networks.byaddr`    |
| `/etc/services` | `services.byname`, `services.byservice` |

The maps are generally stored in:

```
/var/yp/labnis/
```

Check:

```
ls -l /var/yp/labnis/
```

### Step 3: Restart NIS services

```
sudo systemctl restart rpcbind
sudo systemctl restart ypserv
```

Check the services:

```
sudo systemctl status rpcbind
sudo systemctl status ypserv
```

Expected result:

```
Active: active (running)
```

If the service is not found, inspect the installed service names:

```
systemctl list-unit-files | grep -E 'ypserv|rpcbind|nis'
```

### Step 4: Update NIS maps after creating users

Whenever you add or modify users and groups on the NIS master, update the maps.

```
sudo make -C /var/yp
```

Alternatively, use the package-provided Makefile from its directory:

```
cd /var/yp
sudo make
```

This regenerates the NIS maps.

Remember: Creating a Linux user alone does not automatically update the NIS maps. You must rebuild the maps.

## 7. Configure NIS Client

Now move to the second Linux machine.

### Step 1: Install NIS client packages

```
sudo apt update
sudo apt install nis -y
```

### Step 2: Configure the NIS domain

```
sudo nano /etc/defaultdomain
```

Add:

```
labnis
```

Set the active domain:

```
sudo domainname labnis
```

Verify:

```
domainname
```

### Step 3: Configure the NIS server address

Open:

```
sudo nano /etc/yp.conf
```

Add:

```
domain labnis server 192.168.1.10
```

Replace `192.168.1.10` with your actual NIS server IP.

This tells the client to obtain NIS information from the specified server.

### Step 4: Configure Name Service Switch

Open:

```
sudo nano /etc/nsswitch.conf
```

Find the following entries:

```
passwd:
group:
shadow:
```

Configure them to include NIS:

```
passwd:         files systemd nis
group:          files systemd nis
shadow:         files nis
```

The exact existing entries may differ between Ubuntu installations. Preserve other required sources, such as `systemd`, rather than blindly replacing the entire file.

What is `/etc/nsswitch.conf`?

NSS stands for Name Service Switch.

It tells Linux where to obtain system information such as:

- User accounts.
- Group information.
- Hostname information.
- Network services.

For example:

```
passwd: files systemd nis
```

means Linux checks local files, systemd-related account information and then NIS, according to the NSS lookup rules.

### Step 5: Start NIS client services

```
sudo systemctl restart rpcbind
sudo systemctl restart ypbind
```

Check:

```
sudo systemctl status ypbind
```

Verify the NIS binding:

```
ypwhich
```

Expected output:

```
nis-server
```

Or the server's hostname/IP, depending on the system configuration.

### Step 6: Verify NIS user information

Execute:

```
ypcat passwd
```

This displays the user account entries available through the NIS password map.

Search for the user:

```
ypmatch nisuser passwd.byname
```

Expected output should contain the `nisuser` account entry.

Also execute:

```
getent passwd nisuser
```

If everything is configured properly, the client should return the centrally managed user information.

### Step 7: Demonstrate NIS authentication

On the client, try:

```
su - nisuser
```

Enter the password configured for `nisuser` on the server.

If the NIS client, NSS and PAM authentication are correctly configured, you should get the remote user's shell.

Verify:

```
whoami
```

Expected:

```
nisuser
```

You can also execute:

```
hostname
```

This should display the client machine's hostname, while the account information came from the NIS server.

[PPT - Network Information System (NIS) PowerPoint Presentation, free download - ID:6036441](https://images.openai.com/static-rsc-4/hwJYYhVWDV2SGCp70uNFQ68upMebKbB8ssnkMLeSxz3Y-QAyEv_N0b4bU4nr1dZ6vMtIuvGTgaurBfyxHCzfbjZ5cH4olhT93b1p89PZk_d8UG_g7DX1rneclgiAojqaa6Bgsj6RfZc-ZKWIWPwY2FAHJIn7icxxDPJUq-p_0_c?purpose=inline)

[slideserve.com](https://www.slideserve.com/emanuele-yadiel/network-information-system-nis?utm_source=chatgpt.com)

NIS demonstration

What have we demonstrated?

- Centralized user account management.
- NIS database generation.
- NIS client-server communication.
- Retrieval of user information from the server.
- Remote account authentication.

## 8. Important NIS commands

| Command                          | Purpose                         |
| -------------------------------- | ------------------------------- |
| `domainname`                     | Display NIS domain              |
| `sudo domainname labnis`         | Set NIS domain                  |
| `ypinit -m`                      | Initialize NIS master           |
| `ypwhich`                        | Display NIS server              |
| `ypcat passwd`                   | Display NIS password map        |
| `ypcat group`                    | Display NIS group map           |
| `ypmatch username passwd.byname` | Search for a user               |
| `yptest`                         | Test NIS functionality          |
| `make -C /var/yp`                | Rebuild NIS maps                |
| `rpcinfo -p`                     | Display registered RPC services |
| `getent passwd nisuser`          | Retrieve account through NSS    |

# PART B — NFS SERVER

## 9. Aim

To install, configure and demonstrate an NFS Server on Ubuntu Linux for sharing directories and files between multiple Linux systems over a network.

## 10. What is NFS?

NFS (Network File System) is a distributed file system protocol that allows users to access files and directories located on another computer over a network.

It was developed by Sun Microsystems.

NFS makes remote directories appear as if they are part of the local filesystem.

For example:

Suppose a college laboratory has:

- One central Linux server.
- Ten Linux client machines.
- A common directory containing study materials.

Instead of copying the same files to all ten computers, the administrator can create a shared directory on the server and mount it on all client machines.

Every authorized client can access the shared directory.

[NFS Server and client configuration](https://images.openai.com/static-rsc-4/6pNokIIe-w69AiWoUGU9WsT5Ch1b75_OaTTME-icosUT92ozHYBEi176Ea1ltqIkh1iaECpdg2W1Db1yw8ZjTIJnKZkv2fDTgu5vmwf1fNPSUKKWQGNlgukTrkIYxK1VpzyLiJxePyS3Rx22yp7A94Jc0t_zt53J6gUUWaBeuuo?purpose=inline)

[blog.cloudnloud.com](https://blog.cloudnloud.com/nfs-server-and-client-configuration?utm_source=chatgpt.com)

### Important characteristics of NFS

| Property                   | Description                         |
| -------------------------- | ----------------------------------- |
| Full form                  | Network File System                 |
| Developed by               | Sun Microsystems                    |
| OSI layer                  | Application layer                   |
| Architecture               | Client-server                       |
| Transport                  | TCP, and UDP in some configurations |
| Default NFSv4 port         | TCP 2049                            |
| Purpose                    | Remote file and directory sharing   |
| Main configuration         | `/etc/exports`                      |
| Client mount configuration | `/etc/fstab`                        |

### How NFS works

1. The server creates a directory to share.
2. The server configures the directory in `/etc/exports`.
3. The NFS server exports the directory.
4. The client connects to the server.
5. The client mounts the exported directory.
6. The remote directory appears in the client's filesystem.
7. The client can read or write files depending on the export permissions.

[🌐 Network File System (NFS):. How Distributed Systems Make Remote… | by Astitva Arya | Jan, 2026 | Medium](https://images.openai.com/static-rsc-4/7I-iRr7q4Cy08dZaAA5ocDZwnW8ycEs9RqaiWXew-GogR1hEu6yiK0urst5s8ijCIU6L1J28xZXgthZ-1VojwH8rxmiiAwRASGwpBJNtc-KI0F7VdJApTtQheUcVwMtbKLZs2M0qvLK7fASaACCRKJebmYR-NrOPYCrpgBo3oN8?purpose=inline)

[medium.com](https://medium.com/%40astitvaarya9589/network-file-system-nfs-48df2a3d77a7?utm_source=chatgpt.com)

## 11. NFS architecture

NFS consists of two major components.

### NFS Server

- Stores the original files.
- Shares directories with clients.
- Controls client access.
- Defines read-only and read-write permissions.

### NFS Client

- Connects to the NFS server.
- Mounts the remote directory.
- Accesses shared files through the local filesystem.

Important concept: What is mounting?

Mounting means attaching a filesystem or remote directory to a particular directory (mount point) in the Linux filesystem hierarchy.

For example:

```
Server shared directory:
    /srv/nfs/shared

Client mount point:
    /mnt/nfs
```

After mounting, accessing `/mnt/nfs` on the client gives access to the server's `/srv/nfs/shared` directory.

## 12. Requirements

We will use the following lab configuration:

| Component        | Role       | Example IP        |
| ---------------- | ---------- | ----------------- |
| Machine 1        | NFS Server | 192.168.1.10      |
| Machine 2        | NFS Client | 192.168.1.20      |
| Shared directory | Server     | `/srv/nfs/shared` |
| Mount point      | Client     | `/mnt/nfs`        |
| Protocol         | NFSv4      | TCP               |
| Default port     | 2049       | TCP               |

You can also perform this demonstration using two Ubuntu virtual machines.

## 13. Installation of NFS Server

Perform these steps on the server machine.

### Step 1: Update package repositories

```
sudo apt update
```

### Step 2: Install NFS server

```
sudo apt install nfs-kernel-server -y
```

This installs the Linux NFS server components.

### Step 3: Verify installation

```
dpkg -l | grep nfs
```

### Step 4: Start and enable NFS server

```
sudo systemctl start nfs-kernel-server
```

Enable automatic startup:

```
sudo systemctl enable nfs-kernel-server
```

Check the status:

```
sudo systemctl status nfs-kernel-server
```

Expected:

```
Active: active (exited)
```

On Ubuntu, this service can show `active (exited)` because the systemd unit performs initialization and starts or manages the kernel NFS services. This is not necessarily an error.

## 14. Configure NFS Server

### Step 1: Create a shared directory

We will create a directory named `shared`.

```
sudo mkdir -p /srv/nfs/shared
```

### Step 2: Set directory permissions

For a simple lab demonstration:

```
sudo chown nobody:nogroup /srv/nfs/shared
sudo chmod 0777 /srv/nfs/shared
```

Why use `nobody:nogroup`?

It provides a simple ownership arrangement for a shared directory in a lab environment.

Important: `chmod 777` allows all local users to read, write and execute files in that directory. It is convenient for a basic demonstration but should not be used as a general production security policy.

### Step 3: Create a sample file

```
echo "Welcome to NFS Server" | sudo tee /srv/nfs/shared/serverfile.txt
```

Verify:

```
ls -l /srv/nfs/shared
```

### Step 4: Configure NFS exports

The main NFS configuration file is:

```
/etc/exports
```

Open it:

```
sudo nano /etc/exports
```

Add the following entry:

```
/srv/nfs/shared 192.168.1.0/24(rw,sync,no_subtree_check)
```

Replace `192.168.1.0/24` with the actual client network.

### Explanation of export options

| Option             | Meaning                                                         |
| ------------------ | --------------------------------------------------------------- |
| `rw`               | Allows read and write access                                    |
| `ro`               | Allows read-only access                                         |
| `sync`             | Replies after changes are committed to stable storage           |
| `async`            | Allows replies before changes are committed; faster but riskier |
| `no_subtree_check` | Disables subtree checking                                       |
| `root_squash`      | Maps remote root requests to an unprivileged identity           |
| `no_root_squash`   | Does not map remote root to an unprivileged identity            |

Important: `root_squash` is normally enabled by default. It is a security feature that prevents remote root users from automatically obtaining root privileges on the NFS server.

Do not use `no_root_squash` just to make permissions work.

### Step 5: Apply export configuration

Execute:

```
sudo exportfs -rav
```

Explanation:

- `-r`: Re-export all directories.
- `-a`: Export all configured directories.
- `-v`: Display detailed information.

Verify:

```
sudo exportfs -v
```

You should see:

```
/srv/nfs/shared
    192.168.1.0/24(rw,sync,wdelay,hide,no_subtree_check,...)
```

The exact output may contain additional default options.

### Step 6: Restart NFS server

```
sudo systemctl restart nfs-kernel-server
```

Check:

```
sudo systemctl status nfs-kernel-server
```

### Step 7: Verify NFS exports

Execute:

```
showmount -e localhost
```

Expected output:

```
Export list for localhost:
/srv/nfs/shared 192.168.1.0/24
```

This confirms that the directory is exported.

## 15. Configure NFS Client

Now switch to the client machine.

### Step 1: Install NFS client utilities

```
sudo apt update
sudo apt install nfs-common -y
```

`nfs-common` provides utilities required to mount and manage NFS filesystems.

### Step 2: Create a mount point

```
sudo mkdir -p /mnt/nfs
```

This directory will be used to access the remote shared directory.

### Step 3: Mount the NFS shared directory

Execute:

```
sudo mount -t nfs4 192.168.1.10:/srv/nfs/shared /mnt/nfs
```

Replace `192.168.1.10` with the actual NFS server IP.

Explanation:

| Parameter          | Meaning                   |
| ------------------ | ------------------------- |
| `mount`            | Mounts a filesystem       |
| `-t nfs4`          | Specifies NFS version 4   |
| `192.168.1.10`     | NFS server IP             |
| `:/srv/nfs/shared` | Exported server directory |
| `/mnt/nfs`         | Local client mount point  |

### Step 4: Verify successful mounting

Execute:

```
df -hT
```

Look for an NFS filesystem entry.

Alternatively:

```
mount | grep nfs
```

Expected output resembles:

```
192.168.1.10:/srv/nfs/shared on /mnt/nfs type nfs4
```

### Step 5: Access the shared files

Execute:

```
ls -l /mnt/nfs
```

Expected:

```
serverfile.txt
```

Read the file:

```
cat /mnt/nfs/serverfile.txt
```

Expected output:

```
Welcome to NFS Server
```

NFS mount successful

## 16. Demonstrate NFS file sharing

Now perform actual read and write operations.

### Operation 1: Create a file from the client

On the client:

```
echo "Hello from NFS Client" | sudo tee /mnt/nfs/clientfile.txt
```

### Operation 2: Verify the file on the client

```
ls -l /mnt/nfs
```

Expected:

```
clientfile.txt
serverfile.txt
```

### Operation 3: Verify the file on the server

Switch to the NFS server and execute:

```
ls -l /srv/nfs/shared
```

You should see:

```
clientfile.txt
serverfile.txt
```

Read the client-created file on the server:

```
cat /srv/nfs/shared/clientfile.txt
```

Expected:

```
Hello from NFS Client
```

This proves that the client and server are accessing the same shared directory.

### Operation 4: Create a file from the server

On the server:

```
echo "Created on NFS Server" | sudo tee /srv/nfs/shared/server2.txt
```

On the client:

```
cat /mnt/nfs/server2.txt
```

Expected:

```
Created on NFS Server
```

### Operation 5: Create a directory from the client

```
sudo mkdir /mnt/nfs/client_directory
```

Verify on the server:

```
ls -l /srv/nfs/shared
```

You should see `client_directory`.

[Exploring NFS (Network File System) Ever wondered how multiple servers can access the same files as if they were local?  That’s exactly what NFS (Network File System) enables. While learning Linux… | AASHIK H](https://images.openai.com/static-rsc-4/ANGBfy6Z2i_2pdpXEXOdQfxxnX30xEkJZfT67BHG_cVpsqRxu417uxezJOvg5wDzEY0G2Qp1TCO56z6nufvuapIFHtAlQ5aYzM9N-vYhS8q38QK7TG4lkgklhX80yQMmCR2KGnTL2IFLFdELKLiQdOZph7yqPebaRsVoUyOLzdA?purpose=inline)

[linkedin.com](https://www.linkedin.com/posts/aashikh_exploring-nfs-network-file-system-ever-activity-7408241689670156289-CiaV?utm_source=chatgpt.com)

What have we demonstrated?

- Remote directory sharing.
- Mounting a remote filesystem.
- Reading server files from the client.
- Creating client files on the server.
- Bidirectional file access.

## 17. Make NFS mounting permanent

By default, a manually mounted NFS directory may not remain mounted after a system restart.

To make the mount persistent, configure `/etc/fstab` on the client.

Open:

```
sudo nano /etc/fstab
```

Add:

```
192.168.1.10:/srv/nfs/shared /mnt/nfs nfs4 defaults,_netdev 0 0
```

Explanation:

| Field                          | Meaning                                                |
| ------------------------------ | ------------------------------------------------------ |
| `192.168.1.10:/srv/nfs/shared` | Remote NFS location                                    |
| `/mnt/nfs`                     | Client mount point                                     |
| `nfs4`                         | Filesystem type                                        |
| `defaults,_netdev`             | Default options; wait for network availability         |
| `0`                            | Disable dump                                           |
| `0`                            | Do not run filesystem check on this network filesystem |

Test the configuration:

```
sudo umount /mnt/nfs
sudo mount -a
```

Verify:

```
df -hT | grep nfs
```

If successful, the NFS share can be mounted automatically during boot, provided the network and server are available.

## 18. NFS server configuration commands

| Command                                    | Purpose                      |
| ------------------------------------------ | ---------------------------- |
| `sudo apt install nfs-kernel-server`       | Install NFS server           |
| `sudo apt install nfs-common`              | Install NFS client utilities |
| `sudo systemctl status nfs-kernel-server`  | Check server service         |
| `sudo nano /etc/exports`                   | Configure shared directories |
| `sudo exportfs -rav`                       | Reload export configuration  |
| `sudo exportfs -v`                         | Display exported directories |
| `showmount -e SERVER_IP`                   | Display available exports    |
| `sudo mount -t nfs4 SERVER:/PATH /mnt/nfs` | Mount remote directory       |
| `df -hT`                                   | Display mounted filesystems  |
| `mount \\| grep nfs`                       | Display NFS mounts           |
| `sudo umount /mnt/nfs`                     | Unmount NFS directory        |

## 19. NFS versions

NFS has evolved through several versions.

| Version | Features                                                                       |
| ------- | ------------------------------------------------------------------------------ |
| NFSv2   | Original implementation, limited file size and functionality                   |
| NFSv3   | Improved performance, larger files, stateless protocol                         |
| NFSv4   | Stateful protocol, integrated locking, improved security and firewall handling |
| NFSv4.1 | Adds sessions and parallel access capabilities                                 |
| NFSv4.2 | Adds further protocol features, including server-side copy                     |

Important viva point: We used NFSv4 because it simplifies firewall configuration by using TCP port 2049 for normal NFSv4 traffic.

## 20. Configure NFS Firewall

On the server, check:

```
sudo ufw status
```

For NFSv4, allow TCP port 2049 from the lab network:

```
sudo ufw allow from 192.168.1.0/24 to any port 2049 proto tcp
```

This permits NFSv4 connections from the specified subnet.

For a lab using NFSv3, additional RPC and mountd ports may be required, depending on the configuration.

Check the listening port:

```
sudo ss -tlnp | grep ':2049'
```

Check RPC registrations:

```
rpcinfo -p localhost
```

## 21. Troubleshooting common NFS errors

### Error 1: Mount.nfs: Connection refused

```
mount.nfs: Connection refused
```

Possible reasons:

- NFS server is not running.
- Port 2049 is blocked.
- Incorrect server IP address.

Solution:

On the server:

```
sudo systemctl restart nfs-kernel-server
sudo ss -tlnp | grep ':2049'
```

On the client:

```
ping SERVER_IP
```

### Error 2: Access denied by server

```
mount.nfs4: access denied by server
```

Possible reasons:

- Client IP is not permitted in `/etc/exports`.
- Export configuration is incorrect.
- Export changes have not been applied.

Solution:

On the server:

```
sudo nano /etc/exports
```

Check the client network entry.

Then:

```
sudo exportfs -rav
sudo exportfs -v
```

### Error 3: Permission denied while creating a file

```
Permission denied
```

Possible reasons:

- Directory does not have write permissions.
- File ownership does not permit the client user to write.
- NFS root squashing is in effect.

For the basic lab configuration:

```
sudo chown nobody:nogroup /srv/nfs/shared
sudo chmod 0777 /srv/nfs/shared
```

Remember that `0777` is a lab-only shortcut. For production, use suitable user/group ownership and restricted permissions.

### Error 4: NFS mount does not persist after reboot

Check:

```
cat /etc/fstab
```

Ensure the correct entry is present:

```
192.168.1.10:/srv/nfs/shared /mnt/nfs nfs4 defaults,_netdev 0 0
```

Test:

```
sudo mount -a
```

### Error 5: NFS client cannot see exported directories

Check exports from the client:

```
showmount -e 192.168.1.10
```

Check NFSv4 exports and the server service:

```
sudo exportfs -v
sudo systemctl status nfs-kernel-server
```

Note that `showmount` relies on the MOUNT protocol and may not fully represent NFSv4-only export visibility. A successful NFSv4 mount is the stronger test.

# PART C — NIS vs NFS and Their Integration

## 22. Difference between NIS and NFS

This is a very important viva question because both services are commonly used together in Linux networks.

| Feature                 | NIS                                    | NFS                          |
| ----------------------- | -------------------------------------- | ---------------------------- |
| Full form               | Network Information Service            | Network File System          |
| Main purpose            | Centralized user and group information | Remote file sharing          |
| Developed by            | Sun Microsystems                       | Sun Microsystems             |
| Function                | Provides identity information          | Provides filesystem access   |
| Configuration           | `/etc/yp.conf`, `/etc/nsswitch.conf`   | `/etc/exports`, `/etc/fstab` |
| Main server component   | `ypserv`                               | `nfs-kernel-server`          |
| Client component        | `ypbind`                               | `nfs-common`                 |
| Main protocol mechanism | RPC-based NIS                          | NFS protocol                 |
| Common use              | Centralized account management         | Shared directories and files |

### How NIS and NFS work together

Consider a college computer laboratory.

- NIS manages student usernames, passwords and user IDs centrally.
- NFS stores students' home directories centrally.
- Students can log in from different computers.
- Their home directories and files can be accessed from different computers.

[NIS](https://images.openai.com/static-rsc-4/iXIaopRlBu7Q_e8gD7zBMi6yPeitVZfL5TAfmofg8wswBjMXaBzhBywowOdKRnqDSDHaUNo6z9J1wEeXu8QafheJeLF7ySeVQtVl8NRnlnmKaJ0YkhbNRPerLqk__OlziPH6FEKiyUKe3zNu_4KZ0kyAHfz2quu35xRWfIZtxSs?purpose=inline)

[networxsecurity.org](https://www.networxsecurity.org/members-area/glossary/n/nis.html?utm_source=chatgpt.com)

For example:

```
                 Central Linux Server
                 --------------------
                 NIS Server
                 User: student1
                 UID: 1001
                       |
                 NFS Server
                 /home/student1
                       |
              -------------------
              |                 |
          Client 1           Client 2
          nisuser login      nisuser login
          NFS mounted        NFS mounted
              |                 |
              -------------------
                 Same user data
```

Important technical concept:

For NIS and NFS to work together correctly, the user and group IDs (UID and GID) must be consistent across the machines.

NIS provides consistent identity information, while NFS provides access to shared files.

For a full shared-home-directory setup, the administrator also needs to configure NFS exports, client mount points, permissions and login-time mounting correctly.

# PART D — Important Viva Questions

## 23. NIS viva questions

Q1. What is NIS?

NIS stands for Network Information Service. It provides centralized management of user accounts, groups and other network information across multiple Linux machines.

Q2. What was the original name of NIS?

Yellow Pages (YP).

Q3. What is the purpose of an NIS server?

It maintains centralized databases and provides user and group information to NIS clients.

Q4. What is an NIS master server?

It is the primary server that maintains and updates the original NIS maps.

Q5. What is an NIS slave server?

It maintains replicated copies of the NIS maps and provides redundancy.

Q6. What is an NIS domain?

It is a logical identifier used to group systems belonging to the same NIS administrative domain.

Q7. What is the purpose of `ypinit -m`?

It initializes an NIS master server and creates the initial NIS database maps.

Q8. What is the purpose of `ypwhich`?

It displays the NIS server to which the client is currently bound.

Q9. What is the purpose of `ypcat`?

It displays the contents of an NIS map.

Q10. What is `/etc/nsswitch.conf`?

It configures the sources Linux uses to retrieve information such as usernames, groups and hostnames.

Q11. What is `ypbind`?

It is the NIS client binding daemon that locates and binds to an NIS server.

Q12. What is `ypserv`?

It is the NIS server daemon that responds to client requests for NIS information.

Q13. What is an NIS map?

An NIS map is a database containing centrally managed information, such as user accounts and group information.

Q14. Is NIS secure?

No. Traditional NIS does not provide strong modern authentication or encryption. It should only be used in isolated lab environments or legacy systems.

Q15. What happens when a new user is added to the NIS server?

The administrator must rebuild the NIS maps using:

```
sudo make -C /var/yp
```

## 24. NFS viva questions

Q1. What is NFS?

NFS stands for Network File System. It allows computers to access remote directories over a network.

Q2. What is the purpose of an NFS server?

It shares directories and files with authorized client machines.

Q3. Which file is used to configure NFS exports?

```
/etc/exports
```

Q4. Which command is used to display exported directories?

```
sudo exportfs -v
```

Q5. What is mounting?

Mounting attaches a filesystem or remote directory to a directory in the local filesystem hierarchy.

Q6. What is a mount point?

A mount point is the local directory where a remote filesystem is attached.

Q7. Which port does NFSv4 use by default?

TCP port 2049.

Q8. What is the difference between `rw` and `ro`?

- `rw`: Allows read and write access.
- `ro`: Allows read-only access.

Q9. What is the purpose of `sync`?

It ensures that server replies are sent after the corresponding changes have been committed to stable storage.

Q10. What is root squashing?

It maps remote root-user requests to an unprivileged identity on the NFS server.

Q11. What is `/etc/fstab`?

It contains filesystem mounting configuration, including entries for automatically mounting NFS directories.

Q12. What is the difference between NFSv3 and NFSv4?

NFSv4 provides stateful operation, integrated locking and improved firewall handling compared with NFSv3.

Q13. What is the purpose of `exportfs -rav`?

It reloads the configured NFS exports and displays the operations.

Q14. What happens if the NFS server goes down?

Clients may experience blocked or failed access to the remote filesystem, depending on the mount configuration.

Q15. Can multiple clients access the same NFS directory?

Yes. Multiple authorized clients can mount and access the same exported directory, subject to permissions and file-sharing semantics.

## 25. Other important comparison questions

| Question                            | Answer                           |
| ----------------------------------- | -------------------------------- |
| NIS provides what?                  | Centralized identity information |
| NFS provides what?                  | Shared filesystem access         |
| NIS client daemon?                  | `ypbind`                         |
| NIS server daemon?                  | `ypserv`                         |
| NFS server package?                 | `nfs-kernel-server`              |
| NFS client package?                 | `nfs-common`                     |
| NIS database directory?             | `/var/yp/`                       |
| NFS export file?                    | `/etc/exports`                   |
| NIS client configuration?           | `/etc/yp.conf`                   |
| NFS persistent mount configuration? | `/etc/fstab`                     |

# PART E — Practical Examination Checklist

## 26. NIS practical checklist

## NIS server and client

Progress

0/15

Install NIS packages

Configure NIS domain name

Configure NIS master server

Configure securenets

Create NIS user

Initialize maps using ypinit -m

Start rpcbind and ypserv

Rebuild NIS maps

Install NIS on client

Configure client /etc/yp.conf

Configure /etc/nsswitch.conf

Start ypbind

Verify server using ypwhich

Verify user using ypcat and getent

Demonstrate login using NIS user

Reset NIS checklist

## 27. NFS practical checklist

## NFS server and client

Progress

0/16

Install nfs-kernel-server

Start and enable NFS service

Create shared directory

Configure ownership and permissions

Create sample server file

Configure /etc/exports

Apply exports using exportfs -rav

Verify exports using showmount

Install nfs-common on client

Create client mount point

Mount remote directory

Verify mount using df -hT

Read server file from client

Create file from client

Verify client file on server

Configure persistent mount using /etc/fstab

Reset NFS checklist

# PART F — What to write in your practical journal

## 28. NIS experiment

Aim: To install, configure and demonstrate NIS Server on Ubuntu Linux.

Software requirements:

- Ubuntu Linux.
- NIS server and client packages.
- Two Linux machines.
- TCP/IP network.

Procedure:

1. Installed the NIS package.
2. Configured the NIS domain name.
3. Configured the master server.
4. Created a user account.
5. Initialized NIS maps.
6. Started the NIS server services.
7. Configured the NIS client.
8. Updated NSS configuration.
9. Retrieved centralized user information.
10. Demonstrated login using the NIS account.

Result: NIS Server was successfully installed and configured. The NIS client retrieved centralized user information from the NIS server and demonstrated remote account authentication.

## 29. NFS experiment

Aim: To install, configure and demonstrate NFS Server on Ubuntu Linux.

Software requirements:

- Ubuntu Linux.
- NFS server and client packages.
- Two Linux machines.
- TCP/IP network.

Procedure:

1. Installed the NFS server package.
2. Started and enabled the NFS service.
3. Created a shared directory.
4. Configured the `/etc/exports` file.
5. Exported the shared directory.
6. Installed NFS client utilities.
7. Created a mount point on the client.
8. Mounted the remote directory.
9. Performed read and write operations.
10. Verified file sharing between the client and server.

Result: NFS Server was successfully installed and configured. The client mounted the shared directory and performed file operations on the remote server.

# 30. Final revision: Commands you must remember

## NIS — Most important commands

```
sudo apt update
sudo apt install nis -y

sudo domainname labnis

sudo nano /etc/default/nis
sudo nano /etc/ypserv.securenets

sudo adduser nisuser

sudo ypinit -m

sudo systemctl restart rpcbind
sudo systemctl restart ypserv

sudo make -C /var/yp

ypwhich
ypcat passwd
ypmatch nisuser passwd.byname
getent passwd nisuser
```

## NIS — Client commands

```
sudo apt install nis -y

sudo nano /etc/defaultdomain
sudo nano /etc/yp.conf
sudo nano /etc/nsswitch.conf

sudo domainname labnis

sudo systemctl restart rpcbind
sudo systemctl restart ypbind

ypwhich
ypcat passwd
getent passwd nisuser
su - nisuser
```

## NFS — Server commands

```
sudo apt update
sudo apt install nfs-kernel-server -y

sudo mkdir -p /srv/nfs/shared

sudo chown nobody:nogroup /srv/nfs/shared
sudo chmod 0777 /srv/nfs/shared

sudo nano /etc/exports

sudo exportfs -rav
sudo exportfs -v

sudo systemctl restart nfs-kernel-server

showmount -e localhost
```

## NFS — Client commands

```
sudo apt install nfs-common -y

sudo mkdir -p /mnt/nfs

sudo mount -t nfs4 \
192.168.1.10:/srv/nfs/shared /mnt/nfs

df -hT
ls /mnt/nfs

echo "Hello" | sudo tee /mnt/nfs/test.txt

sudo nano /etc/fstab

sudo umount /mnt/nfs
sudo mount -a
```

&#x20;Copy revision commands

## 31. My recommendation for your lab examination

For this experiment, use two Ubuntu machines or two Ubuntu virtual machines.

Demonstrate the following four things to your examiner:

1. NIS: Create a user on the server and retrieve that user's information from the client using `getent passwd`.
2. NIS authentication: Log in as the centrally managed user on the client.
3. NFS: Mount the server's shared directory on the client and read a file created on the server.
4. NFS bidirectional sharing: Create a file on the client and verify that it appears on the server.

These four demonstrations establish that both services are actually functioning, rather than merely showing that the packages are installed.

One important practical distinction: NIS handles centralized identity information; NFS handles shared filesystem access. Neither replaces the other.

Also, NIS is a legacy insecure service. Keep the experiment on an isolated lab network, and avoid exposing its RPC services to public networks.
