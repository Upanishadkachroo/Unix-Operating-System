# Practical: Installation, Configuration and Demonstration of FTP Server

Linux practical examination

Ubuntu 24.04 **LTS**

## 1. Aim

To install, configure and demonstrate an **FTP** (File Transfer Protocol) Server on Ubuntu Linux and perform file transfer operations between an **FTP** client and server.

## 2. What is FTP?

**FTP** (File Transfer Protocol) is an application-layer protocol used to transfer files between two computers over a **TCP**/IP network.

It follows a client-server architecture:

- **FTP** Server: Stores files and accepts file transfer requests.
- **FTP** Client: Connects to the server to upload, download, rename and manage files.
- Network: Provides communication between the client and server.

**FTP** supports two major operations:

## Download: Transfer files from the server to the client.

## Upload: Transfer files from the client to the server.

Other operations include:

- Listing directories.
- Creating directories.
- Deleting files.
- Renaming files.
- Changing directories.

[**FTP**(File Transfer Protocal)란?](https://images.openai.com/static-rsc-4/iuVI1kjvm15CaF988uBU4A_sx_Vz1wOtY8X2NMYsS_dnba7xhSjOtmBj4OYaTIFK6i8Rrm5dFzJyYTr97h665_XmQSYdLVZfVDDSCJZQ7uf5aaAw19kGiTWmxyTA-w8mNuGiIakLx_Pi4Gb4WjdpKUqpO1hKQb9Wgic9VyIkOpQ?purpose=inline)

[xn--os5ba3q.com](https://xn--os5ba3q.com/**100**?utm_source=chatgpt.com)

### Important characteristics

| Property                     | Description                      |
| ---------------------------- | -------------------------------- |
| Full form                    | File Transfer Protocol           |
| OSI layer                    | Application layer (Layer 7)      |
| Transport protocol           | TCP                              |
| Default control port         | 21                               |
| Active mode data connection  | Traditionally server TCP port 20 |
| Passive mode data connection | Server-selected port range       |
| Architecture                 | Client-server                    |
| Authentication               | Username and password            |
| Encryption                   | None in standard FTP             |

Important examination point: Standard **FTP** does not encrypt usernames, passwords or file contents. For secure file transfers, **SFTP** or **FTPS** should be used.

## 3. How FTP works

**FTP** uses two separate connections:

1\. Control connection

- Uses **TCP** port 21 by default.
- Carries commands and responses between client and server.
- Remains open during the **FTP** session.

2\. Data connection

- Transfers actual files and directory listings.
- Uses different connection arrangements depending on active or passive mode.

[**FTP** **101** series part 1: Active vs passive connection](https://images.openai.com/static-rsc-4/61ezkEhMCBQOUygYMyHGRbOXCD3MBAy-WlieUHqNmULcQ063fwcVy6xlFGbLD7GX_bVmGcgc_43zbEEvZVvrueTr85E5LWRN72sgkHEzb-S9RSPt9pHK7d6av_MZOUbVxmMdzgU2LI9O5byQ8G-PaFRSp-uWCIt-UqjQ3rHl_98?purpose=inline)

[ftpgrid.com](https://ftpgrid.com/tutorials/ftp-**101**-active-vs-passive-connections/?utm_source=chatgpt.com)

### Active mode vs Passive mode

| Feature                | Active FTP                            | Passive FTP                           |
| ---------------------- | ------------------------------------- | ------------------------------------- |
| Control connection     | Client to server port 21              | Client to server port 21              |
| Data connection        | Server initiates connection to client | Client initiates connection to server |
| Server data port       | Traditionally 20                      | Server-selected port                  |
| Firewall compatibility | Can be difficult                      | Generally easier                      |
| Common usage           | Legacy environments                   | Modern networks                       |

Remember: In passive **FTP**, the server tells the client which port to use for the data connection. This is why a passive port range must often be configured in the server firewall.

## 4. Requirements

For this practical, we will use:

| Component        | Software                            |
| ---------------- | ----------------------------------- |
| Operating system | Ubuntu 24.04                        |
| FTP Server       | vsftpd                              |
| FTP Client       | inetutils-ftp or another FTP client |
| Protocol         | TCP                                 |
| Control port     | 21                                  |
| Server IP        | Example: 192.168.1.10               |

### What is vsftpd?

`vsftpd` stands for Very Secure **FTP** Daemon.

It is a popular, lightweight **FTP** server for Linux systems.

Features:

- Supports local Linux user authentication.
- Supports anonymous **FTP** access.
- Supports active and passive **FTP**.
- Supports upload and download operations.
- Supports configurable access permissions.
- Supports **SSL**/**TLS** when configured for **FTPS**.

We will use local-user authentication and passive **FTP** for the demonstration.

## 5. Installation of FTP Server

We will install `vsftpd` on Ubuntu 24.04.

### Step 1: Update package repositories

Open the terminal:

``` sudo apt update ```

This refreshes the package repository information.

### Step 2: Install vsftpd

``` sudo apt install vsftpd -y ```

This installs the **FTP** server software.

### Step 3: Install FTP client

``` sudo apt install inetutils-ftp -y ```

This installs an **FTP** command-line client.

### Step 4: Verify installation

Check the version:

``` vsftpd -v ```

Check the installed package:

``` dpkg -l | grep vsftpd ```

Check the **FTP** client:

``` ftp ```

You should see an **FTP** prompt:

``` ftp> ```

Type:

``` quit ```

to exit.

## 6. Start and configure FTP Server

### Step 1: Start the FTP service

``` sudo systemctl start vsftpd ```

Enable it to start automatically during boot:

``` sudo systemctl enable vsftpd ```

Check its status:

``` sudo systemctl status vsftpd ```

Expected output:

``` Active: active (running) ```

Press `q` to exit.

### Step 2: Understand the configuration file

The main **FTP** server configuration file is:

``` /etc/vsftpd.conf ```

Open it:

``` sudo nano /etc/vsftpd.conf ```

This file controls **FTP** server behaviour, authentication, permissions, anonymous access and data connections.

### Step 3: Configure FTP authentication and permissions

Find the following settings and ensure they are configured as shown.

``` # Disable anonymous access anonymous_enable=NO

# Allow local Linux users to log in

local_enable=**YES**

# Allow file upload and modification

write_enable=**YES**

# Set default file permissions

local_umask=**022**

# Restrict local users to their home directories

chroot_local_user=**YES**

# Enable passive FTP mode

pasv_enable=**YES**

# Passive FTP port range

pasv_min_port=**40000** pasv_max_port=**40100** ```

If a setting already exists, edit it rather than adding conflicting duplicate entries.

Explanation of important configuration directives:

| Directive               | Meaning                                         |
| ----------------------- | ----------------------------------------------- |
| `anonymous_enable=NO`   | Disables anonymous login                        |
| `local_enable=YES`      | Allows Linux users to log in                    |
| `write_enable=YES`      | Enables FTP write operations                    |
| `local_umask=022`       | Controls default file permissions               |
| `chroot_local_user=YES` | Restricts local users to their home directories |
| `pasv_enable=YES`       | Enables passive FTP                             |
| `pasv_min_port=40000`   | Minimum passive data port                       |
| `pasv_max_port=40100`   | Maximum passive data port                       |

What is chroot?

Chroot stands for change root.

It restricts an **FTP** user to a designated directory tree, preventing the user from navigating outside that directory through the **FTP** session.

This is useful for restricting access to server files.

### Step 4: Create an FTP user and directory

We will create a dedicated user called `ftpuser`.

``` sudo adduser ftpuser ```

Enter a password when prompted.

Now prepare the directory structure:

``` sudo mkdir -p /home/ftpuser/ftp/upload ```

Set ownership and permissions:

``` sudo chown root:root /home/ftpuser/ftp sudo chmod **755** /home/ftpuser/ftp

sudo chown ftpuser:ftpuser /home/ftpuser/ftp/upload sudo chmod **755** /home/ftpuser/ftp/upload ```

Configure the user's **FTP** starting directory:

``` sudo usermod -d /home/ftpuser/ftp ftpuser ```

The directory structure will look like this:

```
/home/ftpuser/
    |
    +---- ftp/
    |
    +---- upload/
```

The `ftp` directory is owned by root, while `upload` is writable by `ftpuser`.

This is important because vsftpd normally prevents a chrooted user from having a writable chroot root directory.

### Step 5: Restart FTP server

After modifying the configuration:

``` sudo systemctl restart vsftpd ```

Check the status:

``` sudo systemctl status vsftpd ```

### Step 6: Verify that FTP is listening on port 21

Execute:

``` sudo ss -tlnp | grep ':21' ```

Expected output will resemble:

``` **LISTEN** 0 32 0.0.0.0:21 0.0.0.0:* ```

This indicates that the **FTP** server is listening on **TCP** port 21.

## 7. Configure Firewall

If **UFW** is enabled, allow **FTP** control connections and passive data connections.

Check firewall status:

``` sudo ufw status ```

Allow the **FTP** control port:

``` sudo ufw allow 21/tcp ```

Allow the passive port range:

``` sudo ufw allow **40000**:**40100**/tcp ```

Check the rules:

``` sudo ufw status ```

For a real lab network, you can restrict these rules to your lab subnet instead of exposing the service to every network.

Why open passive ports?

The **FTP** client initially connects to port 21. During file transfers and directory listings in passive mode, it also connects to a server-selected port from the configured passive range.

If these ports are blocked, login may succeed while file listing or file transfer fails.

## 8. Demonstration of FTP Server

Now we will demonstrate the actual file transfer operations.

There are two ways to perform the demonstration.

### Method A: FTP client and server on the same machine

This is the easiest method if you have only one laptop.

Terminal 1 – Server

Check whether the **FTP** service is running:

``` sudo systemctl status vsftpd ```

Check port 21:

``` sudo ss -tlnp | grep ':21' ```

Create a sample file in your local working directory:

``` echo *Hello from **FTP** Client* > clientfile.txt ```

Terminal 2 – **FTP** Client

Connect to the local **FTP** server:

``` ftp localhost ```

Expected output:

``` Connected to localhost. **220** (vsFTPd 3.0.5) Name (localhost:username): ```

Enter:

``` ftpuser ```

Then enter the password created earlier.

You should see:

``` **230** Login successful. ftp> ```

**FTP** connection established

### Method B: FTP client and server on two different machines

This demonstrates actual network-based file transfer.

Suppose:

| Machine   | Role       | Example IP   |
| --------- | ---------- | ------------ |
| Machine 1 | FTP Server | 192.168.1.10 |
| Machine 2 | FTP Client | 192.168.1.20 |

On the server:

Find the server IP:

``` hostname -I ```

Verify the **FTP** service:

``` sudo systemctl status vsftpd ```

On the client:

Install the **FTP** client:

``` sudo apt update sudo apt install inetutils-ftp -y ```

Connect to the server:

``` ftp **192**.**168**.1.10 ```

Enter the username:

``` ftpuser ```

Enter the password.

If authentication succeeds:

``` **230** Login successful. ftp> ```

You are now connected to the remote **FTP** server.

[The “ftp” Command in Linux \[14 Practical Examples\]](https://images.openai.com/static-rsc-4/KrA9zQbTqGcwFNkhJtURAkkniDVhum3rjhuqzveAt33bl2EeNwBVBnVi6bpqvtJy8fEMwBTtfrFairbFIw82xCU-XjmUbUSDdKDHhcoMrGpdLyJaRDontqMX84MOl4BZUs_iubLX9CptzGLrGm0ZgbnY9-7u4TTLG1ErI0K3fxM?purpose=inline)

[linuxsimply.com](https://linuxsimply.com/ftp-command-in-linux/?utm_source=chatgpt.com)

## 9. Perform FTP file transfer operations

Once you are logged in, the **FTP** prompt will look like:

``` ftp> ```

Now perform the following commands.

### Operation 1: Display current remote directory

``` pwd ```

Expected output:

``` **257** */* is the current directory ```

The `/` represents the root of the **FTP** user's restricted directory, not the actual Linux filesystem root.

### Operation 2: List files and directories

``` ls ```

This displays files and folders available on the **FTP** server.

Initially, you should see:

``` upload ```

### Operation 3: Change remote directory

``` cd upload ```

This changes the current remote directory to `upload`.

### Operation 4: Upload a file from client to server

First, create a sample file on the client machine, outside the **FTP** prompt:

``` echo *Hello from **FTP** Client* > clientfile.txt ```

Inside the **FTP** session:

``` put clientfile.txt ```

Expected output:

``` local: clientfile.txt remote: clientfile.txt **226** Transfer complete. ```

File uploaded successfully

The file is now stored on the **FTP** server in:

``` /home/ftpuser/ftp/upload/clientfile.txt ```

### Operation 5: Verify uploaded file

Inside **FTP**:

``` ls ```

Expected output:

``` clientfile.txt ```

You can also verify the contents:

``` get clientfile.txt ```

This downloads the file to the client.

Exit the **FTP** session:

``` bye ```

Now, on the server, verify the uploaded file:

``` sudo cat /home/ftpuser/ftp/upload/clientfile.txt ```

Expected output:

``` Hello from **FTP** Client ```

### Operation 6: Download a file from server to client

First, create a sample file on the server:

``` sudo -u ftpuser bash -c 'echo *Hello from **FTP** Server* > /home/ftpuser/ftp/upload/serverfile.txt' ```

Connect again:

``` ftp localhost ```

Log in as `ftpuser`.

Then:

``` cd upload ls get serverfile.txt ```

Expected output:

``` **226** Transfer complete. ```

Exit:

``` bye ```

Verify the downloaded file on the client:

``` cat serverfile.txt ```

Expected output:

``` Hello from **FTP** Server ```

[The “ftp” Command in Linux \[14 Practical Examples\]](https://images.openai.com/static-rsc-4/bvY_qnEoeSBpN-pOrklGrljTmEB1YSMusiuj7H6MOJMgtGNPgN9DkS7J6h6g9351AdA58Yim8Iy081SKt8e7Te8wDMh70RreQbsEFNvFVfaXBckVt1iXR5Xz59JzJbkwndW0v6UcY-0QnJCzmu3d4QeGZnvELB5rylGeyS-Qqk0?purpose=inline)

[linuxsimply.com](https://linuxsimply.com/ftp-command-in-linux/?utm_source=chatgpt.com)

### Operation 7: Create a directory on the server

Inside **FTP**:

``` mkdir practical ```

Verify:

``` ls ```

### Operation 8: Rename a file

``` rename clientfile.txt demo.txt ```

### Operation 9: Delete a file

``` delete demo.txt ```

### Operation 10: Exit FTP

``` bye ```

You have now demonstrated both upload and download, along with basic remote file management.

## 10. Important FTP commands for practical examination

| FTP command       | Purpose                                           |
| ----------------- | ------------------------------------------------- |
| `ftp SERVER_IP`   | Connect to FTP server                             |
| `pwd`             | Display remote working directory                  |
| `ls`              | List remote files                                 |
| `cd directory`    | Change remote directory                           |
| `lcd directory`   | Change local client directory                     |
| `put filename`    | Upload a file                                     |
| `get filename`    | Download a file                                   |
| `mput files`      | Upload multiple files                             |
| `mget files`      | Download multiple files                           |
| `mkdir directory` | Create remote directory                           |
| `rmdir directory` | Remove remote directory                           |
| `delete filename` | Delete remote file                                |
| `rename old new`  | Rename remote file                                |
| `binary`          | Switch to binary transfer mode                    |
| `ascii`           | Switch to ASCII transfer mode                     |
| `passive`         | Toggle passive transfer mode in supported clients |
| `bye`             | Disconnect from FTP server                        |

Important: For images, **ZIP** files, executables and other non-text files, use binary mode:

``` binary ```

For ordinary text files, **ASCII** mode can be used:

``` ascii ```

**FTP** clients may use different default transfer modes and passive-mode settings. If a directory listing or file transfer fails, check the client's passive-mode setting.

## 11. Active and Passive FTP in practical terms

This is a common viva question.

Active **FTP**

[File Transfer Protocol (**FTP**) - Scaler Topics](https://images.openai.com/static-rsc-4/2h_daurG4WlpP2Y4cjyle9kUTKboGfwEC9tu0qf13XeuHkUmPmhg5QKlwB4Byi0HVv_RKm-mIGfThYtVvwfDFt4J77_90YF9tVszFExtd4dMzc6P32fWIbBsY8mj5cQR9fVUpdifV473Gz1C0aHjmSTUnk4XnLgLSR3MKq2DsGY?purpose=inline)

[scaler.com](https://[www.scaler.com/topics/computer-network/file-transfer-protocol/?utm_source=chatgpt.com](https://www.scaler.com/topics/computer-network/file-transfer-protocol/?utm_source=chatgpt.com))

## Client connects to server TCP port 21.

## Client tells the server which client-side port to use for data. ## Server initiates the data connection from its TCP port 20 to the client.

   Passive **FTP**

   [File Transfer Protocol Explained - **IPXO**](https://images.openai.com/static-rsc-4/KBHsmALZ4XTR86aq5FAyssB0EV8hh2uqbtoRmDelOZHo6HpyBGB4VHfXNSzSW9U5zlz8wEfVuxN9IiN2WSxOj8pC0UdTejknOSq39cFbaIzGNJQPEnRXOBR0thUbZAdDvk49FzO9QFjqPB3HYOXEeZPyoU9m3bml2WhykHOxx40?purpose=inline)

[ipxo.com](https://[www.ipxo.com/blog/what-is-ftp/?utm_source=chatgpt.com](https://www.ipxo.com/blog/what-is-ftp/?utm_source=chatgpt.com)) ## Client connects to server TCP port 21. ## Client sends a PASV or EPSV request. ## Server provides a data port. ## Client initiates the data connection to that server port.

Why do we configure passive **FTP**?

Most modern client machines are behind **NAT** routers and firewalls. Passive **FTP** allows the client to initiate both connections, which generally makes communication easier.

For our practical, we configured:

``` pasv_enable=**YES** pasv_min_port=**40000** pasv_max_port=**40100** ```

## 12. Important vsftpd configuration directives

An examiner may ask you to explain the server configuration file.

| Configuration       | Purpose                                 |
| ------------------- | --------------------------------------- |
| `anonymous_enable`  | Controls anonymous FTP access           |
| `local_enable`      | Allows local Linux users                |
| `write_enable`      | Enables write operations                |
| `local_umask`       | Sets default permission mask            |
| `chroot_local_user` | Restricts users to their home directory |
| `pasv_enable`       | Enables passive FTP                     |
| `pasv_min_port`     | Minimum passive port                    |
| `pasv_max_port`     | Maximum passive port                    |
| `listen`            | Controls standalone IPv4 listening      |
| `listen_ipv6`       | Controls IPv6 listening                 |
| `userlist_enable`   | Enables user-list restrictions          |
| `ssl_enable`        | Enables SSL/TLS support                 |

To inspect the configuration:

``` sudo cat /etc/vsftpd.conf ```

To restart after changing it:

``` sudo systemctl restart vsftpd ```

To inspect logs:

``` sudo journalctl -u vsftpd -n 30 --no-pager ```

## 13. Troubleshooting common errors

### Error 1: Connection refused

``` ftp: connect: Connection refused ```

Reasons:

- **FTP** service is not running.
- Port 21 is not listening.
- **FTP** service failed to start.

Solution:

``` sudo systemctl status vsftpd sudo systemctl restart vsftpd sudo ss -tlnp | grep ':21' ```

### Error 2: Login incorrect

``` **530** Login incorrect. ```

Reasons:

- Incorrect username or password.
- User account does not exist.
- User is blocked by **FTP** access restrictions.

Solution:

``` id ftpuser sudo passwd ftpuser ```

Also inspect:

``` sudo cat /etc/ftpusers ```

This file commonly lists users prohibited from **FTP** login.

### Error 3: Permission denied while uploading

``` **550** Permission denied. ```

Reason: The **FTP** user does not have write permissions in the target directory.

Solution:

``` sudo chown ftpuser:ftpuser /home/ftpuser/ftp/upload sudo chmod **755** /home/ftpuser/ftp/upload ```

Make sure you have changed into the upload directory:

``` cd upload ```

### Error 4: 500 OOPS: refusing to run with writable root inside chroot

Reason: The chroot root directory is writable by the **FTP** user.

Solution: Keep the **FTP** root directory owned by root and provide a separate writable upload directory.

``` sudo chown root:root /home/ftpuser/ftp sudo chmod **755** /home/ftpuser/ftp

sudo chown ftpuser:ftpuser /home/ftpuser/ftp/upload ```

### Error 5: Login works but file transfer fails

Possible reasons:

- Passive ports are blocked.
- Client and server have incompatible transfer modes.
- Firewall blocks the data connection.
- Incorrect passive IP configuration when **NAT** is involved.

Solution:

Check the passive port settings:

``` sudo grep -E 'pasv_enable|pasv_min_port|pasv_max_port' /etc/vsftpd.conf ```

Check the firewall:

``` sudo ufw status ```

Allow the configured passive port range if required:

``` sudo ufw allow **40000**:**40100**/tcp ```

## 14. FTP vs SFTP vs FTPS

This is one of the most important viva topics.

| Feature                  | FTP                    | FTPS                            | SFTP                            |
| ------------------------ | ---------------------- | ------------------------------- | ------------------------------- |
| Full form                | File Transfer Protocol | FTP Secure                      | SSH File Transfer Protocol      |
| Security                 | No encryption          | TLS/SSL encryption              | SSH encryption                  |
| Default port             | 21                     | 21 (explicit FTPS)              | 22                              |
| Transport                | TCP                    | TCP                             | SSH over TCP                    |
| Authentication           | Username/password      | Username/password, certificates | Password or SSH keys            |
| Data encryption          | No                     | Yes                             | Yes                             |
| Separate data connection | Yes                    | Yes                             | No separate FTP data connection |

Important distinction: **SFTP** is not simply secure **FTP**. It is a separate file-transfer protocol that operates over **SSH**.

## 15. Advantages and disadvantages of FTP

Advantages

## Supports transferring large files.

## Supports uploading and downloading. ## Allows directory management. ## Supports multiple users. ## Can transfer files between different operating systems. ## Supports active and passive modes.

Disadvantages

## Standard FTP does not encrypt data.

## Username and password are transmitted in plaintext. ## Requires separate control and data connections. ## Firewall configuration can be complicated. ## Standard FTP is vulnerable to network eavesdropping.

## 16. Important viva questions and answers

These are questions you should prepare before your examination.

Q1. What is **FTP**?

**FTP** stands for File Transfer Protocol. It is an application-layer protocol used to transfer files between computers over a **TCP**/IP network.

Q2. Which port does **FTP** use?

**TCP** port 21 for the control connection.

Q3. Which software did you use to configure the **FTP** server?

I used vsftpd (Very Secure **FTP** Daemon) on Ubuntu Linux.

Q4. What is the full form of vsftpd?

Very Secure **FTP** Daemon.

Q5. What is the difference between **FTP** client and server?

- **FTP** client initiates connections and requests file operations.
- **FTP** server accepts connections and provides file transfer services.

Q6. Does **FTP** use **TCP** or **UDP**?

**FTP** uses **TCP** because it requires reliable, connection-oriented communication.

Q7. What are the two connections used by **FTP**?

## Control connection.

## Data connection.

Q8. What is the purpose of port 21?

It handles **FTP** control commands and server responses.

Q9. What is port 20 used for?

Traditionally, **TCP** port 20 is used by the server for data connections in active **FTP**.

**Q10**. What is anonymous **FTP**?

Anonymous **FTP** allows users to access an **FTP** server without using an individual registered account, depending on server configuration.

**Q11**. What is the purpose of `/etc/vsftpd.conf`?

It is the main configuration file for the vsftpd server.

**Q12**. What is the purpose of `write_enable=**YES**`?

It enables **FTP** write operations such as uploading, deleting, renaming and creating directories, subject to permissions.

**Q13**. What is the purpose of `local_enable=**YES**`?

It allows local Linux users to authenticate to the **FTP** server.

**Q14**. What is chroot?

Chroot restricts a user to a specified directory tree, preventing access to files outside that tree through the **FTP** session.

**Q15**. What is the difference between upload and download?

- Upload: Client sends a file to the server.
- Download: Client receives a file from the server.

**Q16**. What is passive **FTP**?

In passive **FTP**, the client initiates both the control and data connections. The server provides a port for the data connection.

**Q17**. What is the difference between **FTP** and **SFTP**?

**FTP** is a traditional file-transfer protocol without encryption, whereas **SFTP** transfers files securely over **SSH**.

**Q18**. How do you check whether the **FTP** server is running?

``` sudo systemctl status vsftpd ```

**Q19**. How do you check whether port 21 is listening?

``` sudo ss -tlnp | grep ':21' ```

**Q20**. How do you upload a file?

``` put filename ```

**Q21**. How do you download a file?

``` get filename ```

**Q22**. How do you terminate an **FTP** session?

``` bye ```

**Q23**. What is the difference between **ASCII** and binary transfer modes?

- **ASCII** mode is used for text files and may perform newline conversion.
- Binary mode transfers file contents without text conversion.

**Q24**. Can multiple clients connect to one **FTP** server?

Yes. An **FTP** server can handle multiple client connections, subject to its configuration and system resources.

**Q25**. Why is **FTP** considered insecure?

Because standard **FTP** transmits credentials and file contents without encryption.

## 17. Practical examination procedure

Follow this sequence during your lab examination.

## FTP practical checklist

Practical progress

0/21 completed

Update Ubuntu repositories

Install vsftpd

Install **FTP** client

Start and enable vsftpd service

Open /etc/vsftpd.conf

Enable local users and write permissions

Disable anonymous access

Configure passive **FTP** ports

Create ftpuser account

Create **FTP** directory and upload directory

Set directory ownership and permissions

Restart **FTP** server

Verify **TCP** port 21

Configure firewall if required

Connect using ftp localhost or server IP

Authenticate with ftpuser

List remote files using ls

Upload a file using put

Download a file using get

Verify transferred files and contents

Exit **FTP** session

Reset checklist

## 18. What to write in your practical journal / answer sheet

You can use the following format.

Aim: To install, configure and demonstrate an **FTP** Server on Ubuntu Linux using vsftpd.

Software requirements:

- Ubuntu Linux 24.04.
- vsftpd **FTP** server.
- **FTP** client.
- **TCP**/IP network.

Procedure:

## Updated the Ubuntu package repositories.

## Installed vsftpd and FTP client. ## Started and enabled the FTP service. ## Configured the FTP server using `/etc/vsftpd.conf`. ## Enabled local user authentication and file write permissions. ## Disabled anonymous access. ## Created a dedicated FTP user. ## Configured the FTP directory structure and permissions. ## Configured passive FTP ports. ## Restarted the FTP server. ## Connected to the FTP server using the FTP client. ## Uploaded and downloaded files. ## Verified the transferred files.

Result:

**FTP** Server was successfully installed and configured on Ubuntu Linux using vsftpd. The **FTP** client successfully connected to the server, authenticated using a local user account, and performed file upload and download operations.

## 19. Disable FTP Server after the practical

Since standard **FTP** is not encrypted, do not leave the service exposed unnecessarily.

Stop the service:

``` sudo systemctl stop vsftpd ```

Disable automatic startup:

``` sudo systemctl disable vsftpd ```

Verify:

``` sudo systemctl status vsftpd ```

If you enabled **UFW** rules specifically for this practical, remove them:

``` sudo ufw delete allow 21/tcp sudo ufw delete allow **40000**:**40100**/tcp ```

Only remove these rules if you added them for this experiment and do not need them for another service.

## 20. Final commands to remember

These are the most important commands for quick revision before entering the lab.

Installation

``` sudo apt update sudo apt install vsftpd inetutils-ftp -y ```

Start and enable server

``` sudo systemctl start vsftpd sudo systemctl enable vsftpd ```

Configuration

``` sudo nano /etc/vsftpd.conf ```

Create **FTP** user

``` sudo adduser ftpuser ```

Verify server

``` sudo systemctl status vsftpd sudo ss -tlnp | grep ':21' ```

Connect

``` ftp localhost ```

Upload and download

``` cd upload put clientfile.txt get serverfile.txt ls bye ```

&#x20;Copy commands

My recommendation for your lab exam: Make sure you demonstrate both `put` and `get`. Merely logging in to the **FTP** server is not sufficient to demonstrate file-transfer functionality. Showing a file uploaded from the client and then verifying its contents on the server is the strongest practical demonstration.

The central distinction to remember:

- Telnet demonstrates remote terminal access.
- **FTP** demonstrates remote file transfer.
- **SSH** provides secure remote terminal access.
- **SFTP** provides secure remote file transfer.
