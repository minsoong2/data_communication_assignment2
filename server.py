import socket
import threading
import random
import time
import numpy as np

ip = '127.0.0.1'
port = 8888

system_clock = 0
Round_MAX = 1#00
matrices = [np.zeros((10, 10)) for _ in range(6)]

MAX_CLIENTS = 4
client_accept_cnt = 0
client_sockets = []
client_list = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
client_semaphore = threading.Semaphore(1)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))

f = open("Server.txt", "w")


def update_system_clock():
    global system_clock
    while True:
        time.sleep(1)
        system_clock += 1


def handle_client(round_number, select_client_list_idx):

    global server, matrices, client_semaphore
    try:
        client_semaphore.acquire()
        matrices = [np.zeros((10, 10)) for _ in range(6)]
        print(matrices)
        clients = client_list[select_client_list_idx]
        non_selected_clients = [c for c in range(1, 5) if c not in clients]
        rows = [random.randint(0, 9) for _ in range(2)]
        cols = [random.randint(0, 9) for _ in range(2)]
        print(clients, non_selected_clients)

        for idx, c_socket in enumerate(client_sockets):
            if idx == clients[0] - 1:
                request_row_idx_data = f"System Clock {system_clock}s - Round {round_number}: Client {c_socket.getpeername()} - Request idx_data -> Row {rows}"
                print(request_row_idx_data)
                f.write(request_row_idx_data + '\n')
                c_socket.send(request_row_idx_data.encode())
                receive_data = c_socket.recv(1024).decode()
                print(receive_data)
                if "Row" in receive_data:
                    data_list = receive_data.split(":")[1].strip().split(", ")
                    print("row_data_list", data_list)
                    data_row1 = data_list[0]
                    data_row2 = data_list[1]

            elif idx == clients[1] - 1:
                request_col_idx_data = f"System Clock {system_clock}s - Round {round_number}: Client {c_socket.getpeername()} - Request idx_data -> Col {cols}"
                print(request_col_idx_data)
                f.write(request_col_idx_data + '\n')
                c_socket.send(request_col_idx_data.encode())
                receive_data2 = c_socket.recv(1024).decode()
                print(receive_data2)
                if "Col" in receive_data2:
                    data_list = receive_data2.split(":")[1].strip().split(", ")
                    print("col_data_list", data_list)
                    data_col1 = data_list[0]
                    data_col2 = data_list[1]

        for idx, c_socket in enumerate(client_sockets):
            if idx == non_selected_clients[0] - 1:
                send_row_col_data1 = f"System Clock {system_clock}s - Round {round_number}: Client {c_socket.getpeername()} - Send data -> Row1, Col1: [{data_row1}], [{data_col1}]"
                print(send_row_col_data1)
                c_socket.send(send_row_col_data1.encode())
                result_matrix1 = c_socket.recv(1024).decode()
                print(result_matrix1)
            elif idx == non_selected_clients[1] - 1:
                send_row_col_data2 = f"System Clock {system_clock}s - Round {round_number}: Client {c_socket.getpeername()} - Send data -> Row2, Col2: [{data_row2}], [{data_col2}]"
                print(send_row_col_data2)
                c_socket.send(send_row_col_data2.encode())
                result_matrix2 = c_socket.recv(1024).decode()
                print(result_matrix2)

    except Exception as e:
        e_line = f"Error: {e}"
        print(e_line)
        f.write(e_line + '\n')
    finally:
        client_semaphore.release()


def accept_4clients_connection():
    global server, client_accept_cnt

    server.listen(4)
    server.settimeout(10)

    if client_accept_cnt == 0:
        listen = "Server is listening..."
        print(listen)
        f.write(listen + '\n')

    while client_accept_cnt < MAX_CLIENTS:
        client_socket, client_address = server.accept()
        accept = f"Accepted connection from {client_address}"
        print(accept)
        f.write(accept + '\n')
        client_sockets.append(client_socket)
        client_accept_cnt += 1


def main():

    accept_4clients_connection()

    clock_thread = threading.Thread(target=update_system_clock)
    clock_thread.daemon = True
    clock_thread.start()

    try:

        for cnt in range(1, Round_MAX + 1):
            server_threads = []
            for idx in range(6):
                server_thread = threading.Thread(target=handle_client, args=(cnt, idx))
                server_threads.append(server_thread)

            for thread in server_threads:
                thread.start()
                print(thread)

            time.sleep(1) # 동시 연산

            for thread in server_threads:
                thread.join()
                print(thread)

    except socket.timeout:
        pass

    for client_socket in client_sockets:
        try:
            client_socket.close()
        except Exception as e:
            print(f"Error while closing client socket: {e}")

    print_system_clock = f"end_time: {system_clock}"
    print(print_system_clock)
    f.write(print_system_clock)

    server.close()
    print("Server closed...")
    f.write("Server closed...")


if __name__ == "__main__":
    main()
