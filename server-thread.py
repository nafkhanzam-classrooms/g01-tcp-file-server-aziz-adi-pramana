import socket
import os
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

print("[SERVER] waiting for connections...")

DIR = "server_files"
os.makedirs(DIR, exist_ok=True)


def handle_client(client, addr):
    print(f"[CONNECTED] {addr}")

    while True:
        try:
            command = client.recv(1024).decode().strip()

            if not command:
                break

            print(f"[CLIENT {addr}] {command}")

            if command.startswith("/list"):
                files = os.listdir(DIR)
                if not files:
                    client.send("No files".encode())
                else:
                    client.send("\n".join(files).encode())

            elif command.startswith("/upload"):
                _, filename = command.split()
                file_path = os.path.join(DIR, filename)

                file_size = int(client.recv(1024).decode())

                with open(file_path, "wb") as f:
                    received = 0
                    while received < file_size:
                        data = client.recv(1024)
                        if not data:
                            break
                        f.write(data)
                        received += len(data)

                print(f"[SERVER] upload done {filename}")
                client.send(f"upload {filename} success".encode())

            elif command.startswith("/download"):
                _, filename = command.split()
                file_path = os.path.join(DIR, filename)

                if not os.path.exists(file_path):
                    client.send("FILE NOT FOUND".encode())
                    print("[SERVER] FILE NOT FOUND")
                    continue

                file_size = os.path.getsize(file_path)
                client.send(str(file_size).encode())

                with open(file_path, "rb") as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        client.send(data)

                print(f"[SERVER] download send {filename}")

            else:
                client.send("UNKNOWN COMMAND".encode())

        except Exception as e:
            print("[ERROR]", e)
            break

    client.close()
    print(f"[DISCONNECTED] {addr}")


while True:
    client, addr = server.accept()

    thread = threading.Thread(target=handle_client, args=(client, addr))
    thread.start()