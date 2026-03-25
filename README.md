[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/mRmkZGKe)
# Network Programming - Assignment G01

## Anggota Kelompok
| Nama               | NRP        | Kelas |
|-------------------|------------|-------|
| Aziz Adi Pramana   | 5025241195 | D     |

## Link Youtube (Unlisted)
Link ditaruh di bawah ini
```
https://youtu.be/Ie6z3yvMEPA
```

#### Deskripsi File

- `client.py` : merupakan file client
- `server-sync.py` : merupakan file server menggunakan skema sinkronus
- `server-select.py` : merupakan file server menggunakan skema select
- `server-poll.py` : merupakan file server menggunakan skema poll
- `server-thread.py` : merupakan file server menggunakan skema thread
- `icon.jpg:` aset file
- `waifu.jfif:` aset file
- `document.txt:` aset file


## Penjelasan Program

### File: `client.py`
```python
import os 
import socket 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))
```

- Blok kode di atas digunakan untuk inisiasi socket client dengan meng-import library dan membuat client socket

```python
while True: 
    command = input(">> ")
```

- Blok kode di atas berperan sebagai loop utama untuk menerima input dari user client yang akan dikirim atau disampaikan ke server

```python
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
```

- Blok kode di atas berperan untuk menghadirkan feature `upload` agar user client dapat mengupload file ke server, yang kemudian akan disimpan di dalam folder server

```python
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
```

- Blok kode di atas berperan untuk menghadirkan feature `download` agar user client dapat mendownload file file yang ada di dalam folder server

```python
elif command.startswith("/list"):
    client.send(command.encode())
    response = client.recv(4096).decode()
    print("Files di server:")
    print(response)
```

- Blok kode di atas berperan untuk menghadirkan feature `list` agar user client dapat melihat apa saja isi file di dalam folder server

```python
elif command == "exit":
    break
```

- Kode di atas berperan untuk user client memutuskan hubungan atau connection dengan server

```python
else:
    client.send(command.encode())
    response = client.recv(4096).decode()
    print(response)
```

- Kode di atas digunakan apabila user mengetikkan command selain 3 command di atas (`/list`, `/download`, `/upload`), di sisi server nanti client akan diberikan sebuah test berupa `UNKNOWN COMMAND`

```python
client.close
```

- Kode di atas untuk koneksi TCP server

### `server-sync.py`

```python
import socket 
import os 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

print("[SERVER] waiting for connection...")
```

- Blok kode di atas digunakan untuk inisiasi socket client dengan meng-import library dan membuat server socket.

```python
DIR = "server_files"
os.makedirs(DIR, exist_ok=True)
```

- Blok kode di atas digunakan untuk membuat folder dengan nama `server_files`

```python
while True: 

    client, addr = server.accept()
    print(f"[CONNECTED] {addr}")
```

- Blok kode di atas berperan sebagai loop utama untuk menerima koneksi dengan client

```python
while True: 

    try: 
        command = client.recv(1024).decode()

        if not command: 
            break

        print(f"[CLIENT] {command}")
```

- Blok kode di atas digunakan untuk menerima perintah client

```python
if command.startswith("/list"): 
    files = os.listdir(DIR)
    if not files: 
        print("[SERVER] FILE NOT FOUND")
    else:
        client.send("\n".join(files).encode()) 
```

- Blok kode di atas berperan untuk memberikan informasi file apa saja yang ada di dalam folder server ke client

```python
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
```

- Blok kode di atas berperan untuk menerima file dan menyimpan file yang dikirim oleh client ke dalam folder server

```python
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
```

- Blok kode di atas untuk mengirim file ke client, sehingga proses download dapat dilakukan

```python
else: 
    client.send("UNKNOWN COMMAND".encode())
    print("[SERVER] unknown command....")
```

- Blok kode di atas untuk mengirim pesan kepada client bahwa command yang diberikan client tidak terdaftar atau tidak dikenali oleh client

```python
except Exception as e: 
    print("[ERROR]", e)
    break 
```

- Blok kode untuk mengatasi error teknis

```python
client.close()
print(f"[DISCONNECTED] {addr}")
```

- Blok kode yang menampilkan tulisan client disconnect dan memutus hubungan dengan client

```python
server.close()
```

- Kode di atas untuk menutup  socket server

### `server-select.py`

```python
import socket
import os
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

print("[SERVER] waiting for connections...")
```

- Blok kode di atas digunakan untuk inisiasi socket client dengan meng-import library dan membuat server socket.

```python
DIR = "server_files"
os.makedirs(DIR, exist_ok=True)
```

- Blok kode di atas digunakan untuk membuat folder dengan nama `server_files`

```python
sockets_list = [server]
clients = {}
```

- `socket_list` digunakan untuk menyimpan semua socket yang akan di pantau oleh server
- `client` digunakan untuk menyimpan alamat dari semua client yang terhubung

 

```python
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
```

- Blok kode di atas merupakan loop utama server dengan menggunakan metode `select`

  

```python
for notified_socket in read_sockets:
```

- Digunakan untuk load semua socket yang siap menerima data

