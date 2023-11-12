import socket
import threading
import numpy as np
import time
import re

# server_ip = "ec2-15-164-95-106.ap-northeast-2.comp ute.amazonaws.com"
# server_port = 55555
server_ip = "127.0.0.1"
server_port = 8888


def generate_random_matrix():
    return np.random.randint(0, 101, size=(10, 10))


def perform_vector_multiplication(row_vector, col_vector):
    if row_vector is not None and col_vector is not None:
        result = np.dot(row_vector, col_vector)
        return result
    else:
        return None


def client(c_idx):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Client {client_socket.getsockname()[1]}: Connected to the server")

    try:
        with open(f"Client{c_idx}.txt", "w") as f:
            while True:
                try:
                    data = client_socket.recv(1024).decode()
                    if not data:
                        break
                except socket.timeout:
                    print(f"Client {client_socket.getsockname()[1]}: Timed out while waiting for data. Breaking the loop.")
                    break
                client_id = f"{client_socket.getsockname()[1]}"
                row_col_1, row_col_2 = [], []

                if client_id in data and "Request idx_data -> Row" in data:
                    print(data)
                    match = re.search(r"Row \[(\d+), (\d+)\]", data)
                    row_indices = [int(match.group(1)), int(match.group(2))]
                    print(f"Client {client_socket.getsockname()[1]} Received row_idx_data:", row_indices)
                    client_matrix = generate_random_matrix()
                    print(f"Client {client_socket.getsockname()[1]} matrix: ", client_matrix)
                    row_data = client_matrix[row_indices[0]]
                    row_data_2 = client_matrix[row_indices[1]]
                    row_data_str = f"Client {client_socket.getsockname()[1]} - Row: {' '.join(map(str, row_data))}, {' '.join(map(str, row_data_2))}"
                    print(row_data_str)
                    client_socket.send(row_data_str.encode())

                elif client_id in data and "Request idx_data -> Col" in data:
                    print(data)
                    match = re.search(r"Col \[(\d+), (\d+)\]", data)
                    col_indices = [int(match.group(1)), int(match.group(2))]
                    print(f"Client {client_socket.getsockname()[1]} Received col_idx_data:", col_indices)
                    client_matrix = generate_random_matrix()
                    print(f"Client {client_socket.getsockname()[1]} matrix: ", client_matrix)
                    col_data = client_matrix[:, col_indices[0]]
                    col_data_2 = client_matrix[:, col_indices[1]]
                    col_data_str = f"Client {client_socket.getsockname()[1]} - Col: {' '.join(map(str, col_data))}, {' '.join(map(str, col_data_2))}"
                    print(col_data_str)
                    client_socket.send(col_data_str.encode())

                elif client_id in data and "Send data -> Row1, Col1:" in data:
                    pattern = r"Round ([1-9][0-9]?|100): Client \('(\d+\.\d+\.\d+\.\d+)', (\d+)\)"
                    match = re.search(pattern, data)
                    round_number, client_ip, client_port = match.group(1), match.group(2), match.group(3)
                    round_cid = f"Round {round_number}: Client ({client_ip}, {client_port})"
                    numbers_list1 = re.findall(r'Send data -> Row1, Col1:\s+(.*)$', data)
                    print(f"{round_cid} - Received Row1, Col1 data: ", numbers_list1)
                    numbers_list1 = numbers_list1[0]
                    numbers_list = numbers_list1.split(',')
                    row1 = [int(num) for num in numbers_list[0].strip("[]").split()]
                    col1 = [int(num) for num in numbers_list[1].strip("[] ").split()]
                    print(row1, col1)
                    row_col_1.append(row1)
                    row_col_1.append(col1)
                    result_non_selected_client1 = f"{round_cid} result: {perform_vector_multiplication(row_col_1[0], row_col_1[1])}"
                    print(result_non_selected_client1)
                    client_socket.send(result_non_selected_client1.encode())

                elif client_id in data and "Send data -> Row2, Col2:" in data:
                    pattern = r"Round ([1-9][0-9]?|100): Client \('(\d+\.\d+\.\d+\.\d+)', (\d+)\)"
                    match = re.search(pattern, data)
                    round_number, client_ip, client_port = match.group(1), match.group(2), match.group(3)
                    round_cid = f"Round {round_number}: Client ({client_ip}, {client_port})"
                    numbers_list2 = re.findall(r'Send data -> Row2, Col2:\s+(.*)$', data)
                    print(f"{round_cid} - Received Row2, Col2 data: ", numbers_list2)
                    numbers_list2 = numbers_list2[0]
                    numbers_list = numbers_list2.split(',')
                    row2 = [int(num) for num in numbers_list[0].strip("[]").split()]
                    col2 = [int(num) for num in numbers_list[1].strip("[] ").split()]
                    print(row2, col2)
                    row_col_2.append(row2)
                    row_col_2.append(col2)
                    result_non_selected_client2 = f"{round_cid} result: {perform_vector_multiplication(row_col_2[0], row_col_2[1])}"
                    print(result_non_selected_client2)
                    client_socket.send(result_non_selected_client2.encode())

    except ConnectionResetError:
        msg = f"Client {client_socket.getsockname()[1]}: Connection to the server was forcibly closed."
        print(msg)
        f.write(msg)
    except KeyboardInterrupt:
        pass
    finally:
        msg = f"Client {client_socket.getsockname()[1]}: Connection closed"
        print(msg)
        f.write(msg)
        client_socket.close()


if __name__ == "__main__":
    client_threads = []

    for idx in range(1, 5):
        client_thread = threading.Thread(target=client, args=(idx,))
        client_threads.append(client_thread)

    for thread in client_threads:
        print(thread)
        thread.start()

    for thread in client_threads:
        thread.join()
        print(thread)