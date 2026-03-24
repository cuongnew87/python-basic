import socket

def udp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto("Hello UDP Server".encode(), ("localhost", 8888))
    data, _ = client.recvfrom(1024)
    
    print("Server trả về:", data.decode())

udp_client()