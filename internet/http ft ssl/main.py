import socket
import ssl

hostname = 'www.google.com'
context = ssl.create_default_context()

# Thiết lập socket tầng thấp
with socket.create_connection((hostname, 443)) as sock:
    # Bọc socket bằng lớp bảo mật SSL/TLS
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(f"--- Kết nối an toàn được thiết lập ---")
        print(f"Phiên bản TLS đang dùng: {ssock.version()}")
        
        # Lấy thông tin chứng chỉ số (Certificate)
        # Lấy toàn bộ thông tin chứng chỉ
        cert = ssock.getpeercert()

        # Hàm trợ giúp để lấy giá trị từ cấu trúc phức tạp của subject
        def get_cert_subject_val(subject, key_name):
            for item in subject:
                for rdn in item:
                    if rdn[0] == key_name:
                        return rdn[1]
            return "N/A"

        common_name = get_cert_subject_val(cert['subject'], 'commonName')
        org_name = get_cert_subject_val(cert['subject'], 'organizationName')

        print(f"--- Thông tin chứng chỉ ---")
        print(f"Common Name (Tên miền): {common_name}")
        print(f"Organization (Tổ chức): {org_name}")
        print(f"Ngày hết hạn: {cert['notAfter']}")

        # Gửi một HTTP Request đơn giản qua kênh đã mã hóa
        request = f"GET / HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
        ssock.sendall(request.encode())

        # Nhận phản hồi
        response = ssock.recv(1024)
        print(f"\nPhản hồi từ Server (1024 bytes đầu): \n{response.decode('utf-8', errors='ignore')}")