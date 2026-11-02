# Experiment: Deploy a Bug Tracking Tool using Docker, Build Its Image, and Push It to Docker Hub

## 1. Aim

To demonstrate a **FOSS** bug tracking tool, deploy it using Docker, create a custom Docker image, push the image to Docker Hub, pull the published image, and run a container using that image.

## 2. Tool selected: MantisBT

[MantisBT Avaliações **2026**: Detalhes, Preços e Recursos | G2](https://images.openai.com/static-rsc-4/Fo-BD9NEAJmWfk1OtugHKkjOKP4IlDcHpIZoJk4nwAzlWihcjj5Sv1roMW9xsO3bH7d0sV9kOlLkG23Ai7apq21l8kUWfXhTwO56EN_rKTtRCJH3-VBwGOHT_HRPn3--7JhR4JQUgYC-udgwXsLsIA_wyfCvvFI_RZuH8pXUGeE?purpose=inline)

MantisBT

Open-source, web-based issue and bug tracking system.

[Official website](https://[www.mantisbt.org/?utm_source=chatgpt.com](https://www.mantisbt.org/?utm_source=chatgpt.com)) · [Source code](https://github.com/mantisbt/mantisbt?utm_source=chatgpt.com)

MantisBT allows software development teams to report bugs, assign issues to developers, track their status, add comments, and manage project defects.

We will use MantisBT because it is a genuine **FOSS** bug tracking application and is also relevant to your earlier MantisBT practical.

What we will demonstrate:

- Install and configure MantisBT using Docker.
- Create a custom Docker image containing MantisBT.
- Run the application with a database.
- Log in and create a sample bug report.
- Push the custom image to Docker Hub.
- Pull the image and launch a fresh container from it.

## 3. Understand the architecture

MantisBT is a **PHP** web application, so it requires a web server/**PHP** runtime and a database.

Web browser

User reports and tracks bugs

MantisBT Docker container

Apache + **PHP** + MantisBT application

MariaDB Docker container

Stores users, projects, bug reports, comments and settings

### Docker Hub

Stores the custom MantisBT image for publishing and distribution

Important distinction: We will create and push the MantisBT application image. MariaDB will use its existing official image; you do not need to build a separate database image.

## 4. Prerequisites

Before starting, check that Docker and Docker Compose are available:

``` sudo docker --version sudo docker compose version sudo systemctl is-active docker ```

Check available disk space:

``` df -h / ```

The application and database images will require additional storage.

Port selection: We will use port `**8989**` on your Ubuntu machine. This keeps this Docker deployment separate from your earlier Apache/MantisBT and Caddy configurations.

Check that the port is available:

``` sudo ss -ltnp | grep ':**8989**' ```

If there is no output, the port is available.

## 5. Create the project directory

``` mkdir -p ~/mantisbt-docker-practical cd ~/mantisbt-docker-practical ```

Our directory structure will be:

``` mantisbt-docker-practical/ │ ├── Dockerfile ├── docker-practical.txt ├── compose.yaml ├── .env ├── config/ └── custom/ ```

Create the directories:

``` mkdir -p config custom ```

## 6. Create a custom Docker image for MantisBT

We will use the community-maintained `xlrl/mantisbt` image as the base. It packages MantisBT with its web-server/**PHP** runtime. We will create our own derived image, add identifying metadata, and publish that image under our Docker Hub account.

The selected base version is `2.28.4-2`.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://github.com\&sz=32](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32))

GitHub+1

Create the Dockerfile:

``` nano Dockerfile ```

Add:

``` **FROM** xlrl/mantisbt:2.28.4-2

**LABEL** org.opencontainers.image.title=*MantisBT **FOSS** Bug Tracker* **LABEL** org.opencontainers.image.description="Custom Docker image for the MantisBT bug tracking practical* **LABEL** org.opencontainers.image.source=*[https://github.com/mantisbt/mantisbt*](https://github.com/mantisbt/mantisbt*)

**COPY** docker-practical.txt /usr/share/doc/mantisbt-practical.txt ```

Create the additional information file:

``` nano docker-practical.txt ```

Add:

``` MantisBT - **FOSS** Bug Tracking Tool

Purpose: Demonstrate bug tracking using MantisBT inside Docker.

Features:
- Report software defects
- Assign bugs to users
- Set bug priority and severity
- Track issue status
- Add comments and monitor progress

Deployment: Docker container with MariaDB database. ```

Save both files.

Explanation of the Dockerfile:

| Instruction | Explanation                                               |
| ----------- | --------------------------------------------------------- |
| `FROM`      | Uses the existing MantisBT application image as the base. |
| `LABEL`     | Adds metadata describing our custom image.                |
| `COPY`      | Adds our practical information file to the image.         |

This produces a custom MantisBT image while retaining the tested application runtime from the base image.

## 7. Configure Docker Compose

MantisBT needs a database to store its projects, users, and bug reports. It supports MySQL and MariaDB; we will use MariaDB.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://mantisbt.org\&sz=32](https://www.google.com/s2/favicons?domain=https://mantisbt.org\&sz=32))

mantisbt.org+1

First, create a `.env` file:

``` nano .env ```

Add the following, replacing the username with your actual Docker Hub username:

``` DOCKERHUB_USER=your_dockerhub_username ```

Now create the Compose configuration:

``` nano compose.yaml ```

Add:

```
services:
    mantisbt:
    build: .
    image: ${DOCKERHUB_USER}/mantisbt-foss-demo:v1
    container_name: mantisbt-web

    ports:
    - ***8989**:80*

    environment:
    MANTIS_TIMEZONE: Asia/Kolkata
    MANTIS_ENABLE_ADMIN: *1*

    volumes:
    - ./config:/var/www/html/config
    - ./custom:/var/www/html/custom

    depends_on:
    db:
    condition: service_healthy

    restart: unless-stopped

    db:
    image: mariadb:10.11
    container_name: mantisbt-db

    environment:
    MARIADB_ROOT_PASSWORD: rootpass123
    MARIADB_DATABASE: bugtracker
    MARIADB_USER: mantisbt
    MARIADB_PASSWORD: mantispass123

    volumes:
    - mantis-db-data:/var/lib/mysql

    healthcheck:
    test: [*CMD*, *healthcheck.sh*, *--connect*, *--innodb_initialized*]
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 30s

    restart: unless-stopped

volumes: mantis-db-data: ```

The credentials here are for a local classroom demonstration only. Do not use these passwords for a public or production deployment.

### Understand the Compose configuration

| Configuration    | Purpose                                            |
| ---------------- | -------------------------------------------------- |
| `mantisbt`       | Application service                                |
| `db`             | MariaDB database service                           |
| `build: .`       | Builds our custom image from the current directory |
| `image:`         | Gives the image its Docker Hub repository name     |
| `8989:80`        | Maps host port 8989 to container port 80           |
| `depends_on`     | Waits for the database health check                |
| `mantis-db-data` | Persists database data                             |
| `./config`       | Persists MantisBT configuration                    |
| `./custom`       | Stores custom MantisBT files                       |

The image contains the application. The Compose file supplies the database service, runtime settings, and persistent storage.

## 8. Set directory permissions

The MantisBT web server runs as `www-data` (**UID**/**GID** 33) in this image. The configuration directories must be writable by that user.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://github.com\&sz=32](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32))

GitHub

Run:

``` sudo chown -R 33:33 config custom ```

Verify:

``` ls -ld config custom ```

## 9. Build the custom Docker image

Make sure you are in:

``` cd ~/mantisbt-docker-practical ```

Build the image:

``` sudo docker compose build --pull ```

This will download the base MantisBT image if necessary and build your custom image using the Dockerfile.

Verify:

``` sudo docker images ```

You should see an image with a name similar to:

``` **REPOSITORY**                         **TAG** your_username/mantisbt-foss-demo   v1 ```

Inspect its metadata:

``` sudo docker image inspect \ "$(< .env sed -n 's/^DOCKERHUB_USER=//p')/mantisbt-foss-demo:v1" ```

If that command is inconvenient, use the full image name directly:

``` sudo docker image inspect your_username/mantisbt-foss-demo:v1 ```

Replace `your_username` with your Docker Hub username.

## 10. Start the MantisBT and database containers

Run:

``` sudo docker compose up -d ```

This starts both services in the background.

Check their status:

``` sudo docker compose ps ```

You should see two services:

- `mantisbt-web`
- `mantisbt-db`

Check the application logs:

``` sudo docker logs mantisbt-web ```

Check database logs:

``` sudo docker logs mantisbt-db ```

Wait until the database is healthy before proceeding with the web installation.

## 11. Open MantisBT in your browser and install it

Open:

[Open MantisBT installation page](http://localhost:**8989**/admin/install.php?utm_source=chatgpt.com)

Or enter this address manually:

``` [http://localhost:**8989**/admin/install.php](http://localhost:**8989**/admin/install.php) ```

The MantisBT installation page should appear.

[Mantis - Installation](https://images.openai.com/static-rsc-4/Dq3KTjTLRmu-6Vey_GDGUijoILEUnJEP52hoJYokVHmfDVRlyVPJRFKEZqGjB15yw-zy14bQEqKBoWgCW9h9UmQ-1eu-5mFkiB4nyj2PdaJG2_E3I4QM4Ri9RFEiyD-TEYtc7iG81Gah1WZF5FiWfvSEwgSVhpGFHl8CUDnipVg?purpose=inline)

The installer asks for database connection details. Enter the following values:

| Installation field                   | Value           |
| ------------------------------------ | --------------- |
| Database type                        | MySQL / MySQLi  |
| Database hostname                    | `db`            |
| Database username                    | `mantisbt`      |
| Database password                    | `mantispass123` |
| Database name                        | `bugtracker`    |
| Admin username for database creation | `root`          |
| Admin password for database creation | `rootpass123`   |

Why is the hostname `db` and not `localhost`?

Because the database runs in a separate Docker container. Docker Compose creates an internal network and makes services accessible using their service names. Here, the database service is named `db`.

Click Install/Upgrade Database.

If installation succeeds, MantisBT will create its database tables and configuration.

## 12. Demonstrate actual bug tracking

Open:

[Open MantisBT](http://localhost:**8989**?utm_source=chatgpt.com).

The default administrator credentials for this image are:

| Field    | Value           |
| -------- | --------------- |
| Username | `administrator` |
| Password | `root`          |

These are initial demonstration credentials, not production credentials. Change the administrator password after logging in.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://github.com\&sz=32](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32))

GitHub

### Create a project

## Navigate to Manage.

## Open Manage Projects. ## Select Create New Project. ## Enter the project name:

``` ### Docker Practical Project ```

5\. Save the project.

### Report a bug

## Select Report Issue.

## Select `Docker Practical Project`. ## Enter the following sample issue details:

| Field              | Value                                                                                    |
| ------------------ | ---------------------------------------------------------------------------------------- |
| Category           | General                                                                                  |
| Summary            | Login page validation fails for empty password                                           |
| Description        | The login form accepts an empty password without displaying a proper validation message. |
| Steps to reproduce | Open the login page, enter a username, leave the password empty, and click Login.        |
| Severity           | Minor                                                                                    |
| Priority           | Normal                                                                                   |

4\. Click Submit Report.

[How to get involved with open source if you're a cat | Opensource.com](https://images.openai.com/static-rsc-4/-koYQE8MiEjXjbXvdkqXx3P15qhbEuiEZ9glXrchAJ_W0FVu7PltDtFWB-WDm0ZZMTZen8er3Ri3QlndOYNj1lSzOG5aWDPh9MYf7Z5KKmcT8qM0yBhWCHuAhVK7IRCDZIiZ312O0G0X7hhsae5Okv1mOA2-QMmErGcuywMl5TE?purpose=inline)

### Verify the bug

Open View Issues.

You should see the newly reported issue in the list.

Open it to demonstrate:

- Issue ID.
- Summary and description.
- Reporter.
- Priority and severity.
- Status.
- History and comments.

This is the actual use of the **FOSS** bug tracking application, rather than simply showing that its container is running.

## 13. Prepare Docker Hub

Open [Docker Hub](https://hub.docker.com/?utm_source=chatgpt.com) and sign in.

Create a repository named:

``` mantisbt-foss-demo ```

Set the repository to Public if you want other people to pull the image without authentication.

Load your username from the `.env` file:

``` cd ~/mantisbt-docker-practical

set -a source .env set +a

echo *$DOCKERHUB_USER* ```

Check that this prints your actual Docker Hub username.

## 14. Log in and push the custom image

Log in:

``` sudo docker login --username *$DOCKERHUB_USER* ```

Use your Docker Hub access token if Docker requests a password.

Now push the custom image:

``` sudo docker push *$DOCKERHUB_USER/mantisbt-foss-demo:v1* ```

Wait for the upload to finish.

A successful push should end with output similar to:

``` v1: digest: sha256:<image-digest> size: <size> ```

The digest and size will be different on your system.

Verify that the `v1` tag appears in your Docker Hub repository.

Your published image name will be:

``` your_dockerhub_username/mantisbt-foss-demo:v1 ```

This is the image you will use for the final container demonstration.

## 15. Remove the local application container and image

To prove that the published image can be retrieved independently, stop the Compose deployment:

``` sudo docker compose down ```

Important: Do not add `-v` to this command. The database volume must be preserved so your project and sample bug report remain available.

Remove the local custom image:

``` sudo docker image rm *$DOCKERHUB_USER/mantisbt-foss-demo:v1* ```

Check:

``` sudo docker images ```

The custom image should no longer appear locally.

The database volume and the `config/` directory are still present.

## 16. Pull the image from Docker Hub

Download the image you published:

``` sudo docker pull *$DOCKERHUB_USER/mantisbt-foss-demo:v1* ```

Verify:

``` sudo docker images ```

You should now see:

``` **REPOSITORY**                                  **TAG** your_username/mantisbt-foss-demo           v1 ```

This verifies that the custom image can be downloaded from Docker Hub.

## 17. Run a new container from the pulled image

Start the application again without rebuilding the image:

``` sudo docker compose up -d --no-build ```

The `--no-build` option is important: it tells Docker Compose to use the image already pulled from Docker Hub instead of rebuilding it from the local Dockerfile.

Verify both containers:

``` sudo docker compose ps ```

Check the application logs:

``` sudo docker logs mantisbt-web ```

Open MantisBT:

[Open the MantisBT application](http://localhost:**8989**?utm_source=chatgpt.com)

Log in and open View Issues. Your previously created project and sample bug should still be present because the database volume was preserved.

Final verification

You have demonstrated that the image published to Docker Hub can be pulled and used to run the MantisBT application again.

## 18. Important Docker commands for the practical

| Operation                | Command                                                             |
| ------------------------ | ------------------------------------------------------------------- |
| Build custom image       | `sudo docker compose build`                                         |
| Start application        | `sudo docker compose up -d`                                         |
| List containers          | `sudo docker ps`                                                    |
| List all containers      | `sudo docker ps -a`                                                 |
| List images              | `sudo docker images`                                                |
| View application logs    | `sudo docker logs mantisbt-web`                                     |
| View database logs       | `sudo docker logs mantisbt-db`                                      |
| Stop deployment          | `sudo docker compose down`                                          |
| Push image               | `sudo docker push *$DOCKERHUB_USER/mantisbt-foss-demo:v1*`          |
| Pull image               | `sudo docker pull *$DOCKERHUB_USER/mantisbt-foss-demo:v1*`          |
| Start using pulled image | `sudo docker compose up -d --no-build`                              |
| Inspect image            | `sudo docker image inspect *$DOCKERHUB_USER/mantisbt-foss-demo:v1*` |

If you open a new terminal, reload the username variable before using commands that refer to it:

``` cd ~/mantisbt-docker-practical

set -a source .env set +a ```

## 19. Troubleshooting

| Problem                             | Possible solution                                                              |
| ----------------------------------- | ------------------------------------------------------------------------------ |
| Docker daemon not running           | `sudo systemctl start docker`                                                  |
| Docker Compose command not found    | Install the Docker Compose plugin.                                             |
| Port 8989 already in use            | Change the mapping to `8990:80` and open `[http://localhost:8990`.](http://localhost:8990`.)              |
| MantisBT cannot connect to database | Check that hostname is `db` and the database credentials match `compose.yaml`. |
| Database is not ready               | Check `sudo docker logs mantisbt-db` and wait for its health check.            |
| Cannot write `config_inc.php`       | Run `sudo chown -R 33:33 config custom`.                                       |
| Installation page returns 404       | Check `MANTIS_ENABLE_ADMIN: *1*` and recreate the application container.       |
| Docker push access denied           | Verify Docker Hub username, repository name, and authentication.               |
| Image not found after pull          | Check the exact repository name and tag.                                       |
| Container exits unexpectedly        | Inspect `sudo docker logs mantisbt-web`.                                       |

## 20. Viva questions and answers

1\. What is a bug tracking tool?

A bug tracking tool is software used to report, assign, prioritize, monitor, and resolve defects in an application.

2\. What is MantisBT?

MantisBT is an open-source, web-based bug and issue tracking system.

3\. What is the purpose of MantisBT?

It helps development teams manage software defects throughout their development and maintenance lifecycle.

4\. What is a Docker image?

A Docker image is a packaged, read-only template used to create containers.

5\. What is a Docker container?

A container is an isolated instance of a Docker image.

6\. Why does MantisBT require a database?

It stores information such as user accounts, projects, issues, comments, and configuration.

7\. Why did we use MariaDB?

MariaDB is an open-source relational database compatible with the MySQL interface supported by MantisBT.

8\. What is Docker Compose?

Docker Compose is a tool for defining and running multi-container applications using a **YAML** configuration file.

9\. What is the purpose of `depends_on`?

It defines a dependency between services. With a health-check condition, Compose can wait for a dependency to become healthy before starting the dependent service.

10\. What is a Docker volume?

A Docker volume provides persistent storage independent of a container's lifecycle.

11\. What is the difference between `docker build` and `docker run`?

`docker build` creates an image, whereas `docker run` creates and starts a container from an image.

12\. What is the purpose of `docker push`?

It uploads an image to a container registry such as Docker Hub.

13\. What is the purpose of `docker pull`?

It downloads an image from a container registry.

14\. What is the purpose of `-p **8989**:80`?

It maps port **8989** on the host machine to port 80 inside the application container.

15\. What happens if we delete a container?

The container is removed, but its image and separately stored volumes remain unless explicitly deleted.

16\. Why did we use `docker compose down` instead of deleting individual containers?

It stops and removes the services and network defined in the Compose project together. It preserves named volumes unless `-v` is specified.

17\. Why did we use `--no-build`?

To ensure the final deployment uses the image pulled from Docker Hub rather than rebuilding the image locally.

18\. What is the difference between severity and priority in bug tracking?

Severity describes the technical impact of a defect; priority indicates how urgently it should be fixed.

19\. What is the difference between an open and a resolved issue?

An open issue is still awaiting resolution, whereas a resolved issue has been addressed according to the project's workflow.

20\. What is the purpose of Docker Hub?

Docker Hub is a registry for storing and distributing Docker images.

## 21. Result

Result: MantisBT, an open-source bug tracking tool, was deployed using Docker with MariaDB as its database. A custom Docker image was created using a Dockerfile, tagged with a Docker Hub repository name, and pushed to Docker Hub. The published image was subsequently pulled and used to run a new MantisBT container. A sample project and bug report were created to demonstrate the application's bug tracking functionality.

## 22. Final practical checklist

Experiment progress

## 0/16

Docker and Docker Compose verified

Project directory and Dockerfile created

Custom MantisBT image built

MariaDB container started and healthy

MantisBT installation completed

Logged in to MantisBT

Created a sample project

Reported and verified a sample bug

Created Docker Hub repository

Logged in to Docker Hub

Pushed custom image successfully

Stopped original deployment without deleting database volume

Removed local custom image

Pulled image from Docker Hub

Started new containers using the pulled image

Verified the application and existing bug report

Reset checklist

Important security note: The demonstration uses simple database and administrator credentials. Change the default MantisBT administrator password before using the system beyond the lab. Do not publish database credentials in a public repository. For a production deployment, disable the installation/admin directory after setup and use proper secrets and persistent backups.

Official references:

- [MantisBT official website](https://[www.mantisbt.org/?utm_source=chatgpt.com](https://www.mantisbt.org/?utm_source=chatgpt.com))
- [MantisBT source repository](https://github.com/mantisbt/mantisbt?utm_source=chatgpt.com)
- [MantisBT Docker image documentation](https://github.com/xlrl/docker-mantisbt?utm_source=chatgpt.com)
- [Docker Compose documentation](https://docs.docker.com/reference/cli/docker/compose/?utm_source=chatgpt.com)

The commands above are the procedure; the image has not been built or pushed from your machine yet.
