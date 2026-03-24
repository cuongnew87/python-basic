import socket

def http_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8080))
    server.listen(1)
    print("HTTP Server chạy tại http://localhost:8080")

    while True:
        conn, addr = server.accept()
        request = conn.recv(1024).decode()
        print("Request:\n", request)

        body = "<html><body><h1>Hello World</h1></body></html>"

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
            "\r\n"
            + body
        )

        conn.send(response.encode())
        conn.close()

http_server()