```python
if notified_socket == server:
    client_socket, client_address = server.accept()
    sockets_list.append(client_socket)
    clients[client_socket] = client_address
    print(f"[CONNECTED] {client_address}")
```

- mekanisme program di atas yaitu jika socket yang siap adalah server, maka itu artinya ada client baru yang ingin connect
- `accept()`  membuat socket baru untuk client tersebut
- menambahkan socket client ke `socket_list` agar dipantau oleh `select`
- menyimpan alamat client di dictionary `clients`

```python
else:
    try:
        command = notified_socket.recv(1024).decode().strip()
        if not command:
            raise Exception("Disconnected")
        print(f"[CLIENT {clients[notified_socket]}] {command}")
```

- Jika socket adalah client, menerima perintah dari client.
- `.strip()` menghapus spasi kosong di awal/akhir.
- Jika tidak ada data (client disconnect), lempar exception agar ditangani di blok error.

```python
if command.startswith("/list"):
    files = os.listdir(DIR)
    if not files:
        notified_socket.send("No files".encode())
    else:
        notified_socket.send("\n".join(files).encode())
```

- Blok kode di atas berperan untuk menghadirkan feature `list` agar user client dapat melihat apa saja isi file di dalam folder server

```python
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
```

- Blok kode di atas berperan untuk menerima file dan menyimpan file yang dikirim oleh client ke dalam folder server

```python
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
```

- Blok kode di atas untuk mengirim file ke client, sehingga proses download dapat dilakukan

 

```python
else:
    notified_socket.send("UNKNOWN COMMAND".encode())
```

- Blok kode di atas untuk mengirim pesan kepada client bahwa command yang diberikan client tidak terdaftar atau tidak dikenali oleh client

```python
except Exception as e:
    print(f"[DISCONNECTED] {clients[notified_socket]}")
    sockets_list.remove(notified_socket)
    del clients[notified_socket]
    notified_socket.close()
```

- Program di atas digunakan untuk
    - Menangkap error atau disconnect client.
    - Menghapus socket client dari list yang dipantau dan dictionary clients.
    - Menutup socket client.
    

```python
for notified_socket in exception_sockets:
    sockets_list.remove(notified_socket)
    del clients[notified_socket]
    notified_socket.close()
```

- Program di atas digunakan untuk:
    - `select` juga mengembalikan socket yang bermasalah (`exception_sockets`).
    - Socket ini langsung dihapus dan ditutup.
    - Menjaga agar server tetap stabil dan tidak crash karena socket bermasalah.

### `server-poll.py`

```python
import socket
import os
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

print("[SERVER] waiting for connections...")
```

- Blok kode di atas digunakan untuk inisiasi socket client dengan meng-import library dan membuat server socket.

```python
DIR = "server_files"
os.makedirs(DIR, exist_ok=True)
```

- Blok kode di atas digunakan untuk membuat folder dengan nama `server_files`

```python
poller = select.poll()
fd_to_socket = {server.fileno(): server}
clients = {}
poller.register(server, select.POLLIN)
```

- Membuat objek `poller` untuk memantau banyak socket secara efisien.
- `fd_to_socket` adalah mapping dari **file descriptor (fd)** ke objek socket.
- `clients` menyimpan mapping socket ke alamat client.
- Server socket diregistrasi ke `poller` untuk event `POLLIN` (siap dibaca).

```python
while True:
    events = poller.poll()
```

- Merupakan loop utama server

```python
for fd, flag in events:
    sock = fd_to_socket[fd]
```

- Memproses setiap socket yang memiliki event.
- Mengambil objek socket dari file descriptor (`fd_to_socket`).

```python
if sock == server:
    client_socket, client_address = server.accept()
    print(f"[CONNECTED] {client_address}")

    fd_to_socket[client_socket.fileno()] = client_socket
    clients[client_socket] = client_address

    poller.register(client_socket, select.POLLIN)
```

- Jika socket adalah server, berarti ada client baru yang ingin connect.
- `accept()` membuat socket baru untuk client tersebut.
- Menambahkan socket client ke mapping fd dan dictionary clients.
- Meregestrasi socket client ke poller untuk event `POLLIN`.

```python
elif flag & select.POLLIN:
    try:
        command = sock.recv(1024).decode().strip()
        if not command:
            raise Exception("Disconnected")
        print(f"[CLIENT {clients[sock]}] {command}")
```

- Mengecek apakah event adalah `POLLIN`, artinya client mengirim data.
- Menerima perintah dari client dan menghapus spasi kosong.
- Jika tidak ada data, lempar exception untuk menandai client disconnect.

```python
if command.startswith("/list"):
    files = os.listdir(DIR)
    if not files:
        sock.send("No files".encode())
    else:
        sock.send("\n".join(files).encode())
```

- Blok kode di atas berperan untuk menghadirkan feature `list` agar user client dapat melihat apa saja isi file di dalam folder server

```python
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
```

- Blok kode di atas berperan untuk menerima file dan menyimpan file yang dikirim oleh client ke dalam folder server

```python
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
```

