FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y g++ && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY client.cpp .

RUN g++ client.cpp -o client

CMD ["./client"]
