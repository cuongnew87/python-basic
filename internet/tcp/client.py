import socket

def tcp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9999))

    client.send("Hello TCP Server".encode())
    response = client.recv(1024).decode()
    
    print("Server trả về:", response)
    client.close()

tcp_client()