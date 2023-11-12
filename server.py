import socket
import threading
import random
import time

ip = '127.0.0.1'
port = 8888

system_clock = 0
Round_MAX = 3#00

MAX_CLIENTS = 4
new_procession = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
client_accept_cnt = 0
client_sockets = []
client_list = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
client_semaphore = threading.Semaphore(1)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
f = open("Server.txt", "a")


def update_system_clock():
    global system_clock
    while True:
        time.sleep(1)
        system_clock += 1


def handle_client(round_number, select_client_list_idx):

    global client_semaphore, f
    try:
        client_semaphore.acquire()
        matrices = [[line[:] for line in new_procession] for _ in range(6)]
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
                f.write(receive_data + '\n')
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
                f.write(receive_data2 + '\n')
                if "Col" in receive_data2:
                    data_list = receive_data2.split(":")[1].strip().split(", ")
                    print("col_data_list", data_list)
                    data_col1 = data_list[0]
                    data_col2 = data_list[1]

        for idx, c_socket in enumerate(client_sockets):
            if idx == non_selected_clients[0] - 1:
                send_row_col_data1 = f"System Clock {system_clock}s - Round {round_number}: Client {c_socket.getpeername()} - Send data -> Row1, Col1: [{data_row1}], [{data_col1}]"
                print(send_row_col_data1)
                f.write(send_row_col_data1 + '\n')
                c_socket.send(send_row_col_data1.encode())
                result_matrix1 = c_socket.recv(1024).decode()
                print(result_matrix1)
                f.write(result_matrix1 + '\n')
                result_number = int(result_matrix1.split(':')[-1].strip())
                matrices[select_client_list_idx][rows[0]][cols[0]] = result_number
                print(matrices)
                for matrix in matrices:
                    for row in matrix:
                        row_str = " ".join(map(str, row))
                        f.write(row_str + "\n")
                    f.write("\n")

            elif idx == non_selected_clients[1] - 1:
                send_row_col_data2 = f"System Clock {system_clock}s - Round {round_number}: Client {c_socket.getpeername()} - Send data -> Row2, Col2: [{data_row2}], [{data_col2}]"
                print(send_row_col_data2)
                f.write(send_row_col_data2 + '\n')
                c_socket.send(send_row_col_data2.encode())
                result_matrix2 = c_socket.recv(1024).decode()
                print(result_matrix2)
                f.write(result_matrix2 + '\n')
                result_number = int(result_matrix2.split(':')[-1].strip())
                matrices[select_client_list_idx][rows[1]][cols[1]] = result_number
                print(matrices)
                for matrix in matrices:
                    for row in matrix:
                        row_str = " ".join(map(str, row))
                        f.write(row_str + "\n")
                    f.write("\n")

    except Exception as e:
        emsg = f"Error: {e}"
        print(emsg)
        f.write(emsg + '\n')
    finally:
        client_semaphore.release()


def accept_4clients_connection():

    global server, client_accept_cnt, f
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
    global f

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

            time.sleep(1)
            for thread in server_threads:
                thread.join()
                print(thread)

    except socket.timeout:
        pass

    for client_socket in client_sockets:
        try:
            client_socket.close()
        except Exception as e:
            emsg = f"Error while closing client socket: {e}"
            print(emsg)
            f.write(emsg + '\n')

    print_system_clock = f"end_time: {system_clock}"
    print(print_system_clock)
    f.write(print_system_clock + '\n')

    server.close()
    print("Server closed...")
    f.write("Server closed..." + '\n')
    f.close()


if __name__ == "__main__":
    main()