import socket
import random
import time
import threading


# server_ip = "ec2-15-164-95-106.ap-northeast-2.comp ute.amazonaws.com"
# server_port = 55555
server_ip = "127.0.0.1"
server_port = 8888


def client(client_id):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Client {client_id}: start!!")

    try:
        with open(f"Client{client_id}.txt", "w") as f:
            print("!!!")

    except ConnectionResetError:
        with open(f"Client{client_id}.txt", "w") as f:
            e_line = f"Client {client_id}: Connection to the server was forcibly closed."
            print(e_line)
            f.write(e_line + '\n')
    except KeyboardInterrupt:
        pass
    finally:
        client_socket.close()


if __name__ == "__main__":
    client_threads = []
    for i in range(1, 5):
        client_thread = threading.Thread(target=client, args=(i,))
        client_threads.append(client_thread)

    for thread in client_threads:
        thread.start()
        print(thread, "start!!!")

    for thread in client_threads:
        thread.join()
