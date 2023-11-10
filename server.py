import socket
import threading
import random
import time
import numpy as np

ip = '127.0.0.1'
port = 8888

system_clock = 0
round_cnt = 1
Round_MAX = 1#00
matrices = [np.zeros((10, 10)) for _ in range(6)]
lock = threading.Lock()
client_count = 0
client_sockets = []
client_semaphore = threading.Semaphore(0)

f = open("Server.txt", "w")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen(4)

listen = "Server is listening..."
print(listen)
f.write(listen + '\n')


def update_system_clock():
    global system_clock
    while round_cnt <= Round_MAX:
        time.sleep(1)
        system_clock += 1


def handle_client(client_socket):
    global system_clock, round_cnt, matrices, client_count
    try:
        client_sockets.append(client_socket)
        client_count += 1
        if client_count == 4:
            client_semaphore.release()
        client_semaphore.acquire()

        while round_cnt <= Round_MAX:
            matrices = [np.zeros((10, 10)) for _ in range(6)]
            clients = random.sample(range(1, 5), 2)
            rows = [random.randint(0, 9) for _ in range(2)]
            cols = [random.randint(0, 9) for _ in range(2)]

            for idx, c_socket in enumerate(client_sockets):
                if idx == clients[0] - 1:
                    request_row_idx_data = f"Round {round_cnt}: Client {c_socket.getpeername()} - Request idx_data -> Row {rows}"
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
                    request_col_idx_data = f"Round {round_cnt}: Client {c_socket.getpeername()} - Request idx_data -> Col {cols}"
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

            non_selected_clients = [c for c in range(1, 5) if c not in clients]
            print(clients, non_selected_clients)
            for idx, c_socket in enumerate(client_sockets):
                if idx == non_selected_clients[0] - 1:
                    send_row_col_data1 = f"Round {round_cnt}: Client {c_socket.getpeername()} - Send data -> Row1, Col1: [{data_row1}], [{data_col1}]"
                    print(send_row_col_data1)
                    c_socket.send(send_row_col_data1.encode())
                    result_matrix1 = c_socket.recv(1024).decode()
                    print(result_matrix1)
                elif idx == non_selected_clients[1] - 1:
                    send_row_col_data2 = f"Round {round_cnt}: Client {c_socket.getpeername()} - Send data -> Row2, Col2: [{data_row2}], [{data_col2}]"
                    print(send_row_col_data2)
                    c_socket.send(send_row_col_data2.encode())
                    result_matrix2 = c_socket.recv(1024).decode()
                    print(result_matrix2)

            system_clock += 1
            round_cnt += 1

        client_semaphore.release()

    except Exception as e:
        e_line = f"Error: {e}"
        print(e_line)
        f.write(e_line + '\n')


def main():
    global server
    clock_thread = threading.Thread(target=update_system_clock)
    clock_thread.daemon = True
    clock_thread.start()

    client_threads = []
    try:
        while True:
            client_socket, client_address = server.accept()
            accept = f"Accepted connection from {client_address}"
            print(accept)
            f.write(accept + '\n')

            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_threads.append(client_handler)
            client_handler.start()

            if len(client_threads) == 4:
                break

    except socket.timeout:
        pass
    print(client_threads)
    for t in client_threads:
        print(t)
        t.join()

    for client in client_sockets:
        client.send("end".encode())

    print_system_clock = f"end_time: {system_clock}"
    print(print_system_clock)
    f.write(print_system_clock + '\n')

    for i, matrix in enumerate(matrices):
        matrix_data = f"Round {round_cnt}: Matrix {i}\n{matrix}"
        print(matrix_data)
        f.write(matrix_data + '\n')

    server.close()
    print("Server closed...")
    f.write("Server closed...")
    if client_count == 0:
        print("No clients connected during the 30 seconds.")
        f.write("No clients connected during the 30 seconds.")

    if round_cnt > Round_MAX:
        print("Operation completed.")
        f.write("Operation completed.")
    for client in client_sockets:
        client.close()


if __name__ == "__main__":
    main()
