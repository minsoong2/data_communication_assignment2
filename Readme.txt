[Server.py]

* 프로그램 구성요소 설명
- 함수
 - update_system_clock() : system_clock을 업데이트하는 함수
 - handle_client(round_number, select_client_list_idx) : 현재 round 번호와, 선택된 클라이언트 리스트 인덱스를 매개변수로 하여 각 클라이언트 리스트 마다 행, 열 추출 및 선택되지 않은 클라이언트 리스트에게 행렬곱셈 계산 후 결과 수신, 결과 행렬 업데이트를 담당하는 함수
 - accept_4clients_connection() : 서버 스레드 하나 당 클라이언트 4개와 통신하기 위해, 4개의 연결을 받는 함수
 - main() : 4개의 클라이언트를 받아, client_sockets에 저장하고 6개의 서버 스레드를 실행시키는 함수

- 전역변수
 - system_clock : 각 연산 당 1씩 증가하는 시스템 초를 저장하는 변수
 - Round_MAX : 총 라운드의 개수를 저장하는 변수
 - MAX_CLIENTS : 연결할 클라이언트들의 개수를 저장하는 변수
 - new_procession : 결과를 저장할 6 * 10 * 10 행렬에서 0으로 초기화된 10 * 10 행렬을 저장하는 변수
 - client_accept_cnt : 연결된 클라이언트들의 개수를 저장하는변수
 - client_sockets : 연결된 클라이언트들의 소켓을 관리하기 위한 리스트 변수
 - client_list : 각 라운드 마다 행, 열을 추출할 클라이언트의 아이디 경우의 수를 저장하는 리스트 변수
 - client_semaphore : 여러 스레드를 사용하기 때문에 임계 구간의 충돌을 막기 위한 변수

- 변수
 - matrices : 각 라운드 당 결과를 저장할 6 * 10 * 10 행렬을 저장하는 변수
 - clients : 선택될 수 있는 클라이언트 쌍의 경우의 수를 저장하는 변수
 - non_selected_clients : 선택되지 못한 클라이언트를 저장하는 리스트 변수
 - request_row or col_idx_data : 선택된 클라이언트 쌍에게 임의의 행, 열을 요청을 str 형태로 저장하는 변수
 - data_row or col{n} : 선택된 클라이언트에게 전달받은 임의의 행, 열을 저장하는 변수
 - send_row_col_data{n} : 선택되지 못한 클라이언트에게 임의의 행, 열을 전달하기 위한 str 형태의 변수
 - result_matrix{n} : 선택되지 못한 클라이언트에게 받은 결과를 저장하는 변수

[client.py]

* 프로그램 구성요소 설명
- 함수
 - generate_random_matrix() : 0~100 사이의 임의의 정수 기반의 10 * 10 행렬을 반환하는 함수
 - perform_vector_multiplication(row_vector, col_vector) : 매개변수가 None이 아닌 경우에 해당 행, 열을 행렬 곱셈하여 결과를 반환하는 함수
 - client(c_idx) : 클라이언트 아이디를 매개변수로 하여 해당 아이디를 갖는 클라이언트가 서버와 통신하여 각 조건에 따라 동작하는 함수

- 변수
 - clients_threads : 1~4의 아이디를 갖는 client thread들로 이루어진 리스트
 - client_thread : client()를 타겟 함수로 하는 스레드
 - match : 서버로부터 받은 데이터에서 몇 번째 행, 열을 추출해야 하는지 저장하는 변수
 - row or col_indices : match의 인덱스 데이터를 저장하는 변수
 - row or col_data_str : 클라이언트에서 추출한 행, 열 데이터를 저장하는 변수
 - number_list : 서버로부터 추출된 행, 열 데이터가 저장된 변수
 - result_msg_non_selected_client : perform_vector_multiplication() 함수를 통해 결과를 str 형태로 저장하는 변수


[소스코드 컴파일 방법]
Python 언어로 작성된 소스 코드이기 때문에 별도의 컴파일 과정이 필요하지 않습니다. 소스 코드에 맞는 Python 버전(3.9 이상)과 적절한 IDE이 필요합니다.


[프로그램 실행환경 및 실행방법 설명]

* 프로그램 실행환경
- Python 버전 3.9 & Pycharm community edition 버전 2023.2.3

* 프로그램 실행방법
- 실행시킬 코드를 "Current File"로 설정하고 "Server.py", "Client.py" 각각 "Run" 또는 "Shift + F10"을 이용하여 실행


[Server-Client 및 Client 간 synchronization 및 serialization 수행방법 설명]

* Server-Client 간 synchronization 및 serialization
- synchronization
  :threading.Semaphore(1)인 client_semaphore 사용하여 임계 영역에 대한 액세스를 제어
  client_semaphore.acquire() 사용 세마포어를 획득, client_semaphore.release() 세마포어 해제
  이를 통해 한 번에 한 스레드만 임계 영역을 실행할 수 있도록 하여 경쟁 조건을 방지
- serialization
  Server-Client 간의 데이터는 무조건 str 형태로 변환하여 전송하며
  encode 형식은 socket 통신의 기본값으로 설정

* Client 간 synchronization 및 serialization
- Client 간의 데이터 교환은 전역변수 등을 사용해야 하는 번거로움이 있어 Server를 통해서 데이터를 교환


[Error or Additional Message Handling에 대한 사항 설명]
- 대부분 또는 예상하지 못한 에러는 "Error: {e}" 의 형식으로 출력 및 Log로 저장
- ConnectionReset Error : 서버로부터 연결이 종료되었다는 메시지를 출력 및 Log로 저장
- KeyboardInterrupt : Ctrl + C 또는 Ctrl + D 등으로 프로세스를 종료한 경우는 pass


[Additional Comments: 추가로 과제제출관련 언급할 내용 작성]
- 서버 및 클라이언트의 operation (각 요소별 메시지 전송, 행렬계산, 행렬 update 등)당 1sec
 - 메시지 전송, 행렬 계산, 행렬 업데이트 등을 통틀어서 operation이라고 정의
 - 서버 스레드 1개가 각 operation을 진행, 이때 6개의 스레드가 동시에 실행되므로 라운드 당 1초씩 증가