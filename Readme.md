# 💡 Data Communications Programming Assignment - Fall 2022

## 🌟Multi-Thread/Process Matrix Multiplication Implementation

This project implements a server-client architecture for a random calculation matching game. Clients solve arithmetic problems issued by the server in a synchronized multi-threaded environment.

### Project Overview

This assignment involves implementing a server-client system that performs matrix multiplication using multi-threading and socket communication. The system consists of one server and four clients.

### 📘Program Components

#### Server.py

**Functions:**
- `update_system_clock()`: Updates the `system_clock` incrementally.
- `handle_client(round_number, select_client_list_idx)`: Handles client interactions by issuing arithmetic problems, receiving solutions, and updating result matrices for each round.
- `accept_4clients_connection()`: Accepts connections from 4 clients per server thread.
- `main()`: Initiates server threads and manages client connections stored in `client_sockets`.

**Global Variables:**
- `system_clock`: Tracks the system time with increments for each operation.
- `Round_MAX`: The total number of rounds to be played.
- `MAX_CLIENTS`: The number of clients that will be connected.
- `new_procession`: A 10x10 matrix initialized to zero to store results.
- `client_accept_cnt`: The count of connected clients.
- `client_sockets`: A list managing the client socket connections.
- `client_list`: A list storing possible combinations of client IDs for row/column extraction each round.
- `client_semaphore`: A semaphore to prevent race conditions in critical sections.

**Variables:**
- `matrices`: A 6x10x10 matrix to store round results.
- `clients`: Possible pairs of client IDs for selection.
- `non_selected_clients`: A list of clients that were not selected for the current operation.
- `request_row or col_idx_data`: String data requesting a specific row or column from selected client pairs.
- `data_row or col{n}`: Stores the received row or column data from selected clients.
- `send_row_col_data{n}`: String data to send specific rows or columns to non-selected clients.
- `result_matrix{n}`: Stores the received result matrix from non-selected clients.

#### Client.py

**Functions:**
- `generate_random_matrix()`: Returns a 10x10 matrix with random integers between 0 and 100.
- `perform_vector_multiplication(row_vector, col_vector)`: Performs matrix multiplication for the provided vectors if they are not None.
- `client(c_idx)`: Manages communication with the server based on the client ID.

**Variables:**
- `clients_threads`: A list of client threads with IDs from 1 to 4.
- `client_thread`: A thread targeting the `client()` function.
- `match`: Stores which row or column index to extract based on data from the server.
- `row or col_indices`: Stores the indices of the data matched.
- `row or col_data_str`: Stores the extracted row or column data from the client.
- `number_list`: Stores the extracted data from the server.
- `result_msg_non_selected_client`: Stores the multiplication result as a string.

### 📘Compilation Method

The source code is written in Python, therefore no compilation is necessary. Python version 3.9 or above and a suitable IDE such as Pycharm community edition 2023.2.3 are required to run the code.

### 📘Program Execution Environment and Method

**Environment:**
- Python version 3.9 & Pycharm community edition version 2023.2.3.

**Execution Method:**
- Set the code to run as the "Current File" and execute "Server.py" and "Client.py" using the "Run" command or "Shift + F10".

### 📘Synchronization and Serialization

**Server-Client Synchronization and Serialization:**
- Use `threading.Semaphore(1)` as `client_semaphore` to control access to critical sections.
- Server-Client data are always converted to string format for transmission, with encoding set to the default for socket communication.

**Client Synchronization and Serialization:**
- Data exchange between clients is done through the server to avoid complications with global variables or direct client-client communication.

### 📘Error or Additional Message Handling

Most unexpected errors are logged and printed in the format "Error: {e}". Specific errors such as `ConnectionResetError` are logged and printed when the server forcibly closes a connection. For a `KeyboardInterrupt`, the process is passed without additional handling.

### 📘Additional Comments

Operations such as message transmission, matrix calculation, and matrix update are considered a single operation and increment the `system_clock` by 1 second. With 6 server threads running simultaneously, the round clock increases by 1 second per round.

For detailed implementation and functionality, refer to the respective Python scripts and documentation provided within the source code.

### 🚀Due Date

- Submission Deadline: November 14, 2023, 23:59
- No late submissions will be accepted.

### 🚀Submission Format

- Submit a single file named `G<group_number>HW2.zip` (e.g., GxHW2.zip) containing all source files and result files.

### 🚀Simulation Environment and Components

- **Server**: Manages client connections, issues matrix multiplication tasks, and aggregates results.
- **Clients**: Connect to the server, receive matrix multiplication tasks, and send back results.
- **Languages & Tools**: Python 3.9, Pycharm Community Edition 2023.2.3, and socket programming.
- **Multithreading**: Used in the server to handle multiple client connections simultaneously.

### 🚀Simulation Scenario

- The server initiates and maintains a system clock, incrementing every second.
- 100 rounds of matrix multiplication tasks are performed, with clients randomly paired in each round.
- Non-selected clients in each round perform the matrix multiplication task and send results back to the server.
- The server aggregates these results and updates its matrices accordingly.
- All interactions and results are logged in respective client and server log files.

### 🚀Submission Details

- Submit a zip file `G<group_number>HW2.zip` containing all source files and log files.
- Include a `Readme.txt` detailing the project overview, group members' information, and execution instructions.
- Ensure all source code and logs are properly organized and labeled for ease of evaluation.

### 🚀Video Explanation

- Create a 5-minute video explaining the project, its structure, and how it operates.
- The video should demonstrate the execution of the program and discuss key parts of the source code.
- Submit a `download.txt` file containing a link to the video.
- Make sure the video is accessible to the evaluators; any access issues may result in penalties.
