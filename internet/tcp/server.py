import socket

def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 9999))
    server.listen(1)
    print("TCP Server đang lắng nghe")

    conn, addr = server.accept()
    print("Kết nối từ:", addr)

    data = conn.recv(1024).decode()
    print("Nhận:", data)

    conn.send("ACK từ server".encode())
    conn.close()

tcp_server()