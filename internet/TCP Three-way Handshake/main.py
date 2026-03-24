from scapy.all import IP, TCP, sr1, conf

# Bước 1: Kiểm tra các interface hiện có (Tùy chọn)
# print(conf.ifaces) 

# Cấu hình mục tiêu
target_ip = "8.8.8.8" 
target_port = 80

print(f"--- Đang thực hiện TCP Handshake trên Windows ---")

# BƯỚC 1: Gửi SYN
# seq=1000 là số tự chọn khởi đầu
syn = IP(dst=target_ip) / TCP(dport=target_port, flags="S", seq=1000)
print(f"[1] Client -> Server: SYN (Seq=1000)")

# BƯỚC 2: Nhận SYN-ACK
# Trên Windows, timeout nên để khoảng 2-3 giây
syn_ack = sr1(syn, timeout=3, verbose=0)

if syn_ack and syn_ack.haslayer(TCP):
    # Lấy thông số từ Server trả về
    srv_seq = syn_ack[TCP].seq
    srv_ack = syn_ack[TCP].ack
    
    if syn_ack[TCP].flags == "SA": # SYN-ACK
        print(f"[2] Server -> Client: SYN-ACK (Seq={srv_seq}, Ack={srv_ack})")
        
        # BƯỚC 3: Gửi ACK hoàn tất
        # Quy tắc: Seq mới = Ack nhận được | Ack mới = Seq nhận được + 1
        ack = IP(dst=target_ip) / TCP(dport=target_port, flags="A", 
                                            seq=srv_ack, 
                                            ack=srv_seq + 1)
        
        # Gửi gói ACK cuối cùng (không đợi phản hồi thêm)
        from scapy.all import send
        send(ack, verbose=0)
        
        print(f"[3] Client -> Server: ACK (Seq={ack[TCP].seq}, Ack={ack[TCP].ack})")
        print("\n--- Kết nối TCP đã thiết lập thành công! ---")
    else:
        print(f"[!] Server phản hồi với Flag: {syn_ack[TCP].flags} (Có thể là RST - Từ chối)")
else:
    print("[!] Không nhận được phản hồi từ Server. Kiểm tra lại kết nối mạng hoặc Firewall.")