- Blok kode di atas untuk mengirim file ke client, sehingga proses download dapat dilakukan

```python
else:
    sock.send("UNKNOWN COMMAND".encode())
```

- Blok kode di atas untuk mengirim pesan kepada client bahwa command yang diberikan client tidak terdaftar atau tidak dikenali oleh client

```python
except Exception as e:
    print(f"[DISCONNECTED] {clients[sock]}")

    poller.unregister(sock)
    del fd_to_socket[sock.fileno()]
    del clients[sock]

    sock.close()
```

- Menangkap error atau disconnect client.
- Menghapus socket dari poller dan dictionary mapping.
- Menutup socket client.
- Menampilkan pesan client terputus.

```python
else:
    poller.unregister(sock)
    if sock in clients:
        print(f"[DISCONNECTED] {clients[sock]}")
        del clients[sock]
    del fd_to_socket[fd]
    sock.close()
```

- Menangani event selain `POLLIN` (misal error atau hang).
- Menghapus socket dari poller, dictionary, dan menutup socket.
- Memastikan server tetap stabil saat socket bermasalah.

### `server-thread.py`

```python
import socket
import os
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

print("[SERVER] waiting for connections...")
```

- Blok kode di atas digunakan untuk inisiasi socket client dengan meng-import library dan membuat server socket.

```python
DIR = "server_files"
os.makedirs(DIR, exist_ok=True)
```

- Blok kode di atas digunakan untuk membuat folder dengan nama `server_files`

```python
def handle_client(client, addr):
    print(f"[CONNECTED] {addr}")

    while True:
        try:
            command = client.recv(1024).decode().strip()
            if not command:
                break

            print(f"[CLIENT {addr}] {command}")
```

- Fungsi ini dijalankan di thread terpisah untuk setiap client.
- Menampilkan pesan saat client terhubung.
- Loop ini terus menerima perintah dari client sampai client disconnect.

```python
if command.startswith("/list"):
    files = os.listdir(DIR)
    if not files:
        client.send("No files".encode())
    else:
        client.send("\n".join(files).encode())
```

- Blok kode di atas berperan untuk menghadirkan feature `list` agar user client dapat melihat apa saja isi file di dalam folder server

```python
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
```

- Blok kode di atas berperan untuk menerima file dan menyimpan file yang dikirim oleh client ke dalam folder server

```python
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
```

- Blok kode di atas untuk mengirim file ke client, sehingga proses download dapat dilakukan

```python
else:
    client.send("UNKNOWN COMMAND".encode())
```

- Blok kode di atas untuk mengirim pesan kepada client bahwa command yang diberikan client tidak terdaftar atau tidak dikenali oleh client

```python
except Exception as e:
    print("[ERROR]", e)
    break
```

- Menangkap semua error atau disconnect dari client.

```python
client.close()
print(f"[DISCONNECTED] {addr}")
```

- Menutup koneksi TCP dengan client saat loop berakhir.
- Menampilkan pesan client terputus.

```python
while True:
    client, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(client, addr))
    thread.start()
```

- Server menerima koneksi client baru.
- Membuat thread baru untuk setiap client menggunakan `handle_client`.
- Thread berjalan paralel sehingga server bisa melayani banyak client sekaligus tanpa blocking.


## Screenshot Hasil

### Hasil server-sync
#### server
![](https://github.com/nafkhanzam-classrooms/g01-tcp-file-server-aziz-adi-pramana/blob/main/images/server-sys.png)

#### client 

![](https://github.com/nafkhanzam-classrooms/g01-tcp-file-server-aziz-adi-pramana/blob/main/images/client-server-sys.png)


### Hasil server select
#### server 
![Screenshot](https://github.com/nafkhanzam-classrooms/g01-tcp-file-server-aziz-adi-pramana/blob/main/images/server-select.png)

#### client 
![](https://github.com/nafkhanzam-classrooms/g01-tcp-file-server-aziz-adi-pramana/blob/main/images/client1-server-select.png)

![](https://github.com/nafkhanzam-classrooms/g01-tcp-file-server-aziz-adi-pramana/blob/main/images/client2-server-select.png)

### Hasil server Poll
#### server 
![](https://github.com/nafkhanzam-classrooms/g01-tcp-file-server-aziz-adi-pramana/blob/main/images/server-poll.png)

#### client 
![](https://github.com/nafkhanzam-classrooms/g01-tcp-file-server-aziz-adi-pramana/blob/main/images/client1-server-poll.png)

![](https://github.com/nafkhanzam-classrooms/g01-tcp-file-server-aziz-adi-pramana/blob/main/images/client2-server-poll.png)


### Hasil server-threads
#### server 
![](https://github.com/nafkhanzam-classrooms/g01-tcp-file-server-aziz-adi-pramana/blob/main/images/server-threads.png)

#### client 
![](https://github.com/nafkhanzam-classrooms/g01-tcp-file-server-aziz-adi-pramana/blob/main/images/client1-server-threads.png)
![](https://github.com/nafkhanzam-classrooms/g01-tcp-file-server-aziz-adi-pramana/blob/main/images/client2-server-select.png)




