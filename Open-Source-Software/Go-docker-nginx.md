# Experiment: Demonstrate a FOSS tool using Docker, build its Docker image, push the image, and run a container

For this experiment, we will use Nginx, an open-source web server, as the **FOSS** tool.

We will perform the complete Docker workflow:

## Install and verify Docker.

## Demonstrate Nginx as a FOSS tool. ## Create a custom webpage for Nginx. ## Write a `Dockerfile` to package Nginx and the webpage into a Docker image. ## Build the Docker image. ## Run a container from the newly created image. ## Test the running container. ## Push the image to Docker Hub. ## Pull the pushed image and run a container from it.

Why Nginx? It is a genuine open-source tool, has an official Docker base image, and can be demonstrated through a browser. We will use host port `**8082**` so that it does not interfere with your existing Caddy setup on port `**8080**` or Apache on port `80`.

## 1. Aim and software selected

Aim: To demonstrate an open-source tool, package it into a Docker image, publish the image to Docker Hub, and run a container using the published image.

Selected **FOSS** tool: **NGINX** Open Source.

**NGINX** is an **HTTP** web server and reverse proxy distributed under a 2-clause **BSD** license. We will use it to serve a custom **HTML** webpage from inside a Docker container.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://nginx.org\&sz=32](https://www.google.com/s2/favicons?domain=https://nginx.org\&sz=32))

Nginx+1

## 2. Understand the workflow

**NGINX** + custom **HTML** webpage

Our **FOSS** application and webpage

Dockerfile

Instructions for packaging the application

Docker image

Our custom, reusable image

### Docker Hub

Publish the image to a registry

Pull image → Run container

Download the published image and launch **NGINX**

An image is the packaged template; a container is a running instance of that image. Docker's documented workflow is to build, tag, authenticate, and push an image to a registry.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://docs.docker.com\&sz=32](https://www.google.com/s2/favicons?domain=https://docs.docker.com\&sz=32))

Docker Docs+1

## 3. Prerequisites and Docker verification

Open a terminal on Ubuntu.

First, check available disk space. Docker images consume storage, so this is worth checking before downloading them.

``` df -h / ```

Check whether Docker is installed:

``` docker --version ```

Check whether the Docker service is running:

``` sudo systemctl status docker ```

If Docker is installed but inactive:

``` sudo systemctl start docker sudo systemctl enable docker ```

Verify Docker can communicate with its daemon:

``` sudo docker version sudo docker info ```

Run a test container:

``` sudo docker run hello-world ```

Expected verification

You should see a message beginning with:

``` Hello from Docker! This message shows that your installation appears to be working correctly. ```

If `docker --version` reports that the command is not found, Docker still needs to be installed. You can use the Docker installation procedure from the previous Docker practical.

## 4. Demonstrate the FOSS tool: NGINX

We will create a custom webpage and serve it using **NGINX**.

Create a working directory:

``` mkdir -p ~/nginx-foss-demo cd ~/nginx-foss-demo ```

Create an **HTML** file:

``` nano index.html ```

Paste the following content:

```
<!**DOCTYPE** html>
<html>
<head>
    <title>**NGINX** **FOSS** Demonstration</title>
</head>
<body>
    <h1>**NGINX** Open Source Web Server</h1>

    <h2>**FOSS** Tool Demonstration using Docker</h2>

    <p>**NGINX** is an open-source **HTTP** web server.</p>

    <p>This webpage is being served from a Docker container.</p>

    <p>The Docker image was created as part of a practical experiment.</p>

    <p>Application: **NGINX**</p>
    <p>Container Platform: Docker</p>
</body>
</html>
```

Save with `Ctrl+O`, press Enter, and exit with `Ctrl+X`.

Check the file:

``` cat index.html ```

This **HTML** file will be copied into the **NGINX** image and served as its default webpage.

## 5. Create the Dockerfile

In the same directory, create a file named `Dockerfile` (capital D, no extension):

``` nano Dockerfile ```

Add:

``` **FROM** nginx:alpine

**COPY** index.html /usr/share/nginx/html/index.html

**EXPOSE** 80 ```

Save and exit.

Explanation of each instruction:

| Instruction           | Purpose                                                                |
| --------------------- | ---------------------------------------------------------------------- |
| `FROM nginx:alpine`   | Uses the official NGINX image based on Alpine Linux as the base image. |
| `COPY index.html ...` | Copies our custom webpage into NGINX's default web root.               |
| `EXPOSE 80`           | Documents that NGINX listens on port 80 inside the container.          |

