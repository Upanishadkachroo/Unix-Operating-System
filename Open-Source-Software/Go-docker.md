# Go Applications – Experiment 2: Docker

A complete practical guide to installing, configuring, and demonstrating **Docker**, a containerization platform written primarily in Go for building, deploying, and running applications inside containers.

---

## Table of Contents

1. [Aim](#1-aim)
2. [Introduction to Docker](#2-introduction-to-docker)
3. [Docker Architecture](#3-docker-architecture)
4. [Requirements](#4-requirements)
5. [Installation of Docker on Ubuntu](#5-installation-of-docker-on-ubuntu)
6. [Run the First Docker Container](#6-run-the-first-docker-container)
7. [Docker Images and Containers](#7-docker-images-and-containers)
8. [Deploy a Web Server Using Docker](#8-deploy-a-web-server-using-docker)
9. [Manage Docker Containers](#9-manage-docker-containers)
10. [Build Your Own Docker Image Using a Dockerfile](#10-build-your-own-docker-image-using-a-dockerfile)
11. [Important Docker Commands](#11-important-docker-commands)
12. [Docker Networking and Port Mapping](#12-docker-networking-and-port-mapping)
13. [Docker Volumes and Persistent Data](#13-docker-volumes-and-persistent-data)
14. [Docker Compose](#14-docker-compose)
15. [Common Errors and Troubleshooting](#15-common-errors-and-troubleshooting)
16. [Cleanup After the Experiment](#16-cleanup-after-the-experiment)
17. [Viva Questions and Answers](#17-viva-questions-and-answers)
18. [Result](#18-result)
19. [Quick Practical Examination Checklist](#19-quick-practical-examination-checklist)
20. [Final Commands to Remember](#20-final-commands-to-remember)

---

## 1. Aim

To install, configure, and demonstrate **Docker**, a platform consisting of tools for building, deploying, and running applications inside containers. The experiment covers Docker installation, image management, container creation, execution, and deployment of a web application.

---

## 2. Introduction to Docker

Docker is an open-source **containerization platform** that allows developers to package applications and their dependencies into portable units called **containers**.

Docker is primarily implemented using **Go** and uses Linux kernel features such as **namespaces** and **control groups (cgroups)** to isolate and manage containers.

### 2.1 Why Docker is Used

Consider an application that works correctly on one developer's computer but fails on another computer because of different software versions or dependencies.

Docker addresses this problem by packaging the application and its dependencies into a consistent environment.

For example, a web application may require:

- Ubuntu Linux
- Python or Node.js
- Specific libraries
- Configuration files
- Application source code

Docker allows these requirements to be packaged into an **image** and executed as a **container**.

### 2.2 Important Features of Docker

| Feature | Description |
|---------|-------------|
| **Containerization** | Runs applications in isolated environments called containers |
| **Portability** | Containers can run on different systems that support Docker |
| **Lightweight Execution** | Containers share the host operating system's kernel instead of running a separate guest operating system |
| **Image Management** | Applications and their dependencies are packaged into reusable images |
| **Scalability** | Multiple containers can run simultaneously |
| **Isolation** | Linux namespaces and cgroups help isolate processes and manage resources |
| **Docker Hub** | Provides a registry for storing and distributing container images |

---

## 3. Docker Architecture

Docker uses a **client-server architecture**. Its main components are:

| Component | Description |
|-----------|-------------|
| **Docker Client** | Provides the command-line interface used to communicate with Docker |
| **Docker Daemon** | Background service responsible for managing Docker objects |
| **Docker Image** | Read-only template used to create containers |
| **Docker Container** | Running or stopped instance of an image |
| **Docker Registry** | Repository used to store and distribute Docker images |
| **Docker Hub** | Public container image registry maintained by Docker |

### 3.1 Working of Docker

## The user enters a Docker command in the terminal.

## The Docker client sends the request to the Docker daemon. ## The daemon checks whether the required image is available locally. ## If the image is unavailable, Docker can download it from a registry. ## The daemon creates and starts a container using the image. ## The application executes inside the container.

---

## 4. Requirements

| Requirement | Purpose |
|-------------|---------|
| Ubuntu 24.04 | Host operating system |
| Internet connection | Download Docker packages and images |
| Terminal | Execute Docker commands |
| `sudo` privileges | Install and manage Docker |
| Web browser | Verify the deployed web application |

> **Note:** Docker is written primarily in Go, but it is not a programming language or a single application. It is a collection of tools and services for containerization.

---

## 5. Installation of Docker on Ubuntu

We will use Docker's **official **APT** repository** rather than an unofficial installation script.

### Step 1: Update the system

```bash sudo apt update sudo apt upgrade -y ```

### Step 2: Install required dependencies

```bash sudo apt install -y ca-certificates curl ```

### Step 3: Add Docker's official GPG key

Create the keyring directory:

```bash sudo install -m **0755** -d /etc/apt/keyrings ```

Download the Docker signing key:

```bash sudo curl -fsSL [https://download.docker.com/linux/ubuntu/gpg](https://download.docker.com/linux/ubuntu/gpg) -o /etc/apt/keyrings/docker.asc ```

Set permissions:

```bash sudo chmod a+r /etc/apt/keyrings/docker.asc ```

### Step 4: Add the Docker APT repository

```bash
echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] [https://download.docker.com/linux/ubuntu](https://download.docker.com/linux/ubuntu) \
    $(. /etc/os-release && echo *${UBUNTU_CODENAME:-$VERSION_CODENAME}*) stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Update the package lists:

```bash sudo apt update ```

### Step 5: Install Docker Engine and related components

```bash sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin ```

The packages provide:

| Package | Purpose |
|---------|---------|
| `docker-ce` | Docker Engine |
| `docker-ce-cli` | Docker command-line interface |
| `containerd.io` | Container runtime |
| `docker-buildx-plugin` | Extended image-building functionality |
| `docker-compose-plugin` | Multi-container application management |

### Step 6: Verify Docker installation

Check the Docker version:

```bash docker --version ```

Check the service:

```bash sudo systemctl status docker ```

Check the installed components:

```bash sudo docker version ```

> **Expected result:** Docker Client and Docker Server information should be displayed.

### Step 7: Enable Docker at startup

```bash sudo systemctl enable docker sudo systemctl start docker ```

Verify:

```bash sudo systemctl is-active docker ```

Expected output:

``` active ```

---

## 6. Run the First Docker Container

We will use the official `hello-world` image to verify that Docker can download an image and execute a container.

### Step 1: Execute the container

```bash sudo docker run hello-world ```

### Step 2: Understand what happened

When this command executes:

## Docker searches for the `hello-world` image locally.

## If unavailable, Docker downloads it from Docker Hub. ## Docker creates a container using the downloaded image. ## The container executes a small program. ## The program prints a success message. ## The container exits.

Expected output includes:

``` Hello from Docker! This message shows that your installation appears to be working correctly. ```

> **Installation verification:** This confirms that Docker Engine can communicate with the registry, download an image, create a container, and execute it.

---

## 7. Docker Images and Containers

These are two fundamental Docker concepts.

### Docker Image

A packaged, **read-only template** containing application files and dependencies.

### Docker Container

An **instance** created from an image, with its own runtime state and writable layer.

### 7.1 List downloaded images

```bash sudo docker images ```

This displays locally available images.

### 7.2 List running containers

```bash sudo docker ps ```

### 7.3 List all containers

```bash sudo docker ps -a ```

> The `hello-world` container will normally appear as `Exited`, because its program finishes execution immediately.

### 7.4 Download an image manually

For example, download Ubuntu:

```bash sudo docker pull ubuntu ```

Verify:

```bash sudo docker images ```

### 7.5 Run an interactive Ubuntu container

```bash sudo docker run -it ubuntu bash ```

Explanation:

| Option | Meaning |
|--------|---------|
| `run` | Creates and starts a container |
| `-i` | Keeps standard input open |
| `-t` | Allocates a terminal |
| `ubuntu` | Specifies the image |
| `bash` | Starts the Bash shell inside the container |

Inside the container, execute:

```bash cat /etc/os-release ```

This displays the Ubuntu environment inside the container.

Try:

```bash hostname ```

Exit the container:

```bash exit ```

You are now back in your host Ubuntu terminal.

---

## 8. Deploy a Web Server Using Docker

Now we will perform an actual deployment using an **Nginx container**.

This is an important part of the experiment because it demonstrates how Docker can deploy a real application without installing Nginx directly on Ubuntu.

### Step 1: Download the Nginx image

```bash sudo docker pull nginx ```

This downloads the official Nginx image from Docker Hub.

Verify:

```bash sudo docker images ```

### Step 2: Run an Nginx container

We will use host port `**8081**` to avoid conflicts with your existing Caddy and Apache configurations.

```bash
sudo docker run -d \
    --name my-nginx \
    -p **8081**:80 \
    nginx
```

Understanding the command:

| Argument | Meaning |
|----------|---------|
| `run` | Creates and starts a container |
| `-d` | Runs the container in the background |
| `--name my-nginx` | Assigns a name to the container |
| `-p 8081:80` | Maps host port 8081 to container port 80 |
| `nginx` | Specifies the image |

**Understanding port mapping:**

```
Ubuntu Host (localhost:**8081**)
        ↓
Browser sends **HTTP** request
        ↓
Docker Port Mapping (**8081** → 80)
        ↓
Nginx Container (Port 80)
        ↓
Nginx serves the web page
```

### Step 3: Verify the running container

```bash sudo docker ps ```

You should see a container named `my-nginx` with a port mapping similar to:

``` 0.0.0.0:**8081**->80/tcp ```

### Step 4: Open the website

Open your browser and visit:

``` [http://localhost:**8081**](http://localhost:**8081**) ```

You should see the default Nginx welcome page.

### Step 5: Test using curl

```bash curl -I [http://localhost:**8081**](http://localhost:**8081**) ```

Expected output:

``` **HTTP**/1.1 **200** OK Server: nginx Content-Type: text/html ```

This confirms that the Nginx application is running inside a Docker container and responding to requests from your Ubuntu host.

---

## 9. Manage Docker Containers

Docker provides commands to inspect, stop, restart, and remove containers.

### Step 1: List running containers

```bash sudo docker ps ```

### Step 2: List all containers

```bash sudo docker ps -a ```

### Step 3: View container logs

```bash sudo docker logs my-nginx ```

For continuous logs:

```bash sudo docker logs -f my-nginx ```

Press `Ctrl + C` to exit the log view.

### Step 4: Execute a command inside a running container

```bash sudo docker exec -it my-nginx bash ```

If Bash is unavailable, use:

```bash sudo docker exec -it my-nginx sh ```

Inside the container, execute:

```bash hostname cat /etc/os-release ```

Exit:

```bash exit ```

### Step 5: Stop the container

```bash sudo docker stop my-nginx ```

Verify:

```bash sudo docker ps ```

The container should no longer appear among running containers.

### Step 6: Start the container again

```bash sudo docker start my-nginx ```

Verify:

```bash sudo docker ps ```

### Step 7: Remove the container

First stop it:

```bash sudo docker stop my-nginx ```

Then remove it:

```bash sudo docker rm my-nginx ```

> The container is removed, but the downloaded Nginx image remains available locally.

### Step 8: Remove an image (optional)

```bash sudo docker rmi nginx ```

This works when no remaining container references the image.

---

## 10. Build Your Own Docker Image Using a Dockerfile

So far, we have used an existing Nginx image. Now we will create a **custom Docker image** containing our own **HTML** webpage.

This demonstrates the complete containerization workflow:

```
**HTML** source code (index.html)
        ↓
Dockerfile (Instructions for building the image)
        ↓
Docker Image (my-web-app:v1)
        ↓
Docker Container (Running application)
```

### Step 1: Create a project directory

```bash mkdir -p ~/docker-demo cd ~/docker-demo ```

### Step 2: Create an HTML webpage

```bash nano index.html ```

Insert:

```html
<!**DOCTYPE** html>
<html>
<head>
    <title>Docker Practical</title>
</head>
<body>
    <h1>Welcome to Docker!</h1>

    <h2>Custom Docker Image Demonstration</h2>

    <p>This webpage is deployed inside a Docker container.</p>

    <p>Docker makes application deployment portable.</p>

    <p>Experiment performed using Ubuntu Linux.</p>
</body>
</html>
```

Save and exit.

### Step 3: Create a Dockerfile

```bash nano Dockerfile ```

Insert:

```dockerfile **FROM** nginx:alpine

**COPY** index.html /usr/share/nginx/html/index.html

**EXPOSE** 80 ```

### Understanding the Dockerfile

| Instruction | Explanation |
|-------------|-------------|
| `FROM nginx:alpine` | Uses the lightweight Alpine-based Nginx image as the base image |
| `COPY` | Copies your HTML file into the Nginx website directory |
| `EXPOSE 80` | Documents that the containerized application listens on port 80 |

> **Note:** `**EXPOSE**` does not itself publish the port to the host. We publish it using `-p` when creating the container.

### Step 4: Build your custom Docker image

```bash sudo docker build -t my-web-app:v1 . ```

Explanation:

| Argument | Meaning |
|----------|---------|
| `build` | Builds an image from a Dockerfile |
| `-t` | Assigns a name and tag to the image |
| `my-web-app` | Image name |
| `v1` | Image version |
| `.` | Uses the current directory as the build context |

### Step 5: Verify your image

```bash sudo docker images ```

You should see:

``` **REPOSITORY**    **TAG**    **IMAGE** ID my-web-app    v1     ... ```

### Step 6: Run a container from your custom image

```bash
sudo docker run -d \
    --name my-custom-web \
    -p **8082**:80 \
    my-web-app:v1
```

> We are using host port `**8082**` to avoid conflicts with Caddy and the previous Nginx demonstration.

### Step 7: Verify the container

```bash sudo docker ps ```

### Step 8: Open your custom website

Open your browser and visit:

``` [http://localhost:**8082**](http://localhost:**8082**) ```

You should see your own **HTML** page served by Nginx inside the custom Docker container.

Test through the terminal:

```bash curl [http://localhost:**8082**](http://localhost:**8082**) ```

This completes the image-building and container-deployment demonstration.

---

## 11. Important Docker Commands

Keep these commands handy for your practical examination.

| Command | Purpose |
|---------|---------|
| `docker --version` | Display Docker version |
| `docker version` | Display client and server details |
| `docker info` | Display Docker system information |
| `docker images` | List downloaded images |
| `docker pull ubuntu` | Download an Ubuntu image |
| `docker build -t name .` | Build a Docker image |
| `docker run hello-world` | Run the test container |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker start name` | Start a stopped container |
| `docker stop name` | Stop a running container |
| `docker restart name` | Restart a container |
| `docker rm name` | Remove a container |
| `docker rmi image` | Remove an image |
| `docker logs name` | Display container logs |
| `docker exec -it name bash` | Open a shell inside a container |
| `docker inspect name` | Inspect container details |
| `docker system df` | Display Docker disk usage |

> For your installation, prefix commands with `sudo`, as in the examples above.

---

## 12. Docker Networking and Port Mapping

Docker allows containers to communicate with the host and other containers through virtual networks.

The `-p` option publishes a container port on the host.

For example:

```bash sudo docker run -d -p **8081**:80 nginx ```

Here:

- `**8081**` is the **host port**.
- `80` is the **container port**.

The browser accesses `localhost:**8081**`, while Nginx receives the request on port 80 inside the container.

This is called **port mapping** or **port publishing**.

---

## 13. Docker Volumes and Persistent Data

Containers are generally treated as disposable. If a container is removed, data stored only in its writable container layer is removed with it.

**Docker volumes** provide persistent storage that can outlive individual containers.

Create a volume:

```bash sudo docker volume create my-volume ```

List volumes:

```bash sudo docker volume ls ```

Inspect a volume:

```bash sudo docker volume inspect my-volume ```

Remove it after the experiment, once it is no longer in use:

```bash sudo docker volume rm my-volume ```

This is an additional demonstration of Docker's storage-management capabilities.

---

## 14. Docker Compose

Docker Compose is a tool for defining and running **multi-container applications** using a **YAML** configuration file.

Instead of executing several `docker run` commands, we can define the services in one file.

Verify that Docker Compose is installed:

```bash sudo docker compose version ```

### Create a Compose configuration

Inside `~/docker-demo`, create:

```bash nano compose.yaml ```

Insert:

```yaml
services:
    web:
    build: .
    container_name: compose-web
    ports:
    - ***8083**:80*
    restart: unless-stopped
```

Start the application:

```bash sudo docker compose up -d ```

Check the running containers:

```bash sudo docker compose ps ```

Open in your browser:

``` [http://localhost:**8083**](http://localhost:**8083**) ```

Stop the Compose application:

```bash sudo docker compose down ```

### What did we demonstrate?

- Docker Compose configuration
- **YAML**-based service definition
- Automatic image building
- Container creation and deployment
- Container lifecycle management

---

## 15. Common Errors and Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Cannot connect to the Docker daemon` | Docker service is not running | `sudo systemctl start docker` |
| `Permission denied` | Insufficient permissions | Use `sudo` |
| `port is already allocated` | Another process uses the host port | Choose another host port |
| `No such image` | Image is not downloaded | `sudo docker pull nginx` |
| `Conflict. Container name already in use` | Container name already exists | Remove or rename the existing container |
| `Dockerfile not found` | Incorrect working directory or filename | Check using `ls -la` |
| `No space left on device` | Insufficient disk space | Check using `df -h` and `sudo docker system df` |

### Useful diagnostic commands

Check Docker service:

```bash sudo systemctl status docker ```

Check Docker logs:

```bash sudo journalctl -u docker -n 50 ```

Check disk space:

```bash df -h ```

Check Docker storage:

```bash sudo docker system df ```

> **Security note:** Membership in the `docker` group grants highly privileged access and is effectively equivalent to root-level access on a conventional Docker Engine installation. For this practical, continue using `sudo docker` rather than changing group permissions unnecessarily. > > Also, Docker-published container ports can bypass some **UFW** firewall rules. Avoid exposing demonstration containers to untrusted networks.

---

## 16. Cleanup After the Experiment

Remove the containers created during the demonstration.

```bash sudo docker stop my-custom-web sudo docker rm my-custom-web ```

If you ran the original Nginx demonstration and have not removed it:

```bash sudo docker stop my-nginx sudo docker rm my-nginx ```

Stop the Compose application if you used it:

```bash cd ~/docker-demo sudo docker compose down ```

Check remaining containers:

```bash sudo docker ps -a ```

You can retain the downloaded images for future demonstrations.

To remove the custom image:

```bash sudo docker rmi my-web-app:v1 ```

To check remaining images:

```bash sudo docker images ```

> **Warning:** Do not run `docker system prune -a --volumes` casually; it can delete images, stopped containers, networks, and unused volumes belonging to other projects.

### Restore your previous Caddy/Apache setup

Docker can continue running alongside your web servers as long as their published ports do not conflict.

If Caddy was left running, there is no need to stop it merely because Docker is installed.

If you want to restore Apache for MantisBT:

```bash sudo systemctl stop caddy sudo systemctl start apache2 ```

> Docker's containers using ports **8081**, **8082**, or **8083** do not normally conflict with Apache on port 80.

---

## 17. Viva Questions and Answers

**Q1. What is Docker?** Docker is an open-source containerization platform used to build, package, distribute, and run applications inside containers.

**Q2. Why is Docker associated with Go?** Docker's core components, including Docker Engine and its **CLI**, are primarily implemented in Go.

**Q3. What is containerization?** Containerization is the process of packaging an application and its dependencies into an isolated environment called a container.

**Q4. What is a Docker image?** A Docker image is a read-only template containing application code, libraries, dependencies, and configuration required to create a container.

**Q5. What is a Docker container?** A Docker container is an isolated runtime instance of a Docker image.

**Q6. What is the difference between a Docker image and a container?** An image is the template, whereas a container is an instance created from that template.

**Q7. What is Docker Engine?** Docker Engine is the core containerization technology responsible for building and running containers.

**Q8. What is Docker Daemon?** Docker Daemon (`dockerd`) is the background service responsible for managing Docker images, containers, networks, and volumes.

**Q9. What is Docker Hub?** Docker Hub is a registry used to store and distribute Docker images.

****Q10**. What is a Dockerfile?** A Dockerfile is a text file containing instructions for building a Docker image.

****Q11**. What is the purpose of the `**FROM**` instruction?** It specifies the base image used to build a new Docker image.

****Q12**. What is the purpose of the `**COPY**` instruction?** It copies files and directories from the build context into the Docker image.

****Q13**. What is the difference between a virtual machine and a Docker container?**

| Virtual Machine | Docker Container |
|-----------------|------------------|
| Runs a guest operating system | Shares the host kernel |
| Requires a hypervisor | Uses a container runtime |
| Generally consumes more resources | Generally lightweight |
| Has its own OS environment | Uses isolated processes and resources |

****Q14**. What are namespaces in Docker?** Namespaces are Linux kernel features that provide isolation of resources such as processes, networking, mount points, and hostnames.

****Q15**. What are cgroups?** Control groups are Linux kernel features used to account for and limit resource usage, such as **CPU** and memory.

****Q16**. What is Docker Compose?** Docker Compose is a tool for defining and managing multi-container applications using **YAML** configuration files.

****Q17**. What is port mapping?** Port mapping connects a port on the host machine to a port inside a container.

****Q18**. What is a Docker volume?** A Docker volume is persistent storage managed by Docker that can be used by containers.

****Q19**. What does `docker run` do?** It creates and starts a new container from the specified image.

****Q20**. What is the difference between `docker stop` and `docker rm`?**
- `docker stop` stops a running container.
- `docker rm` removes a stopped container.

****Q21**. What is the difference between `docker pull` and `docker push`?**
- `docker pull` downloads an image from a registry.
- `docker push` uploads an image to a registry.

****Q22**. What does the `-d` option mean?** It runs a container in detached mode, meaning it operates in the background.

****Q23**. What is the purpose of `docker exec`?** It executes a command inside an already-running container.

****Q24**. Can multiple containers run simultaneously?** Yes. Multiple containers can run simultaneously, provided sufficient system resources are available and their network and port configurations do not conflict.

****Q25**. Does Docker require a separate operating system for each container?** No. Linux containers share the host Linux kernel while maintaining process and resource isolation.

---

## 18. Result

Docker was **successfully installed and configured** on Ubuntu Linux.

The following activities were demonstrated:

## Installation and configuration of Docker Engine.

## Verification of Docker Client and Docker Server. ## Execution of the `hello-world` container. ## Downloading and managing Docker images. ## Running an interactive Ubuntu container. ## Deploying an Nginx web server inside a container. ## Mapping host ports to container ports. ## Creating a custom Docker image using a Dockerfile. ## Running and managing custom containers. ## Demonstrating persistent storage using Docker volumes. ## Understanding Docker Compose and multi-container deployment.

**Conclusion:** The experiment demonstrated Docker as a Go-based containerization platform for building, deploying, and managing Linux containers. It illustrated how applications can be packaged into portable images and executed in isolated environments without requiring a separate guest operating system for every application.

---

## 19. Quick Practical Examination Checklist

- [ ] Install Docker Engine and required plugins
- [ ] Verify Docker version and service status
- [ ] Run the `hello-world` container
- [ ] Download and inspect an Ubuntu image
- [ ] Run an interactive Ubuntu container
- [ ] Deploy Nginx using Docker
- [ ] Verify host-to-container port mapping
- [ ] Build a custom image using Dockerfile
- [ ] Run the custom web application
- [ ] Demonstrate Docker Compose
- [ ] Inspect, stop, and remove containers

---

## 20. Final Commands to Remember

These are the most important commands to reproduce during your practical examination.

```bash # Verify Docker docker --version sudo systemctl status docker

# Run test container

sudo docker run hello-world

# Download an image

sudo docker pull ubuntu

# Run interactive container

sudo docker run -it ubuntu bash

# List images and containers

sudo docker images sudo docker ps -a

# Run Nginx web server

sudo docker run -d --name my-nginx -p **8081**:80 nginx

# Test website

curl -I [http://localhost:**8081**](http://localhost:**8081**)

# Build custom image

sudo docker build -t my-web-app:v1 .

# Run custom container

sudo docker run -d --name my-custom-web -p **8082**:80 my-web-app:v1

# Inspect logs

sudo docker logs my-custom-web

# Stop and remove container

sudo docker stop my-custom-web sudo docker rm my-custom-web ```

---

**End of Experiment – Docker: Tools for Deploying Linux Containers**
