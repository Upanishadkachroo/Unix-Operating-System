For this experiment, build a **LAMP** (Linux, Apache, MySQL, **PHP**) stack using Docker containers, host your own **PHP** web application, connect it to a MySQL database, and publish your custom application image to Docker Hub.

I suggest creating a Student Record Management System. It will allow you to add student records and display records stored in MySQL.

We will use official Docker Hub images for **PHP**/Apache and MySQL rather than an old, bundled all-in-one **LAMP** image. This separates the web server and database into independently managed containers while still providing a complete **LAMP** stack. This follows Docker's recommended **PHP** and database containerization approach.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://docs.docker.com\&sz=32](https://www.google.com/s2/favicons?domain=https://docs.docker.com\&sz=32))

Docker Docs+2

# Experiment: Deploy a LAMP application using Docker and push the image to Docker Hub

## 1. Architecture

Web browser

[http://localhost:**8085**](http://localhost:**8085**?utm_source=chatgpt.com)

Web container

Apache + **PHP**

Custom image: student-records-lamp:1.0

Handles web requests and executes **PHP** code.

Docker bridge network · **PDO** MySQL

Database container

MySQL 8.0

Official image: mysql:8.0

Stores student records in a persistent Docker volume.

Persistent volume: mysql_data

## 2. Pull images from Docker Hub

First, check Docker and Docker Compose:

``` sudo docker --version sudo docker compose version ```

Pull the **PHP**-Apache and MySQL images:

``` sudo docker pull php:8.2-apache sudo docker pull mysql:8.0 ```

Verify:

``` sudo docker images ```

You should see images similar to:

``` **REPOSITORY**   **TAG**          **IMAGE** ID php          8.2-apache   ... mysql        8.0          ... ```

References: [**PHP** Docker Hub](https://hub.docker.com/_/php?utm_source=chatgpt.com) and [MySQL Docker Hub](https://hub.docker.com/_/mysql?utm_source=chatgpt.com).

## 3. Create the project directory

I suggest keeping this experiment in your existing **OSS** practical workspace.

``` cd ~/Unix-Operating-System/Open-Source-Software

mkdir lamp-docker-practical cd lamp-docker-practical

mkdir app ```

Your initial structure:

``` lamp-docker-practical/ ├── app/ ├── Dockerfile ├── compose.yaml └── .env ```

## 4. Create the PHP web application

We will implement a Student Record Management System.

Create the application:

``` nano app/index.php ```

Paste this code:

```

<?php $host = getenv('DB_HOST') ?: 'db'; $db   = getenv('MYSQL_DATABASE') ?: 'studentdb'; $user = getenv('MYSQL_USER') ?: 'studentuser'; $pass = getenv('MYSQL_PASSWORD');

try {
    $pdo = new **PDO**(
    *mysql:host=$host;dbname=$db;charset=utf8mb4*,
    $user,
    $pass,
    [**PDO**::ATTR_ERRMODE => **PDO**::ERRMODE_EXCEPTION]
    );

    // Create the table if it does not exist.
    $pdo->exec("
    **CREATE** **TABLE** IF **NOT** **EXISTS** students (
    id **INT** AUTO_INCREMENT **PRIMARY** **KEY**,
    name **VARCHAR**(**100**) **NOT** **NULL**,
    email **VARCHAR**(**150**) **NOT** **NULL**,
    course **VARCHAR**(**100**) **NOT** **NULL**,
    created_at **TIMESTAMP** **DEFAULT** CURRENT_TIMESTAMP
    )
    ");

    // Insert a new student.
    if ($_SERVER['REQUEST_METHOD'] === '**POST**') {
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $course = trim($_POST['course'] ?? '');

    if ($name !== '' && filter_var($email, FILTER_VALIDATE_EMAIL)
    && $course !== '') {
    $stmt = $pdo->prepare(
    "**INSERT** **INTO** students (name, email, course)
    **VALUES** (?, ?, ?)"
    );
    $stmt->execute([$name, $email, $course]);

    header(*Location: index.php*);
    exit;
    }
    }

    $students = $pdo->query(
    ***SELECT** * **FROM** students **ORDER** BY id **DESC***
    )->fetchAll(**PDO**::FETCH_ASSOC);

} catch (PDOException $e) {
    die(*Database connection failed: * .
    htmlspecialchars($e->getMessage()));
}
?>

<!**DOCTYPE** html>
<html lang=*en*>
<head>
    <meta charset=***UTF**-8*>
    <title>Student Record Management</title>
    <style>
    body {
    font-family: Arial, sans-serif;
    background: #f2f4f8;
    margin: 40px;
    }
    .container {
    max-width: 900px;
    margin: auto;
    background: white;
    padding: 25px;
    border-radius: 10px;
    }
    input {
    padding: 10px;
    margin: 5px;
    }
    button {
    padding: 10px 18px;
    background: #1769aa;
    color: white;
    border: none;
    cursor: pointer;
    }
    table {
    width: **100**%;
    border-collapse: collapse;
    margin-top: 25px;
    }
    th, td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
    }
    th {
    background: #1769aa;
    color: white;
    }
    </style>
</head>
<body>
<div class=*container*>
    <h1>Student Record Management System</h1>
    <p>Powered by Docker, Apache, **PHP** and MySQL.</p>

    <h2>Add Student</h2>

    <form method=*POST*>
    <input type=*text* name=*name*
    placeholder=*Student Name* required>

    <input type=*email* name=*email*
    placeholder=*Email* required>

    <input type=*text* name=*course*
    placeholder=*Course* required>

    <button type=*submit*>Add Student</button>
    </form>

    <h2>Student Records</h2>

    <table>
    <tr>
    <th>ID</th>
    <th>Name</th>
    <th>Email</th>
    <th>Course</th>
    </tr>

    <?php foreach ($students as $student): ?>
    <tr>
    <td><?= htmlspecialchars($student['id']) ?></td>
    <td><?= htmlspecialchars($student['name']) ?></td>
    <td><?= htmlspecialchars($student['email']) ?></td>
    <td><?= htmlspecialchars($student['course']) ?></td>
    </tr>
    <?php endforeach; ?>
    </table>
</div>
</body>
</html>

```

Save and exit.

The application:

- Connects to MySQL using **PDO**.
- Creates a `students` table automatically.
- Inserts student records using prepared statements.
- Retrieves and displays records from MySQL.

## 5. Create the Dockerfile

At the project root:

``` nano Dockerfile ```

Add:

```

**FROM** php:8.2-apache

# Install PHP extensions required for MySQL connectivity.

**RUN** docker-php-ext-install pdo pdo_mysql

# Copy the application into Apache's document root.

**COPY** app/ /var/www/html/

# Apache listens on port 80.

**EXPOSE** 80

```

This image is based on the **PHP**-Apache image pulled from Docker Hub. We install the MySQL **PDO** extensions and copy our own application into the image.

## 6. Configure database credentials

Create the `.env` file:

``` nano .env ```

Add the following:

``` MYSQL_ROOT_PASSWORD=RootLab@**2026** MYSQL_DATABASE=studentdb MYSQL_USER=studentuser MYSQL_PASSWORD=StudentLab@**2026**

DOCKERHUB_USERNAME=YOUR_DOCKERHUB_USERNAME ```

Replace the Docker Hub username with your actual username.

Do not publish this `.env` file or commit it to a public Git repository.

## 7. Create Docker Compose configuration

Create:

``` nano compose.yaml ```

Paste:

```

services:

    web:
    build:
    context: .
    dockerfile: Dockerfile
    image: ${DOCKERHUB_USERNAME}/student-records-lamp:1.0
    container_name: lamp-web
    ports:
    - ***8085**:80*
    environment:
    DB_HOST: db
    MYSQL_DATABASE: ${MYSQL_DATABASE}
    MYSQL_USER: ${MYSQL_USER}
    MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    depends_on:
    db:
    condition: service_healthy
    restart: unless-stopped

    db:
    image: mysql:8.0
    container_name: lamp-db
    environment:
    MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    MYSQL_DATABASE: ${MYSQL_DATABASE}
    MYSQL_USER: ${MYSQL_USER}
    MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
    - mysql_data:/var/lib/mysql
    healthcheck:
    test: [***CMD**-**SHELL***, *mysqladmin ping -h localhost -uroot -p\*$${MYSQL_ROOT_PASSWORD}\* || exit 1*]
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 30s
    restart: unless-stopped

volumes: mysql_data:

```

Important configuration details:

| Configuration | Purpose                                                 |
| ------------- | ------------------------------------------------------- |
| `build`       | Builds your custom PHP-Apache image                     |
| `ports`       | Maps host port 8085 to Apache port 80                   |
| `DB_HOST: db` | Uses the Compose service name for database connectivity |
| `depends_on`  | Waits for MySQL health before starting the web service  |
| `mysql_data`  | Persists database records                               |
| `image`       | Assigns your Docker Hub image name                      |

## 8. Build and run the LAMP stack

First validate the Compose configuration:

``` sudo docker compose config ```

Build your application image and start the containers:

``` sudo docker compose up -d --build ```

Check running containers:

``` sudo docker ps ```

Expected containers:

``` **CONTAINER** ID   **IMAGE**                       **STATUS** ...            student-records-lamp:1.0    Up ... ...            mysql:8.0                   Up (healthy) ```

If a container does not start, inspect its logs:

``` sudo docker compose logs ```

Or inspect each service separately:

``` sudo docker logs lamp-web sudo docker logs lamp-db ```

## 9. Demonstrate the web application

Open your browser:

### Student Record Management System

# [http://localhost:8085](http://localhost:8085?utm_source=chatgpt.com)

Hosted by Apache inside your Docker container

Enter sample data:

| Student Name | Email              | Course                 |
| ------------ | ------------------ | ---------------------- |
| Rahul Sharma | rahul\@example.com | Computer Engineering   |
| Priya Patil  | priya\@example.com | Information Technology |
| Amit Desai   | amit\@example.com  | Electronics            |

Click Add Student.

The records should appear in the table.

Database integration demonstrated

## 10. Verify that data is actually stored in MySQL

This is an important part of your practical demonstration.

Enter the MySQL container:

``` sudo docker exec -it lamp-db mysql -u root -p ```

Enter the root password configured in `.env`.

Execute:

``` **SHOW** **DATABASES**;

**USE** studentdb;

**SHOW** **TABLES**;

**SELECT** * **FROM** students; ```

You should see the student records you entered through the browser.

Exit:

``` **EXIT**; ```

This demonstrates that the **PHP** application is communicating with the separate MySQL container.

## 11. Demonstrate database persistence

Stop and remove the containers:

``` sudo docker compose down ```

Start them again:

``` sudo docker compose up -d ```

Open:

`[http://localhost:**8085**`](http://localhost:**8085**`)

Your previous student records should still be visible.

This works because the MySQL database uses the named Docker volume `mysql_data`.

Do not run `docker compose down -v` during this demonstration: that command removes the database volume and its stored records.

## 12. Push your custom image to Docker Hub

Now publish your custom application image.

### Step 1: Create a Docker Hub repository

Open [Docker Hub](https://hub.docker.com/?utm_source=chatgpt.com).

## Sign in.

## Select Create repository. ## Repository name: `student-records-lamp`. ## Select Public (if your practical requires public access). ## Create the repository.

### Step 2: Log in from the terminal

``` sudo docker login -u YOUR_DOCKERHUB_USERNAME ```

Use your Docker Hub credentials or access token when prompted.

### Step 3: Verify your image name

``` sudo docker images ```

Your image should have the repository name:

``` YOUR_DOCKERHUB_USERNAME/student-records-lamp   1.0 ```

If necessary, tag it:

```
sudo docker tag \
    lamp-docker-practical-web \
    YOUR_DOCKERHUB_USERNAME/student-records-lamp:1.0
```

If the Compose-built image already has the correct name, you do not need to tag it again.

### Step 4: Push the image

``` sudo docker push YOUR_DOCKERHUB_USERNAME/student-records-lamp:1.0 ```

Image published when push completes

The custom **PHP**-Apache application image is now available in your Docker Hub repository. The MySQL image is not part of this custom image; it is pulled separately when the stack is deployed.

## 13. Verify the published image independently

To demonstrate that your image can be retrieved from Docker Hub:

``` sudo docker pull YOUR_DOCKERHUB_USERNAME/student-records-lamp:1.0 ```

You can also inspect the image:

``` sudo docker image inspect \ YOUR_DOCKERHUB_USERNAME/student-records-lamp:1.0 ```

Your Docker Hub repository should show the `1.0` tag.

Important: To deploy the published image on another machine, use the same `compose.yaml` but replace the `build` section under `web` with:

```
    image: YOUR_DOCKERHUB_USERNAME/student-records-lamp:1.0
```

Then run:

``` sudo docker compose up -d ```

The other machine will pull your custom web image and the MySQL image and start the application.

## 14. Useful Docker commands for your viva

| Command                                         | Purpose                    |
| ----------------------------------------------- | -------------------------- |
| `docker pull php:8.2-apache`                    | Pull PHP-Apache image      |
| `docker pull mysql:8.0`                         | Pull MySQL image           |
| `docker images`                                 | List local images          |
| `docker ps`                                     | List running containers    |
| `docker compose up -d --build`                  | Build and start stack      |
| `docker compose down`                           | Stop and remove containers |
| `docker logs lamp-web`                          | View Apache/PHP logs       |
| `docker exec -it lamp-db mysql -u root -p`      | Access MySQL               |
| `docker volume ls`                              | List Docker volumes        |
| `docker push username/student-records-lamp:1.0` | Publish custom image       |

## 15. Viva questions

Q1. What is the **LAMP** stack?

**LAMP** stands for Linux, Apache, MySQL and **PHP**. It is a software stack used for hosting dynamic web applications.

Q2. Why are we using two containers?

Apache/**PHP** and MySQL have separate responsibilities. Running them independently improves modularity, maintenance and scalability.

Q3. How does the **PHP** container communicate with MySQL?

Both containers are connected to the same Docker Compose network. **PHP** uses the service name `db` as the hostname and port `**3306**` as the MySQL port.

Q4. What is a Docker volume?

A Docker volume provides persistent storage independent of a container's lifecycle.

Q5. What is the purpose of a Dockerfile?

It defines the instructions required to build a custom Docker image.

Q6. What is the difference between `docker pull` and `docker push`?

- `docker pull` downloads an image from a registry.
- `docker push` uploads an image to a registry.

Q7. What is Docker Compose?

Docker Compose is a tool used to define and manage multi-container applications using a **YAML** configuration file.

Q8. What happens if the MySQL container restarts?

The database files remain available because they are stored in a persistent Docker volume. The application can reconnect once MySQL is healthy.

## 16. Screenshots to capture for your practical record

- **PHP**-Apache and MySQL images pulled from Docker Hub.
- Project directory and source files.
- Dockerfile and Compose configuration.
- Successful `docker compose up -d --build`.
- Both containers running using `docker ps`.
- Student application opened in the browser.
- Multiple student records displayed.
- MySQL `**SELECT** * **FROM** students;` output.
- Data still present after container restart.
- Successful Docker Hub image push.
- Docker Hub repository showing the custom image and tag.

## 17. References

- [Docker – **PHP** application containerization guide](https://docs.docker.com/guides/php/?utm_source=chatgpt.com)
- [Docker – Using containerized databases](https://docs.docker.com/guides/databases/?utm_source=chatgpt.com)
- [Official **PHP** Docker image](https://hub.docker.com/_/php?tab=ags\&utm_source=chatgpt.com)
- [Docker image push documentation](https://docs.docker.com/reference/cli/docker/image/push/?utm_source=chatgpt.com)

Expected final result: A working **PHP** student management application, Apache and MySQL running in separate Docker containers, persistent database storage, and your custom application image published to Docker Hub.

Start with sections 1–3 and create the project directory. If you encounter any error, share the terminal output before proceeding; we can troubleshoot it against your Ubuntu and Docker setup.
