import socket
import threading
import random
import time
import numpy as np

ip = '127.0.0.1'
port = 8888

system_clock = 0
round = 100
total_sum = 0
f = open("Server.txt", "w")


def update_system_clock():
    global system_clock
    while system_clock < round:
        time.sleep(1)
        system_clock += 1


def handle_client(client_socket):
    global system_clock
    try:
        while system_clock < round:
            system_clock += 1
    except Exception as e:
        e_line = f"Error: {e}"
        print(e_line)
        f.write(e_line + '\n')
    finally:
        client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(4)
    server.settimeout(1)

    listen = "Server is listening..."
    print(listen)
    f.write(listen + '\n')

    threads = []
    clock_thread = threading.Thread(target=update_system_clock)
    clock_thread.daemon = True
    clock_thread.start()

    client_count = 0

    while system_clock < round:
        if system_clock >= round:
            break
        try:
            client_socket, client_address = server.accept()
            accept = f"Accepted connection from {client_address}"
            print(accept)
            f.write(accept + '\n')
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
            threads.append(client_handler)
            client_count += 1
        except socket.timeout:
            pass

    for thread in threads:
        thread.join()

    print_system_clock = f"end_time: {system_clock}"
    print(print_system_clock)
    f.write(print_system_clock + '\n')
    server.close()
    print("Server closed...")
    f.write("Server closed...")
    if client_count == 0:
        print("No clients connected during the 30 seconds.")
        f.write("No clients connected during the 30 seconds.")


if __name__ == "__main__":
    main()