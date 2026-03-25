import os 
import socket 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

while True: 
    command = input(">> ")

    if command.startswith("/upload"):
        _, filename = command.split()

        if not os.path.exists(filename):
            print("file not found")
            continue

        client.send(command.encode())

        file_size = os.path.getsize(filename)
        client.send(str(file_size).encode())

        with open(filename, "rb") as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client.send(data)

        response = client.recv(1024).decode()
        print(response)

    elif command.startswith("/download"):
        client.send(command.encode())

        response = client.recv(1024).decode()

        if response == "FILE NOT FOUND":
            print(response)
            continue

        file_size = int(response)

        _, filename = command.split()
        with open(filename, "wb") as f:
            received = 0
            while received < file_size:
                data = client.recv(1024)
                f.write(data)
                received += len(data)

        print("Download selesai")

    elif command.startswith("/list"):
        client.send(command.encode())
        response = client.recv(4096).decode()
        print("Files di server:")
        print(response)

    elif command == "exit":
        break

    else:
        client.send(command.encode())
        response = client.recv(4096).decode()
        print(response)

client.close 