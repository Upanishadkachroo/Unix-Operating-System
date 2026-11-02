# Caddy Web Server – Go Applications Experiment 1

A complete practical guide to installing, configuring, and demonstrating **Caddy**, an open-source web server written in the Go programming language.

---

## Table of Contents

1. [Aim](#1-aim)
2. [Introduction to Caddy](#2-introduction-to-caddy)
3. [Architecture and Working](#3-architecture-and-working)
4. [Requirements](#4-requirements)
5. [Installation of Caddy](#5-installation-of-caddy)
6. [Hosting a Website with Caddy](#6-hosting-a-website-with-caddy)
7. [Verifying HTTP/HTTPS Functionality](#7-verifying-httphttps-functionality)
8. [Understanding Automatic HTTPS](#8-understanding-automatic-https)
9. [Reverse Proxy Demonstration (Optional)](#9-reverse-proxy-demonstration-optional)
10. [Stopping Caddy and Restoring Apache](#10-stopping-caddy-and-restoring-apache)
11. [Common Errors and Troubleshooting](#11-common-errors-and-troubleshooting)
12. [Experiment Outcome](#12-experiment-outcome)
13. [Viva Questions and Answers](#13-viva-questions-and-answers)
14. [Result](#14-result)

---

## 1. Aim

To install, configure, and demonstrate **Caddy**, an open-source web server written in Go that supports HTTP/2 and provides automatic HTTPS using TLS certificates.

---

## 2. Introduction to Caddy

Caddy is a modern web server and reverse proxy written in the **Go programming language**.

Unlike traditional web servers that often require manual SSL certificate configuration, Caddy can automatically obtain and renew TLS certificates.

### Key Features

| Feature | Description |
|---------|-------------|
| **Written in Go** | Developed using the Go programming language |
| **HTTP/2 Support** | Supports modern HTTP communication |
| **Automatic HTTPS** | Automatically obtains and renews TLS certificates when domain and network configuration permit |
| **Reverse Proxy** | Forwards incoming requests to backend applications |
| **Simple Configuration** | Uses a human-readable configuration file called `Caddyfile` |
| **Cross-Platform** | Runs on Linux, Windows, macOS, and other supported platforms |

---

## 3. Architecture and Working

The basic request flow is:

1. A client (browser) sends an HTTP or HTTPS request.
2. Caddy receives the request.
3. Caddy processes the request according to its configuration.
4. It either serves static website files or forwards the request to a backend application.
5. The response is returned to the client.

---

## 4. Requirements

| Requirement | Purpose |
|-------------|---------|
| Ubuntu 24.04 | Operating system |
| Internet connection | Download Caddy |
| Terminal | Execute commands |
| curl | Test HTTP/HTTPS requests |
| Browser | Verify the hosted website |

> **Note:** This demonstration uses Ubuntu and does **not** require a public domain name.

---

## 5. Installation of Caddy

### Step 1: Update package lists

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install dependencies

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
```

### Step 3: Add the official Caddy repository

Download and install its signing key:

```bash
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
```

Add the repository:

```bash
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
```

Set the required permissions:

```bash
sudo chmod o+r /usr/share/keyrings/caddy-stable-archive-keyring.gpg
sudo chmod o+r /etc/apt/sources.list.d/caddy-stable.list
```

### Step 4: Install Caddy

```bash
sudo apt update
sudo apt install -y caddy
```

### Step 5: Verify installation

```bash
caddy version
```

Check whether the service is running:

```bash
sudo systemctl status caddy
```

**Expected result:**
- Caddy should be installed.
- The systemd service should show `active (running)`.

> The official Ubuntu/Debian package normally starts Caddy automatically as a systemd service.

---

## 6. Hosting a Website with Caddy

### Step 1: Create the website directory

```bash
sudo mkdir -p /var/www/caddy-demo
```

### Step 2: Create an HTML file

```bash
sudo nano /var/www/caddy-demo/index.html
```

Paste the following HTML:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Caddy Web Server Experiment</title>
</head>
<body>
    <h1>Welcome to Caddy Web Server!</h1>

    <h2>Go Application Demonstration</h2>

    <p>Caddy is an open-source web server written in Go.</p>

    <h3>Features Demonstrated</h3>
    <ul>
        <li>HTTP/2 support</li>
        <li>Automatic HTTPS</li>
        <li>Static website hosting</li>
        <li>TLS certificate management</li>
    </ul>

    <p>Experiment performed on Ubuntu Linux.</p>
</body>
</html>
```

Save using `Ctrl + O`, `Enter`, and exit using `Ctrl + X`.

### Step 3: Set permissions

```bash
sudo chown -R caddy:caddy /var/www/caddy-demo
sudo chmod 755 /var/www/caddy-demo
sudo chmod 644 /var/www/caddy-demo/index.html
```

### Step 4: Modify the Caddyfile

```bash
sudo nano /etc/caddy/Caddyfile
```

Replace the existing configuration with:

```caddyfile
localhost:8080 {
    root * /var/www/caddy-demo
    file_server
}
```

### Understanding the configuration

| Directive | Function |
|-----------|----------|
| `localhost:8080` | Defines the address and port |
| `root *` | Specifies the website's root directory |
| `file_server` | Enables static file serving |

### Step 5: Validate and reload

```bash
sudo caddy validate --config /etc/caddy/Caddyfile
```

If valid:

```bash
sudo systemctl reload caddy
```

Check the service:

```bash
sudo systemctl status caddy
```

### Step 6: Test your website

```bash
curl -k -I https://localhost:8080
```

Expected response includes:

```
HTTP/2 200
content-type: text/html
server: Caddy
```

View the HTML response:

```bash
curl -k https://localhost:8080
```

Open your browser and visit:

```
https://localhost:8080
```

You should see your HTML webpage.

> Caddy automatically enables HTTPS for the localhost hostname. It may prompt for permission to install its local certificate authority into the trust store. If necessary, use:
>
> ```bash
> sudo caddy trust
> ```

> **Important:** A localhost certificate is **locally trusted**, not a publicly trusted certificate. This demonstration establishes local HTTPS; public-domain certificate issuance is a separate demonstration.

---

## 7. Verifying HTTP/HTTPS Functionality

Open a second terminal.

### Test HTTPS response

```bash
curl -k -I https://localhost:8080
```

Expected response includes:

```
HTTP/2 200
content-type: text/html
```

> The exact HTTP version may depend on the client's protocol negotiation.

### Test webpage content

```bash
curl -k https://localhost:8080
```

You should see the HTML content of your webpage.

### Check HTTP/2 support in curl

```bash
curl -V
```

Look for `HTTP2` in the listed features.

### Test HTTP/2 explicitly

```bash
curl -k --http2 -I https://localhost:8080
```

> If your installed `curl` does not support HTTP/2, use a browser's **Developer Tools → Network → Protocol** column to inspect the negotiated protocol.

### Check which ports Caddy is listening on

```bash
sudo ss -ltnp | grep caddy
```

### Test the actual HTTPS endpoint on the configured port

```bash
curl -k -I https://localhost:8080
```

Expected output:

```
HTTP/2 200
alt-svc: h3=":8080"; ma=2592000
content-type: text/html; charset=utf-8
server: Caddy
```

| Output | Meaning |
|--------|---------|
| `HTTP/2 200` | Request succeeded using HTTP/2 |
| `alt-svc: h3=":8080"` | Caddy advertises HTTP/3 availability |
| `content-type: text/html` | Response is an HTML page |
| `server: Caddy` | Response was served by Caddy |

### Inspect your Caddy configuration

```bash
sudo cat /etc/caddy/Caddyfile
```

---

## 8. Understanding Automatic HTTPS

Caddy's automatic HTTPS mechanism works as follows:

1. Caddy identifies the hostname in its configuration.
2. It determines that HTTPS should be enabled.
3. For localhost, it generates certificates using its own **local certificate authority**.
4. It serves requests over HTTPS.
5. It manages certificate storage and renewal.

For a public domain, Caddy can obtain a publicly trusted certificate from an ACME certificate authority such as **Let's Encrypt**, provided DNS and network requirements are satisfied.

### Difference between local and public demonstrations

| Localhost Demonstration | Public-Domain Demonstration |
|--------------------------|------------------------------|
| Uses `localhost` | Uses a registered domain |
| Local CA certificate | Publicly trusted certificate |
| No public DNS required | DNS must point to the server |
| No public exposure required | Ports 80 and 443 must be reachable |

### Trust the local certificate authority

If you encounter a certificate warning in the browser:

```bash
sudo caddy trust
```

Then reload the browser.

### HTTP request on port 80 (redirect behavior)

```bash
curl -I http://localhost
```

Example output:

```
HTTP/1.1 308 Permanent Redirect
Location: https://localhost:8080/
Server: Caddy
```

This confirms Caddy is redirecting HTTP traffic to the HTTPS endpoint.

### HTTPS request on the default port 443

```bash
curl -k -I https://localhost
```

> If Caddy is configured on port 8080, this request will fail with `curl: (7) Failed to connect to localhost port 443`. That is expected because Caddy is listening on 8080 in this demonstration. Use `https://localhost:8080` instead.

---

## 9. Reverse Proxy Demonstration (Optional)

A reverse proxy forwards client requests to another application.

Suppose a backend application is running on port **9000**. Caddy can forward requests to it.

### Step 1: Create another configuration

```bash
nano reverse-proxy.Caddyfile
```

Add:

```caddyfile
localhost:8081 {
    reverse_proxy localhost:9000
}
```

### Step 2: Start the backend application

Start your backend application separately on port **9000**.

### Step 3: Run Caddy with the reverse proxy configuration

```bash
caddy run --config reverse-proxy.Caddyfile
```

### Step 4: Visit the reverse-proxied site

```
https://localhost:8081
```

Caddy will forward requests to the backend application.

> This is an optional extension; the static website demonstration is sufficient to establish the basic Caddy setup.

---

## 10. Stopping Caddy and Restoring Apache

### Stop Caddy

If Caddy is running in the foreground, press:

```
Ctrl + C
```

Or stop the systemd service:

```bash
sudo systemctl stop caddy
```

### Restore Apache (if you need it for other practicals)

```bash
sudo systemctl start apache2
```

Verify:

```bash
sudo systemctl status apache2
```

> **Important:** Apache and Caddy both default to port 80. They cannot run simultaneously on the same IP address and port. Stop Caddy before restarting Apache.

### Useful service-management commands

| Command | Purpose |
|---------|---------|
| `sudo systemctl start caddy` | Start Caddy |
| `sudo systemctl stop caddy` | Stop Caddy |
| `sudo systemctl restart caddy` | Restart Caddy |
| `sudo systemctl reload caddy` | Reload configuration |
| `sudo journalctl -u caddy -f` | View live logs |
| `caddy version` | Display version |

---

## 11. Common Errors and Troubleshooting

| Problem | Possible Solution |
|---------|-------------------|
| `address already in use` | Stop the existing Caddy service, Apache, or Nginx, or use another port |
| `permission denied` | Check directory permissions and file ownership |
| Certificate warning in browser | Run `sudo caddy trust` and restart browser |
| Website not found (404) | Check the root directory and `index.html` |
| Caddy configuration error | Run `caddy validate --config Caddyfile` |
| Caddy service fails | Inspect `sudo journalctl -u caddy -n 50` |

### Diagnosing port conflicts

If Caddy fails with `listening on :80: bind: address already in use`, identify the process using port 80:

```bash
sudo ss -ltnp | grep ':80 '
```

Alternatively:

```bash
sudo lsof -i :80
```

You may see `apache2`, `nginx`, `docker-proxy`, or another `caddy` process.

### Fixing the conflict

**Option A – Keep Apache/Nginx running (recommended if you need it).**

Change Caddy to use port 8080:

```bash
sudo nano /etc/caddy/Caddyfile
```

Replace its contents with:

```caddyfile
localhost:8080 {
    respond "Caddy Web Server is Working!"
}
```

Validate and restart:

```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl restart caddy
sudo systemctl status caddy
```

Test in your browser:

```
https://localhost:8080
```

**Option B – Give port 80 to Caddy.**

Stop Apache or Nginx:

```bash
sudo systemctl stop apache2
# or
sudo systemctl stop nginx
```

Then restart Caddy:

```bash
sudo systemctl restart caddy
sudo systemctl status caddy
```

### Note about Postfix messages

You may see:

```
fatal: open /etc/postfix/main.cf: No such file or directory
```

This is unrelated to Caddy's startup. It indicates a missing Postfix configuration, likely from an attempted system mail notification. It can be safely ignored for this experiment.

---

## 12. Experiment Outcome

Your final demonstration should establish:

- ✅ Caddy is installed successfully.
- ✅ Caddy is running as a web server (systemd service `active (running)`).
- ✅ A custom HTML webpage is hosted.
- ✅ The webpage is accessible through HTTPS.
- ✅ HTTP/2 support can be verified (`HTTP/2 200` response).
- ✅ Caddy's reverse-proxy functionality can optionally be demonstrated.

### Practical demonstration checklist

- [x] Caddy installed successfully
- [x] Caddy systemd service running
- [x] Port 80 and HTTPS redirection verified
- [x] Local TLS certificate obtained
- [x] HTTP/2 response verified
- [x] HTML website hosted successfully
- [x] Website opened in browser
- [x] Caddy configuration validated

### Sample verified output

```
$ curl -k -I https://localhost:8080
HTTP/2 200
alt-svc: h3=":8080"; ma=2592000
content-type: text/html; charset=utf-8
server: Caddy
content-length: 512
date: Mon, 02 Nov 2026 05:10:12 GMT
```

```
$ sudo ss -ltnp | grep caddy
LISTEN 0 4096 *:80 *:* users:(("caddy",pid=105966,fd=9))
```

```
$ sudo systemctl status caddy
● caddy.service - Caddy
     Loaded: loaded (/usr/lib/systemd/system/caddy.service; enabled; preset: enabled)
     Active: active (running)
   Main PID: 105966 (caddy)
```

---

## 13. Viva Questions and Answers

**Q1. What is Caddy?**
Caddy is an open-source web server and reverse proxy written in Go. It supports HTTP/1.1, HTTP/2, HTTP/3 and automatic HTTPS.

**Q2. Why is Caddy associated with Go?**
Caddy is implemented using Go. Go provides concurrency, portability, efficient networking, and a convenient deployment model.

**Q3. What is HTTP/2?**
HTTP/2 is a version of the HTTP protocol that supports multiplexing multiple requests over a single TCP connection, header compression, and more efficient communication.

**Q4. What is HTTPS?**
HTTPS is HTTP secured using TLS (Transport Layer Security). It provides encryption, authentication, and data integrity.

**Q5. What is TLS?**
TLS is a cryptographic protocol that secures communication between clients and servers.

**Q6. What is an SSL certificate?**
An SSL certificate is commonly used to refer to a digital certificate used in HTTPS. Modern HTTPS actually uses TLS rather than the obsolete SSL protocols.

**Q7. What is automatic HTTPS?**
It is Caddy's ability to automatically obtain, configure, and renew TLS certificates for eligible domains and configure HTTP-to-HTTPS redirects.

**Q8. What is a Caddyfile?**
A Caddyfile is Caddy's human-readable configuration file. It specifies site addresses, document roots, reverse proxies, and other server directives.

**Q9. What is a reverse proxy?**
A reverse proxy receives requests from clients and forwards them to backend servers. It can also handle TLS termination, load balancing, and routing.

**Q10. What is the difference between a web server and a reverse proxy?**
A web server can directly serve website files, whereas a reverse proxy forwards requests to other servers. Caddy supports both functions.

**Q11. What is the purpose of port 443?**
Port 443 is the standard port for HTTPS communication.

**Q12. What is ACME?**
ACME (Automatic Certificate Management Environment) is a protocol used to automate the issuance and renewal of TLS certificates.

**Q13. What is systemd?**
systemd is a Linux initialization and service-management system. It allows Caddy to run as a background service.

**Q14. What is the difference between `caddy run` and `caddy start`?**
- `caddy run`: Runs Caddy in the foreground.
- `caddy start`: Starts Caddy in the background.

**Q15. Can Caddy serve static websites?**
Yes. The `file_server` directive allows Caddy to serve static files such as HTML, CSS, JavaScript, and images.

---

## 14. Result

Caddy, an open-source web server written in Go, was **successfully installed and configured**. A sample HTML website was hosted, HTTPS functionality was demonstrated using Caddy's automatic local certificate management, and HTTP/2 support was verified.

---

## Recommendations for the Practical Examination

Focus on the following steps, which demonstrate the core functionality without requiring a registered domain or cloud server:

1. **Installation** of Caddy
2. Creating `index.html`
3. Configuring the `Caddyfile`
4. Running Caddy
5. Opening `https://localhost:8080`
6. Explaining **automatic HTTPS**

---

## Cleanup Reminder

After completing the experiment, remember to:

```bash
sudo systemctl stop caddy
sudo systemctl start apache2
```

This restores your Apache setup (e.g., for MantisBT) and avoids port conflicts.