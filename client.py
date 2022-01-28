import socket
import os

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)


def main():

    def send(msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        print(client.recv(2048).decode(FORMAT))

    while True:

      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


      client.connect(ADDR) 
      command = input(">>")

      if command.upper() == "HELP":
         print("""create <name>.txt - to create a file
         delete <name>.txt - to delete a file
         edit <name.txt> - to edit the file
         cat <name.txt> - to read the file
         exit - to exit from the program""")
      elif command.upper() == "EXIT":
         os._exit(0)
      elif command.upper() == "EDIT":
         send(command)
         ip = ""
         rep = client.recv(HEADER).decode(FORMAT)

         if rep == "OK":
            while ip != "#":
                  ip += input()

            send(ip)
         else:
            print("Error while accessing file")

      else:
         send(command)

if __name__ == "__main__":
    main()