`**EXPOSE**` does not itself publish a port on your Ubuntu machine. We will publish the port using `-p` when running the container.

Verify your files:

``` ls -l ```

Expected files:

``` Dockerfile index.html ```

## 6. Build the Docker image

Run this command from inside `~/nginx-foss-demo`:

``` sudo docker build -t nginx-foss-demo:v1 . ```

Explanation:

- `docker build` builds an image from a Dockerfile.
- `-t` assigns a name and tag.
- `nginx-foss-demo` is the image name.
- `v1` is the image version.
- `.` specifies the current directory as the build context.

Verify that the image has been created:

``` sudo docker images ```

You should see an entry similar to:

``` **REPOSITORY**       **TAG**       **IMAGE** ID       **CREATED**         **SIZE** nginx-foss-demo  v1        <image-id>     moments ago     ... ```

The actual image ID and size will differ.

You can also inspect its build history:

``` sudo docker image history nginx-foss-demo:v1 ```

This demonstrates that your custom image was built using the **NGINX** base image and your Dockerfile instructions.

## 7. Run a container from the newly created image

Now launch a container using the image you just built:

```
sudo docker run -d \
    --name nginx-foss-container \
    -p **8082**:80 \
    nginx-foss-demo:v1
```

Explanation:

| Option               | Meaning                                     |
| -------------------- | ------------------------------------------- |
| `-d`                 | Runs the container in the background.       |
| `--name`             | Assigns a name to the container.            |
| `-p 8082:80`         | Maps Ubuntu port 8082 to container port 80. |
| `nginx-foss-demo:v1` | The image used to create the container.     |

Check the running container:

``` sudo docker ps ```

You should see `nginx-foss-container` with a port mapping similar to:

``` 0.0.0.0:**8082**->80/tcp ```

Test the webpage from your terminal:

``` curl [http://localhost:**8082**](http://localhost:**8082**) ```

You should see the **HTML** content you created.

Open the following address in your browser:

