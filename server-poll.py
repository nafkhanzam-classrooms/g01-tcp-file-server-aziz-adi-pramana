import socket
import os
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

print("[SERVER] waiting for connections...")

DIR = "server_files"
os.makedirs(DIR, exist_ok=True)

# inisialisasi poll
poller = select.poll()

# mapping fd ke socket
fd_to_socket = {server.fileno(): server}
clients = {}

# register server socket
poller.register(server, select.POLLIN)

while True:
    events = poller.poll()

    for fd, flag in events:
        sock = fd_to_socket[fd]

        if sock == server:
            client_socket, client_address = server.accept()
            print(f"[CONNECTED] {client_address}")

            fd_to_socket[client_socket.fileno()] = client_socket
            clients[client_socket] = client_address

            poller.register(client_socket, select.POLLIN)

        elif flag & select.POLLIN:
            try:
                command = sock.recv(1024).decode().strip()

                if not command:
                    raise Exception("Disconnected")

                print(f"[CLIENT {clients[sock]}] {command}")

                if command.startswith("/list"):
                    files = os.listdir(DIR)
                    if not files:
                        sock.send("No files".encode())
                    else:
                        sock.send("\n".join(files).encode())

                elif command.startswith("/upload"):
                    _, filename = command.split()
                    file_path = os.path.join(DIR, filename)

                    file_size = int(sock.recv(1024).decode())

                    with open(file_path, "wb") as f:
                        received = 0
                        while received < file_size:
                            data = sock.recv(1024)
                            if not data:
                                break
                            f.write(data)
                            received += len(data)

                    print(f"[SERVER] upload done {filename}")
                    sock.send(f"upload {filename} success".encode())

                elif command.startswith("/download"):
                    _, filename = command.split()
                    file_path = os.path.join(DIR, filename)

                    if not os.path.exists(file_path):
                        sock.send("FILE NOT FOUND".encode())
                        print("[SERVER] FILE NOT FOUND")
                        continue

                    file_size = os.path.getsize(file_path)
                    sock.send(str(file_size).encode())

                    with open(file_path, "rb") as f:
                        while True:
                            data = f.read(1024)
                            if not data:
                                break
                            sock.send(data)

                    print(f"[SERVER] download send {filename}")

                else:
                    sock.send("UNKNOWN COMMAND".encode())

            except Exception as e:
                print(f"[DISCONNECTED] {clients[sock]}")

                poller.unregister(sock)
                del fd_to_socket[sock.fileno()]
                del clients[sock]

                sock.close()

        else:
            poller.unregister(sock)
            if sock in clients:
                print(f"[DISCONNECTED] {clients[sock]}")
                del clients[sock]
            del fd_to_socket[fd]
            sock.close()