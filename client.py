import socket
import random
import time
import threading
import numpy as np
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


def client(c_id):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Client {client_socket.getsockname()[1]}: Connected to the server")

    try:
        data = client_socket.recv(1024).decode()
        client_id = f"{client_socket.getsockname()[1]}"
        row_col_1, row_col_2 = [], []

        if client_id in data and "Request idx_data -> Row" in data:
            print(client_id, data)
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
            print(client_id, data)
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

        else:

            if client_id in data and "Send data -> Row1, Col1:" in data:
                print(client_id, data)
                print()
                numbers_string1 = re.findall(r'Send data -> Row1, Col1:\s+(.*)$', data)
                if numbers_string1:
                    numbers_string1 = numbers_string1[0]
                    numbers_list = numbers_string1.split(',')
                    row1 = [int(num) for num in numbers_list[0].strip("[]").split()]
                    col1 = [int(num) for num in numbers_list[1].strip("[] ").split()]
                    print(row1, col1)
                    row_col_1.append(row1)
                    row_col_1.append(col1)
                    result_non_selected_client1 = perform_vector_multiplication(row_col_1[0], row_col_1[1])
                    print(result_non_selected_client1, "!@##@$!@#$")

            elif client_id in data and "Send data -> Row2, Col2:" in data:
                print(client_id, data)
                print()
                numbers_string2 = re.findall(r'Send data -> Row2, Col2:\s+(.*)$', data)
                if numbers_string2:
                    numbers_string2 = numbers_string2[0]
                    numbers_list = numbers_string2.split(',')
                    row2 = [int(num) for num in numbers_list[0].strip("[]").split()]
                    col2 = [int(num) for num in numbers_list[1].strip("[] ").split()]
                    print(row2, col2)
                    row_col_2.append(row2)
                    row_col_2.append(col2)
                    result_non_selected_client2 = perform_vector_multiplication(row_col_2[0], row_col_2[1])
                    print(result_non_selected_client2, "!@##@$!@#$")

    except ConnectionResetError:
        e_line = f"Client {client_socket.getsockname()[1]}: Connection to the server was forcibly closed."
        print(e_line)
    except KeyboardInterrupt:
        pass
    finally:
        print(f"Client {client_socket.getsockname()[1]}: Connection closed")
        client_socket.close()


if __name__ == "__main__":
    client_threads = []
    for i in range(1, 5):
        client_thread = threading.Thread(target=client, args=(i,))
        client_threads.append(client_thread)

    print(client_threads)
    for thread in client_threads:
        thread.start()
        print(thread, "start!!!")

    for thread in client_threads:
        thread.join()