import socket
import os
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

print("[SERVER] waiting for connections...")

DIR = "server_files"
os.makedirs(DIR, exist_ok=True)

# list socket yang dipantau
sockets_list = [server]

clients = {}

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:

        if notified_socket == server:
            client_socket, client_address = server.accept()
            sockets_list.append(client_socket)
            clients[client_socket] = client_address
            print(f"[CONNECTED] {client_address}")

        else:
            try:
                command = notified_socket.recv(1024).decode().strip()

                if not command:
                    raise Exception("Disconnected")

                print(f"[CLIENT {clients[notified_socket]}] {command}")

                if command.startswith("/list"):
                    files = os.listdir(DIR)
                    if not files:
                        notified_socket.send("No files".encode())
                    else:
                        notified_socket.send("\n".join(files).encode())

                elif command.startswith("/upload"):
                    _, filename = command.split()
                    file_path = os.path.join(DIR, filename)

                    file_size = int(notified_socket.recv(1024).decode())

                    with open(file_path, "wb") as f:
                        received = 0
                        while received < file_size:
                            data = notified_socket.recv(1024)
                            if not data:
                                break
                            f.write(data)
                            received += len(data)

                    print(f"[SERVER] upload done {filename}")
                    notified_socket.send(f"upload {filename} success".encode())

                elif command.startswith("/download"):
                    _, filename = command.split()
                    file_path = os.path.join(DIR, filename)

                    if not os.path.exists(file_path):
                        notified_socket.send("FILE NOT FOUND".encode())
                        print("[SERVER] FILE NOT FOUND")
                        continue

                    file_size = os.path.getsize(file_path)
                    notified_socket.send(str(file_size).encode())

                    with open(file_path, "rb") as f:
                        while True:
                            data = f.read(1024)
                            if not data:
                                break
                            notified_socket.send(data)

                    print(f"[SERVER] download send {filename}")

                else:
                    notified_socket.send("UNKNOWN COMMAND".encode())

            except Exception as e:
                print(f"[DISCONNECTED] {clients[notified_socket]}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                notified_socket.close()

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
        notified_socket.close()