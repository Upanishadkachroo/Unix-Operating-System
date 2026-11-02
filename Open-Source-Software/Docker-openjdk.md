# Experiment: Create a Dockerfile with Ubuntu and OpenJDK and run a Java application

## 1. Aim

To write a Dockerfile that pulls an Ubuntu base image, installs OpenJDK, copies a Java application into the Docker image, builds the image, and executes the Java application inside a Docker container.

## 2. Create the project directory

Open your Ubuntu terminal:

``` mkdir -p ~/java-docker-demo cd ~/java-docker-demo ```

## 3. Write a Java application

We will create a simple Java program that displays a welcome message and performs basic arithmetic operations.

Create the file:

``` nano HelloDocker.java ```

Add the following code:

```
public class HelloDocker {
    public static void main(String[] args) {

    System.out.println(*================================*);
    System.out.println(* Java Application Using Docker *);
    System.out.println(*================================*);

        System.out.println(*Hello from Ubuntu Docker Container!*);

    int a = 20;
    int b = 10;

    System.out.println(*First Number: * + a);
    System.out.println(*Second Number: * + b);

    System.out.println(*Addition: * + (a + b));
    System.out.println(*Subtraction: * + (a - b));
    System.out.println(*Multiplication: * + (a * b));
    System.out.println(*Division: * + (a / b));

    System.out.println(*Java application executed successfully.*);
    }
}
```

Save the file using `Ctrl+O`, Enter, and `Ctrl+X`.

## 4. Write the Dockerfile

Create a file named exactly `Dockerfile`:

``` nano Dockerfile ```

Add:

``` **FROM** ubuntu:24.04

**ENV** DEBIAN_FRONTEND=noninteractive

**RUN** apt-get update && \
    apt-get install -y openjdk-21-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

**WORKDIR** /app

**COPY** HelloDocker.java .

**RUN** javac HelloDocker.java

**CMD** [*java*, *HelloDocker*] ```

### Explanation of Dockerfile instructions

| Instruction                          | Purpose                                                       |
| ------------------------------------ | ------------------------------------------------------------- |
| `FROM ubuntu:24.04`                  | Pulls Ubuntu 24.04 as the base image.                         |
| `ENV DEBIAN_FRONTEND=noninteractive` | Prevents interactive prompts during package installation.     |
| `RUN apt-get update`                 | Updates Ubuntu's package index.                               |
| `apt-get install -y openjdk-21-jdk`  | Installs OpenJDK 21, including the Java compiler.             |
| `apt-get clean`                      | Removes cached package files.                                 |
| `WORKDIR /app`                       | Creates and sets `/app` as the working directory.             |
| `COPY HelloDocker.java .`            | Copies the Java source file into the image.                   |
| `RUN javac HelloDocker.java`         | Compiles the Java program into a `.class` file.               |
| `CMD [*java*, *HelloDocker*]`        | Runs the compiled Java application when the container starts. |

## 5. Build the Docker image

Run this command inside `~/java-docker-demo`:

``` sudo docker build -t ubuntu-java-demo:v1 . ```

Docker will:

## Download the Ubuntu 24.04 image if it is not already available.

## Install OpenJDK 21. ## Copy the Java source file. ## Compile the Java program. ## Create the custom Docker image.

Verify the image:

``` sudo docker images ```

Expected entry:

``` **REPOSITORY**          **TAG** ubuntu-java-demo    v1 ```

## 6. Run the Docker container

Execute:

``` sudo docker run --name java-container ubuntu-java-demo:v1 ```

Expected output:

# ```

#  Java Application Using Docker Hello from Ubuntu Docker Container! First Number: 20 Second Number: 10 Addition: 30 Subtraction: 10 Multiplication: **200** Division: 2 Java application executed successfully. ```

The container runs the Java application and exits after the program finishes. This is normal for a short-lived application.

## 7. Verify the container

List all containers:

``` sudo docker ps -a ```

You should see `java-container` with an exited status.

View its output again:

``` sudo docker logs java-container ```

Verify the installed Java version inside the image:

``` sudo docker run --rm ubuntu-java-demo:v1 java -version ```

Verify the compiler:

``` sudo docker run --rm ubuntu-java-demo:v1 javac -version ```

## 8. Run the same container again

To execute the application again, remove the previous container:

``` sudo docker rm java-container ```

Run it again:

``` sudo docker run --name java-container ubuntu-java-demo:v1 ```

Alternatively, create a new container each time:

``` sudo docker run --rm ubuntu-java-demo:v1 ```

The `--rm` option automatically removes the container after the application finishes.

## 9. Project directory structure

Your final project should look like this:

``` java-docker-demo/ │ ├── Dockerfile │ └── HelloDocker.java ```

## 10. Important Docker and Java concepts for viva

| Question                            | Answer                                                                                    |
| ----------------------------------- | ----------------------------------------------------------------------------------------- |
| What is OpenJDK?                    | Open-source implementation of the Java Platform, including the Java compiler and runtime. |
| What is a Dockerfile?               | A text file containing instructions to build a Docker image.                              |
| What is a base image?               | The starting image used to create another image.                                          |
| What is `javac`?                    | The Java compiler that converts `.java` source code into `.class` bytecode.               |
| What is JVM?                        | Java Virtual Machine, which executes Java bytecode.                                       |
| What is `WORKDIR`?                  | Sets the working directory inside the container.                                          |
| What is `COPY`?                     | Copies files from the build context into the image.                                       |
| What is `CMD`?                      | Specifies the default command executed when a container starts.                           |
| Difference between `RUN` and `CMD`? | `RUN` executes during image construction; `CMD` specifies the default runtime command.    |
| Why does the container exit?        | The Java program completes, and there is no foreground process left running.              |

## Result

Successfully created a Dockerfile using Ubuntu 24.04 as the base image, installed OpenJDK 21, compiled a Java application, built a custom Docker image, and executed the Java application inside a Docker container.

Note: This experiment uses `ubuntu:24.04` with `openjdk-21-jdk`, rather than a prebuilt Java-only image. This explicitly demonstrates installing OpenJDK inside Ubuntu, as required by the experiment.