[http://localhost:**8082**](http://localhost:**8082**?utm_source=chatgpt.com)

[Exploring Microsoft Radius Application Platform - The New Stack](https://images.openai.com/static-rsc-4/TVh8NxOjrWasvQG3Ae95i_dL5bEu1nzCiftb6WYyr_LjVr4xiLzAtNVMkOMzC6ltoVuIbgWdRjISZ7WqIkfxo7zjjKHoeRP3LtK6wQOdnmlLpvhqERsg61q_SmMtQ8oMgSVNPldOcUffitxZS8h-BHqaUXWQmQKL24qPYpJdOz0?purpose=inline)

Your browser should display your custom **NGINX** **FOSS** demonstration webpage, not necessarily the default **NGINX** welcome page shown in the illustrative image.

Additional container checks:

``` sudo docker logs nginx-foss-container sudo docker inspect nginx-foss-container ```

At this point, you have successfully built an image and run a container from it locally.

## 8. Prepare your Docker Hub account

To push your image, you need a Docker Hub account.

## Open [Docker Hub](https://hub.docker.com/?utm_source=chatgpt.com).

## Sign in or create an account. ## Note your exact Docker Hub username. ## Create a repository named `nginx-foss-demo`. ## Set its visibility to Public if you want others to be able to pull your image without authentication.

[Running Python on Docker - Earthly Blog](https://images.openai.com/static-rsc-4/kccudg6_wY4dQAFtHXdX4Lpzb_WyU4v8WWWZ9tOrd51LErSFblAoX7MVCOQy_pMxic7gMoSTzGDurOcdSmyqoTDhqGL8cnCQPG6nO8IcKT59VyMNIf1mowTIwbJcX7b1cGEUH6HgxONMqso1kWXDfExwt0Sr8FPUjMDg35devzY?purpose=inline)

The final image name must follow this format:

``` DOCKERHUB_USERNAME/nginx-foss-demo:v1 ```

Replace `DOCKERHUB_USERNAME` with your actual username. Do not use your email address unless it is also your Docker Hub username.

## 9. Log in to Docker Hub

In your terminal, set your Docker Hub username:

``` DOCKERHUB_USER=*your_dockerhub_username* ```

For example, if your username were `student123`, the command would be:

``` DOCKERHUB_USER=*student123* ```

Now log in:

``` sudo docker login --username *$DOCKERHUB_USER* ```

Docker will prompt for your credentials. Use a Docker Hub access token if prompted for a password; do not share your password or token.

Expected successful output:

``` ### Login Succeeded ```

## 10. Tag your image for Docker Hub

Currently, your local image is named:

``` nginx-foss-demo:v1 ```

Docker Hub requires the image name to include your Docker Hub username and repository name.

Run:

```
sudo docker tag nginx-foss-demo:v1 \
    *$DOCKERHUB_USER/nginx-foss-demo:v1*
```

Verify:

``` sudo docker images ```

You should now see both tags pointing to the same image ID:

``` **REPOSITORY**                         **TAG** nginx-foss-demo                    v1 your_username/nginx-foss-demo      v1 ```

Tagging does not create a second independent image; it adds another name to the same image.

## 11. Push the Docker image to Docker Hub

Now upload the image:

``` sudo docker push *$DOCKERHUB_USER/nginx-foss-demo:v1* ```

Docker will upload the image layers to Docker Hub.

Expected result

The output should finish with a digest similar to:

``` v1: digest: sha256:<image-digest> size: <size> ```

The actual digest will be different.

You can verify the image by opening Docker Hub:

[View your Docker Hub repositories](https://hub.docker.com/repositories?utm_source=chatgpt.com)

Open `nginx-foss-demo` and check the Tags section. You should find the `v1` tag.

The image is now published and can be shared with other Docker users.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://docs.docker.com\&sz=32](https://www.google.com/s2/favicons?domain=https://docs.docker.com\&sz=32))

Docker Docs+1

## 12. Pull the image from Docker Hub

We will now verify that the image can be downloaded from Docker Hub independently of the original local build.

First, stop and remove the original container:

``` sudo docker stop nginx-foss-container sudo docker rm nginx-foss-container ```

Remove the two local tags of your custom image:

``` sudo docker image rm nginx-foss-demo:v1 sudo docker image rm *$DOCKERHUB_USER/nginx-foss-demo:v1* ```

If Docker reports that an image is still being used by a container, check `sudo docker ps -a` and remove the relevant container first.

Now download the published image:

``` sudo docker pull *$DOCKERHUB_USER/nginx-foss-demo:v1* ```

Expected output will indicate that the image layers have been downloaded or are already present.

Verify:

``` sudo docker images ```

You should see:

``` **REPOSITORY**                         **TAG** your_username/nginx-foss-demo      v1 ```

This step demonstrates that the image is available from Docker Hub and can be retrieved onto a machine without rebuilding it locally.

## 13. Run a container using the pulled image

Now create a new container using the image pulled from Docker Hub:

```
sudo docker run -d \
    --name nginx-foss-from-hub \
    -p **8082**:80 \
    *$DOCKERHUB_USER/nginx-foss-demo:v1*
```

Verify that the container is running:

``` sudo docker ps ```

Test the application:

``` curl [http://localhost:**8082**](http://localhost:**8082**) ```

Open your browser:

\*\*http\://localhost:**8082**\*\*

You should see the same custom webpage that you saw earlier.

Final demonstration

You have now completed the full sequence:

- Created a custom **NGINX** Docker image.
- Ran a container using the locally built image.
- Tagged and pushed the image to Docker Hub.
- Removed the local custom image.
- Pulled the published image from Docker Hub.
- Ran a new container using the pulled image.

This is the important distinction in the experiment: the final container is created from the image retrieved from Docker Hub, not from the original local build.

## 14. Useful Docker commands for your practical demonstration

| Operation               | Command                                                          |
| ----------------------- | ---------------------------------------------------------------- |
| List images             | `sudo docker images`                                             |
| List running containers | `sudo docker ps`                                                 |
| List all containers     | `sudo docker ps -a`                                              |
| View container logs     | `sudo docker logs nginx-foss-from-hub`                           |
| Inspect image           | `sudo docker image inspect *$DOCKERHUB_USER/nginx-foss-demo:v1*` |
| Stop container          | `sudo docker stop nginx-foss-from-hub`                           |
| Start stopped container | `sudo docker start nginx-foss-from-hub`                          |
| Remove container        | `sudo docker rm -f nginx-foss-from-hub`                          |
| Pull published image    | `sudo docker pull *$DOCKERHUB_USER/nginx-foss-demo:v1*`          |

## 15. Troubleshooting

| Problem                          | Solution                                                                                |
| -------------------------------- | --------------------------------------------------------------------------------------- |
| Docker daemon not running        | `sudo systemctl start docker`                                                           |
| Permission denied                | Use `sudo` with Docker commands.                                                        |
| Port 8082 already allocated      | Use `-p 8084:80` and open `[http://localhost:8084`.](http://localhost:8084`.)                                      |
| Docker Hub authentication failed | Verify your username and access token; log in again.                                    |
| Push access denied               | Check that the image tag contains your correct Docker Hub username and repository name. |
| Image not found                  | Check `sudo docker images` and verify the image tag.                                    |
| Container name already exists    | Inspect `sudo docker ps -a`; remove the old test container if appropriate.              |
| Webpage not loading              | Check `sudo docker ps`, `sudo docker logs nginx-foss-from-hub`, and the port mapping.   |

## 16. Viva questions and answers

1\. What is **FOSS**?

**FOSS** stands for Free and Open Source Software. Its source code is available under a license that permits users to use, study, modify, and redistribute the software under the license terms.

2\. What is **NGINX**?

**NGINX** is an open-source web server that can also work as a reverse proxy, load balancer, and **HTTP** cache.

3\. What is Docker?

Docker is a platform for building, packaging, distributing, and running applications in containers.

4\. What is a Docker image?

A Docker image is a packaged, read-only template containing the application and the files and dependencies required to run it.

5\. What is a Docker container?

A container is an isolated running instance of a Docker image.

6\. What is a Dockerfile?

A Dockerfile is a text file containing instructions used to build a Docker image.

7\. What is the purpose of the `**FROM**` instruction?

It specifies the base image on which the new image will be built.

8\. What is the purpose of the `**COPY**` instruction?

It copies files from the build context into the image.

9\. What is the difference between `**EXPOSE**` and `-p`?

`**EXPOSE**` documents the container's listening port. `-p` actually publishes a container port on the host.

10\. What is Docker Hub?

Docker Hub is a registry used to store, distribute, and share Docker images.

11\. What is the purpose of `docker build`?

It builds an image using the instructions in a Dockerfile.

12\. What is the purpose of `docker tag`?

It assigns an additional name and tag to an existing image, often to prepare it for publishing.

13\. What is the purpose of `docker push`?

It uploads an image to a container registry.

14\. What is the purpose of `docker pull`?

It downloads an image from a container registry.

15\. What does `-d` mean in `docker run`?

It runs the container in detached mode, in the background.

16\. What does `-p **8082**:80` mean?

It maps port **8082** on the host machine to port 80 inside the container.

17\. Why did we use Alpine in the Dockerfile?

Alpine is a lightweight Linux distribution, commonly used to create smaller container images.

18\. Can multiple containers run from one image?

Yes. Multiple containers can be created from the same image.

19\. Does deleting a container delete its image?

No. Containers and images are separate Docker objects.

20\. Why do we pull the image after pushing it?

To verify that the published image can be retrieved from Docker Hub and used to create a new container.

## 17. Result

Result: The open-source **NGINX** web server was successfully packaged into a custom Docker image using a Dockerfile. The image was tagged with the Docker Hub repository name, pushed to Docker Hub, pulled back from the registry, and used to run a new Docker container. The deployed webpage was verified using a web browser and `curl`.

## 18. Practical completion checklist

Use this to track your actual execution. Mark an item only after you have verified it on your machine.

Experiment progress

## 0/15

Docker installed and service running

hello-world container executed successfully

**NGINX** **HTML** webpage created

Dockerfile created

Custom image built successfully

Container started from local image

Webpage verified at localhost:**8082**

Docker Hub account and repository prepared

Docker Hub login successful

Image tagged with Docker Hub username

Image pushed successfully

Local custom image removed

Image pulled from Docker Hub

New container started from pulled image

Final webpage verified

Reset checklist

Official references

- [Docker: Build, tag, and publish an image](https://docs.docker.com/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/?utm_source=chatgpt.com)
- [Docker: Image push command](https://docs.docker.com/reference/cli/docker/image/push/?utm_source=chatgpt.com)
- [**NGINX** official website](https://nginx.org/en/?utm_source=chatgpt.com)

Important: The commands above are instructions for your terminal; the image has not been built or pushed yet. When you reach the Docker Hub step, replace the username placeholder with your actual Docker Hub username.
