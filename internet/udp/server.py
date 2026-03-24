import socket

def udp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("localhost", 8888))
    print("UDP Server đang lắng nghe")

    data, addr = server.recvfrom(1024)
    print("Nhận từ:", addr, ":", data.decode())

    server.sendto("ACK UDP".encode(), addr)

udp_server()