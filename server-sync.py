import socket 
import os 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

print("[SERVER] waiting for connection...")

DIR = "server_files"
os.makedirs(DIR, exist_ok=True)

while True: 

    client, addr = server.accept()
    print(f"[CONNECTED] {addr}")

    while True: 

        try: 
            command = client.recv(1024).decode()

            if not command: 
                break

            print(f"[CLIENT] {command}")

            if command.startswith("/list"): 
                files = os.listdir(DIR)
                if not files: 
                    print("[SERVER] FILE NOT FOUND")
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
                    client.send("upload {filename} success".encode())

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
                print("[SERVER] unknown command....")

        except Exception as e: 
            print("[ERROR]", e)
            break 

    client.close()
    print(f"[DISCONNECTED] {addr}")
      
server.close()

