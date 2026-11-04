# Practical: Installation, Configuration and Demonstration of Telnet Server



Linux practical examination

Ubuntu 24.04 LTS



## 1. Aim

To install, configure and demonstrate a Telnet Server on a Linux system and establish remote communication between a Telnet client and server.

## 2. What is Telnet?

Telnet (Teletype Network) is an application-layer protocol used to remotely access and manage another computer over a TCP/IP network.

It allows a user to:

- Connect to a remote Linux machine.
- Log in using a username and password.
- Execute commands on the remote machine.
- Access the remote machine's command-line interface.
- Manage files and processes, subject to the logged-in user's permissions.

Telnet follows a client-server architecture.

[Medium](https://images.openai.com/static-rsc-4/E7HjZdysyYjYRF6h2X1vLiXmDrR-IP3wcaqZgpttJtJeYsMyueuPIzwRcKq9moluaRC1S7xZbGDfSIV8cNDBhxCTQ2FtEm4Dv635Jwguxfo7k5PHD_qDt3WaiMy7S8-Jgm9Ck6sJVACe25rYa7DUvZW9WpnEXcpKopVajfFdOXk?purpose=inline)

[medium.com](https://medium.com/%40manohar017manu/what-is-telnet-81449156c54c?utm_source=chatgpt.com)

### Important characteristics

| Property           | Description                 |
| ------------------ | --------------------------- |
| Protocol           | Telnet                      |
| OSI layer          | Application layer (Layer 7) |
| Transport protocol | TCP                         |
| Default port       | 23                          |
| Architecture       | Client-server               |
| Communication      | Bidirectional               |
| Authentication     | Username and password       |
| Encryption         | None                        |
| Terminal type      | Virtual terminal (NVT)      |

Important examination point: Telnet transmits usernames, passwords and data in plaintext. Therefore, it is insecure for real-world remote administration. SSH (Secure Shell) is its secure alternative.

## 3. How Telnet works

The communication process is:

1. The Telnet client initiates a TCP connection to the server on port 23.
2. The server accepts the connection.
3. The server presents a login prompt.
4. The client enters a username and password.
5. The server authenticates the user.
6. After successful authentication, the server provides a remote shell.
7. Commands entered by the client execute on the server.
8. The output is transmitted back to the client.

[What is Port 23?](https://images.openai.com/static-rsc-4/APjOv28ktNbKvd21eSdOby4JmNiWxp5FjTEY8dGvJJKzNMxdgdaBXEQcdRzAnPmHIIWn5G2Ltek0sOutN_O8CGuC554_HuuXf-w9qjD5kzbmUBOF8p109RMynXdrGgL7DtYA9cVYQC0uKY8SKwZ81zPKN2o9bmJ4grxjA5Oj-pY?purpose=inline)

[cbtnuggets.com](https://www.cbtnuggets.com/common-ports/what-is-port-23?utm_source=chatgpt.com)

Example:

Suppose we have:

- Server IP: `192.168.1.10`
- Client IP: `192.168.1.20`
- Server port: `23`

The client executes:

```
telnet 192.168.1.10 23
```

The connection is established if the Telnet service is running and the network permits TCP port 23.

## 4. Requirements

For the practical, you can use either two Linux machines or one Linux machine with two terminals.

| Component      | Purpose                                                                             |
| -------------- | ----------------------------------------------------------------------------------- |
| Telnet Server  | Accepts remote connections                                                          |
| Telnet Client  | Initiates remote connections                                                        |
| inetd          | Internet super-server that listens for incoming requests and launches Telnet server |
| TCP/IP network | Provides communication                                                              |
| Port 23        | Default Telnet port                                                                 |

For your Ubuntu 24.04 laptop, we will use the GNU Inetutils Telnet server.

Ubuntu provides the `inetutils-telnetd` package for the server and `inetutils-telnet` for the client.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://packages.ubuntu.com\&sz=32)

Details of package inetutils-telnetd in noble+1



## 5. Installation of Telnet Server

### Step 1: Update package repositories

Open the terminal:

```
sudo apt update
```

This refreshes the local package index.

### Step 2: Install Telnet Server and Client

```
sudo apt install inetutils-telnetd inetutils-telnet -y
```

The packages serve different purposes:

- `inetutils-telnetd`: Installs the Telnet server.
- `inetutils-telnet`: Installs the Telnet client.

The server also requires an Internet super-server (inetd), which is installed as a dependency.

### Step 3: Verify installation

```
telnet --version
```

Check the server executable:

```
which telnetd
```

You can also check installed packages:

```
dpkg -l | grep -E 'inetutils-telnet|telnetd|inetd'
```

## 6. Configuration of Telnet Server

This is the most important part of the practical.

Ubuntu 24.04 uses an inetd-based configuration. The Telnet service may be installed but disabled by default.

### Step 1: Check the inetd configuration

Open the configuration file:

```
sudo nano /etc/inetd.conf
```

Look for a Telnet entry similar to:

```
#<off># telnet stream tcp nowait telnetd /usr/sbin/tcpd /usr/sbin/in.telnetd
```

The `#<off>#` indicates that the service is disabled.

### Step 2: Enable Telnet service

Remove the `#<off>#` prefix so that the line becomes:

```
telnet stream tcp nowait telnetd /usr/sbin/tcpd /usr/sbin/in.telnetd
```

Save the file:

- Press `Ctrl + O` to save.
- Press `Enter`.
- Press `Ctrl + X` to exit.

What does this configuration mean?

| Field                | Meaning                                                                |
| -------------------- | ---------------------------------------------------------------------- |
| telnet               | Service name                                                           |
| stream               | TCP stream socket                                                      |
| tcp                  | Transport protocol                                                     |
| nowait               | inetd handles the connection without waiting for the service to finish |
| telnetd              | User account under which the server runs                               |
| /usr/sbin/tcpd       | TCP wrapper, where available                                           |
| /usr/sbin/in.telnetd | Telnet server executable                                               |

### Step 3: Restart inetd

For Ubuntu 24.04, execute:

```
sudo systemctl restart inetutils-inetd
```

Check its status:

```
sudo systemctl status inetutils-inetd
```

Expected output should contain:

```
Active: active (running)
```

You can press `q` to exit the status screen.

### Step 4: Verify that port 23 is listening

Execute:

```
sudo ss -tlnp | grep ':23'
```

Expected output will look similar to:

```
LISTEN 0 10 0.0.0.0:23 0.0.0.0:*
```

This indicates that the server is listening for incoming TCP connections on port 23.

The `ss` command displays socket information.

- `-t`: TCP sockets.
- `-l`: Listening sockets.
- `-n`: Numeric addresses and ports.
- `-p`: Associated processes.

The Ubuntu configuration and service activation procedure are documented in the package and server references.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://linuxcapable.com\&sz=32)

LinuxCapable+1



## 7. Create a user for remote login

For the practical, create a separate normal Linux user rather than using root.

Execute:

```
sudo adduser telnetuser
```

You will be prompted to enter a password and optional user details.

For example:

```
New password:
Retype new password:
Full Name:
Room Number:
Work Phone:
Home Phone:
Other:
```

You can leave the optional details blank.

Verify the account:

```
id telnetuser
```

Why create a separate user?

The Telnet client needs a valid account on the server. The user will authenticate using the username and password created on the server.

Do not enable direct root login for this demonstration.

## 8. Demonstration of Telnet Server

Now comes the actual practical demonstration.

There are two methods.

### Method A: Connect using localhost (single machine)

This is the easiest method if you have only one laptop.

Terminal 1 – Server

Check the service:

```
sudo systemctl status inetutils-inetd
```

Check port 23:

```
sudo ss -tlnp | grep ':23'
```

Terminal 2 – Client

Connect to the local Telnet server:

```
telnet localhost
```

Alternatively:

```
telnet 127.0.0.1 23
```

Expected output:

```
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
Ubuntu 24.04 LTS
login:
```

Enter:

```
telnetuser
```

Then enter the password you created.

After successful authentication, you should get a remote shell.

[Explaing sl commandand cowway etc and find out defferent? | by Aamir qureshi | Medium](https://images.openai.com/static-rsc-4/SVwcLfO1OtFQvAJ_Jm6eUqq6Jw7BFobz_wLh-7yS9zIgEWUxEayuS12YQYW593nufaHbs7_QmfTsNdou8FXcFy7CiPdP0OLkLBYjot0yhP-sJhLB84TW-LkBvI6gbLDcqyPzkRBQQ2Ebt0AeCeglRkzIQ6URXvc8YADEzVnIlQY?purpose=inline)

[medium.com](https://medium.com/%40aq702654/explaing-sl-commandand-cowway-etc-and-find-out-defferent-febf7e173e3c?utm_source=chatgpt.com)

### Method B: Connect between two different machines

This is a better demonstration of actual client-server communication.

Suppose you have:

| Machine   | Role          | IP address   |
| --------- | ------------- | ------------ |
| Machine 1 | Telnet Server | 192.168.1.10 |
| Machine 2 | Telnet Client | 192.168.1.20 |

These are example IP addresses; use your actual IP addresses.

On the server machine

Find its IP address:

```
hostname -I
```

Make sure the Telnet server is listening:

```
sudo ss -tlnp | grep ':23'
```

If UFW is enabled, permit connections from your lab network. Replace the subnet below with your actual network subnet:

```
sudo ufw allow from 192.168.1.0/24 to any port 23 proto tcp
```

On the client machine

Install the Telnet client:

```
sudo apt update
sudo apt install inetutils-telnet -y
```

Connect to the server:

```
telnet 192.168.1.10 23
```

Enter the server's username and password.

If successful, you will receive a remote shell on Machine 1.

[Accessing Remote Servers with Telnet (Use with Caution!) - DEV Community](https://images.openai.com/static-rsc-4/3FSvl037A_2Y7ngHKSUEOHAF-Q5mvlBxVSBqW10Lh2zGcfhyvZe7DjPIWJ_Ll0jS9V1Tzx224u17CmEqD8RC3ZZr-io0he-FAWO_nT4TWc9nIIfffTSAioEs9U4GzpTJPYw9GTreaeuVdgdtRw4b1zT0ifv5TDeh6sE67iw977Q?purpose=inline)

[dev.to](https://dev.to/babsarena/accessing-remote-servers-with-telnet-use-with-caution-414a?utm_source=chatgpt.com)

## 9. Verify remote command execution

Once logged in through Telnet, execute the following commands in the Telnet session:

Command 1: Check username

```
whoami
```

Expected output:

```
telnetuser
```

Command 2: Check hostname

```
hostname
```

This displays the hostname of the remote server, not the client.

Command 3: Check IP configuration

```
hostname -I
```

This displays the IP address of the server.

Command 4: Display current directory

```
pwd
```

Command 5: Create a file on the server

```
echo "Hello from Telnet Client" > telnet_demo.txt
```

Command 6: Verify the file

```
cat telnet_demo.txt
```

Expected output:

```
Hello from Telnet Client
```

Command 7: Check logged-in users

```
who
```

This helps demonstrate the remote login session.

Command 8: Exit the Telnet session

```
exit
```

You will return to the local terminal.

Demonstration complete

You have demonstrated:

1. Installation of Telnet server.
2. Configuration of Telnet service.
3. Establishment of a TCP connection.
4. Remote user authentication.
5. Remote command execution.
6. File creation and verification on the server.

## 10. Important configuration and verification commands

These are the commands you should remember for your examination.

| Command                                                  | Purpose                     |
| -------------------------------------------------------- | --------------------------- |
| `sudo apt update`                                        | Update package repositories |
| `sudo apt install inetutils-telnetd inetutils-telnet -y` | Install server and client   |
| `sudo nano /etc/inetd.conf`                              | Configure Telnet service    |
| `sudo systemctl restart inetutils-inetd`                 | Restart inetd               |
| `sudo systemctl status inetutils-inetd`                  | Check service status        |
| `sudo ss -tlnp`                                          | Check listening TCP ports   |
| `hostname -I`                                            | Find IP address             |
| `sudo adduser telnetuser`                                | Create a user               |
| `telnet localhost`                                       | Connect locally             |
| `telnet IP_ADDRESS 23`                                   | Connect to remote server    |
| `whoami`                                                 | Identify logged-in user     |
| `exit`                                                   | Terminate Telnet session    |

## 11. Troubleshooting common errors

During your practical, you might encounter these errors.

### Error 1: Connection refused

```
telnet: Unable to connect to remote host: Connection refused
```

Possible reasons:

- Telnet server is not running.
- Port 23 is not listening.
- Telnet service is disabled in `/etc/inetd.conf`.

Solution:

```
sudo nano /etc/inetd.conf
```

Check that the Telnet entry is enabled.

Then:

```
sudo systemctl restart inetutils-inetd
sudo ss -tlnp | grep ':23'
```

### Error 2: Connection timed out

```
Connection timed out
```

Possible reasons:

- Client and server are not reachable over the network.
- Firewall is blocking port 23.
- Incorrect server IP address.

Solution:

Check network connectivity:

```
ping SERVER_IP
```

Check firewall:

```
sudo ufw status
```

Allow TCP port 23 from your lab network if required.

### Error 3: Login incorrect

```
Login incorrect
```

Possible reasons:

- Incorrect username.
- Incorrect password.
- User account does not exist.

Solution:

On the server:

```
id telnetuser
```

Reset the password if necessary:

```
sudo passwd telnetuser
```

### Error 4: Unit not found

```
Unit inetutils-inetd.service could not be found
```

Check installed packages:

```
dpkg -l | grep inetd
```

Check available services:

```
systemctl list-unit-files | grep inetd
```

Install the missing inetd implementation if required:

```
sudo apt install inetutils-inetd
```

Then retry the service configuration.

## 12. Telnet vs SSH

This is a very important viva question.

| Feature           | Telnet                             | SSH                                   |
| ----------------- | ---------------------------------- | ------------------------------------- |
| Full form         | Teletype Network                   | Secure Shell                          |
| Default port      | 23                                 | 22                                    |
| Transport         | TCP                                | TCP                                   |
| Encryption        | No                                 | Yes                                   |
| Authentication    | Typically username/password        | Password or public-key authentication |
| Security          | Insecure                           | Secure when properly configured       |
| Data transmission | Plaintext                          | Encrypted                             |
| Usage             | Legacy systems, lab demonstrations | Modern remote administration          |

[Le protocole Telnet pour les débutants - Réseau informatique](https://images.openai.com/static-rsc-4/YGwHwtH10PB_WypJzjHJwRFhHQyiuzDQqxirGFt99BQEgyN9R0LGg_vDpLiRLVsqLNRIDlT2qtYU8VGfz_OSICu3iGP9GYWnw9kszoh9nQnVDxpt7-1KbrhVWU7Y6Mug6lITJnRKwsRYDFis5HMpwo9B-W9Vih9g4brFC-ZdISU?purpose=inline)

[5.2. セキュアシェルsshのしくみ/How the secure shell works — Simulation programming guidebook for C++ 1.0 documentation](https://images.openai.com/static-rsc-4/H_9-XS8FcpMItmoaLu4ldyALMhW_NSHi6S96WxkiSrBIBdxp8FYQ1FkJqr85_rS7A0ugvazwBgKfUiIpxFmoJRBaT4LKzFu3WZpsUuhQHyYNqsjjBIUYGThzNUl0IKGxDloxmUH5aV8SY1FU3QKyRj-Ia4M2is8yrD5fABKKFwU?purpose=inline)

[Wireshark for Pentester: Password Sniffing](https://images.openai.com/static-rsc-4/C3oHn4bWSsP7CTr7mtFJM3-XW6-GPFWwrGk2hSLTgqLx22nkLt9go12-lnMSt7N9nm3EJzoVWSOSImToM7Wdx_p29MYXZ1ak5eJ9Zyr2CF1DaaixVrT1vr3QV4_Cxm4WzessIcOflaFYUTk0mJpq4ZGquBY88fSHrXh12g9pWsc?purpose=inline)

6

Why is SSH preferred over Telnet?

Telnet does not encrypt its communication. Anyone who can capture the network traffic may be able to read the username, password and commands.

SSH encrypts the communication, protecting the session against network eavesdropping.

For real-world administration, use SSH rather than Telnet.

## 13. Advantages and disadvantages of Telnet

Advantages

1. Simple to install and configure.
2. Requires relatively few system resources.
3. Supports remote command-line access.
4. Useful for testing TCP connectivity.
5. Supports communication between different operating systems.

Disadvantages

1. No encryption.
2. User credentials are transmitted in plaintext.
3. Vulnerable to eavesdropping and man-in-the-middle attacks.
4. Not suitable for sensitive information.
5. Has largely been replaced by SSH.

## 14. Important viva questions and answers

These are questions an examiner may ask after your demonstration.

Q1. What is Telnet?

Telnet is an application-layer protocol used for remote terminal access to another computer over a TCP/IP network.

Q2. Which port does Telnet use?

TCP port 23 by default.

Q3. Is Telnet TCP or UDP?

Telnet uses TCP because it requires reliable, connection-oriented communication.

Q4. What is the difference between Telnet client and server?

- Client initiates a connection.
- Server listens for incoming connections and provides remote terminal access.

Q5. What is inetd?

inetd is an Internet super-server that listens for requests on configured network ports and launches the corresponding network service when a request arrives.

Q6. What is the purpose of `/etc/inetd.conf`?

It contains configuration entries defining which network services inetd should listen for and how those services should be started.

Q7. Why do we use port 23?

Port 23 is the standard registered port for the Telnet protocol.

Q8. What is NVT?

NVT stands for Network Virtual Terminal. It provides a standard representation of terminal communication so that different types of computers can communicate.

Q9. What is the difference between local and remote login?

- Local login: A user accesses the machine directly.
- Remote login: A user accesses another machine over a network.

Q10. Can we use Telnet to transfer files?

Telnet itself is not a file-transfer protocol. FTP or SFTP can be used for file transfer.

Q11. Why is Telnet insecure?

Because it transmits credentials and session data without encryption.

Q12. What is the alternative to Telnet?

SSH (Secure Shell).

Q13. How can you check whether port 23 is open?

```
sudo ss -tlnp | grep ':23'
```

Q14. What happens if the server is stopped?

The client cannot establish a new Telnet connection to that server.

Q15. Can Telnet connect to a web server?

Yes. Telnet can establish a TCP connection to a web server's port, such as port 80, but it does not itself implement HTTP.

Example:

```
telnet example.com 80
```

This can be used for basic TCP and HTTP troubleshooting.

Q16. What is the purpose of TCP's three-way handshake?

It establishes a TCP connection using SYN, SYN-ACK and ACK packets before application data is exchanged.

## 15. Practical examination procedure

Here is the order I recommend following in your lab examination.

## Telnet practical checklist

Practical progress

0/13 completed

Update Ubuntu package repositories

Install Telnet server and client

Check /etc/inetd.conf

Enable the Telnet service

Restart inetd

Verify service status

Verify TCP port 23

Create a separate login user

Connect using telnet localhost or server IP

Authenticate with username and password

Execute remote Linux commands

Create and read a test file

Exit the Telnet session

Reset checklist

## 16. What to write on your practical answer sheet

You can use this format for your journal or examination record.

Aim: To install, configure and demonstrate Telnet Server on Ubuntu Linux.

Software requirements:

- Ubuntu Linux 24.04.
- Telnet server package.
- Telnet client package.
- TCP/IP network connectivity.

Procedure:

1. Updated the package repositories.
2. Installed Telnet server and client.
3. Enabled the Telnet service using `/etc/inetd.conf`.
4. Restarted the inetd service.
5. Verified that TCP port 23 was listening.
6. Created a separate user account for remote login.
7. Connected to the Telnet server using the Telnet client.
8. Authenticated using the server's username and password.
9. Executed remote Linux commands and verified file creation.

Result:

Telnet Server was successfully installed and configured on Ubuntu Linux. A Telnet client established a TCP connection with the server using port 23, authenticated successfully and executed remote commands.

## 17. Extra: Disable Telnet after your practical

Since Telnet is insecure, do not leave it enabled for normal use.

Edit the configuration:

```
sudo nano /etc/inetd.conf
```

Comment out the Telnet entry again:

```
#telnet stream tcp nowait telnetd /usr/sbin/tcpd /usr/sbin/in.telnetd
```

Restart inetd:

```
sudo systemctl restart inetutils-inetd
```

Verify that port 23 is no longer listening:

```
sudo ss -tlnp | grep ':23'
```

No output means no matching TCP listener was found.

## 18. Final understanding: What exactly are you demonstrating?

Remember this distinction because it is useful when explaining the practical to your examiner:

- Installation means installing the Telnet server and client software.
- Configuration means enabling the Telnet service and configuring the network listener.
- Authentication means verifying the remote user's identity.
- Demonstration means connecting from the client and executing commands on the server.

The most important commands to remember are:

```
sudo apt install inetutils-telnetd inetutils-telnet -y

sudo nano /etc/inetd.conf

sudo systemctl restart inetutils-inetd

sudo systemctl status inetutils-inetd

sudo ss -tlnp | grep ':23'

sudo adduser telnetuser

telnet localhost
```

My recommendation: First perform the localhost demonstration on your ThinkPad. Once it works, try connecting from a second Linux machine if one is available. This lets you demonstrate both Telnet functionality and actual network-based remote login.
