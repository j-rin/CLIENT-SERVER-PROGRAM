import socket
import threading
import os

HEADER = 64
PORT = 5050
ADDR = ('127.0.0.1', PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            cmd = msg.split(' ')

            if cmd[0].lower() == "create":
                if not os.path.exists(f'./{cmd[1]}'):
                    f = open(f"{cmd[1]}", "w")
                    f.write("")
                    f.close()
                    print("test1")
                    conn.send(bytes("File created!",'utf-8'))
                    print("test2")
                else:
                    conn.send(bytes("File with same name already exists.",'utf-8'))

            elif cmd[0].lower() == "delete":
                if os.path.exists(f'./{cmd[1]}'):
                    os.remove(f'{cmd[1]}')
                    conn.send(bytes("File deleted",'utf-8'))
                else:
                    conn.send(bytes("File does not exist",'utf-8'))

            elif cmd[0].lower() == "cat":
                if os.path.exists(f'./{cmd[1]}'):
                    f = open(f'./{cmd[1]}', 'r')
                    content = f.read()
                    f.close()

                    conn.send(content.encode('utf-8'))
                else:
                    conn.send(bytes("File does not exist",'utf-8'))

            elif cmd[0].lower() == "edit":
                to_write = conn.recv(HEADER).decode(FORMAT)
                cmd = to_write.split(' ')

                if os.path.exists(f'./{cmd[1]}'):
                    conn.send(bytes("OK", "utf-8"))

                    to_write = conn.recv(HEADER).decode(FORMAT)

                    f = open(f'./{cmd[1]}', 'a')
                    f.write(to_write)
                    f.close()

                    conn.send(bytes("File edited.", 'utf-8'))
                else:
                    conn.send(bytes("File does not exist", "utf-8"))



def start():
    server.listen()
    print(f"[LISTENING] Server is listening on localhost")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
