import my_debugger
from my_debugger_defines import *

debugger = my_debugger.debugger()
pid = input("Enter the PID of the process to attach to: ")
debugger.attach(int(pid))
debugger.run()
# thread_list = debugger.enumerate_threads()
# # debugger.run()
# for thread in thread_list:
#     # 1. Mở handle luồng
#     h_thread = debugger.open_thread(thread)
    
#     # 2. TẠM DỪNG LUỒNG trước khi lấy context
#     debugger.kernel32.SuspendThread(h_thread)
    
#     thread_context = debugger.get_thread_context(thread)
    
#     if thread_context:
#         rax_value = thread_context.Rax
#         print(f"[*] Dumping registers for thread ID: 0x{thread:08x}")

#         print(f"[**] RIP: 0x{thread_context.Rip:016x}") # RIP (instruction pointer) là con trỏ lệnh, rất quan trọng để biết luồng đang thực thi ở đâu
#         print(f"[**] RSP: 0x{thread_context.Rsp:016x}") # RSP (stack pointer) là con trỏ ngăn xếp, giúp ta biết được vị trí ngăn xếp hiện tại của luồng
#         print(f"[**] RAX: 0x{thread_context.Rax:016x}") # RAX (accumulator) thường được dùng để trả về giá trị của hàm, nên biết RAX có thể giúp ta hiểu được kết quả của các cuộc gọi hàm gần đây

#         opcode = debugger.read_process_memory(thread_context.Rip, 5)
#         if opcode:
#             # Chuyển byte sang dạng hex để dễ nhìn
#             hex_opcode = "".join(f"{b:02x} " for b in opcode)
#             print(f"  [->] Opcode at RIP: {hex_opcode}")

#         # Thử "dịch" RAX: Đọc 16 byte tại địa chỉ mà RAX trỏ tới
#         if rax_value > 0x10000: # Chỉ đọc nếu giá trị RAX trông giống một địa chỉ bộ nhớ
#             content = debugger.read_process_memory(rax_value, 16)
#             if content:
#                 print(f"  [->] Memory at RAX: {content}")
#         print("[*] END DUMP")
#     else:
#         print(f"[!] Could not get context for thread 0x{thread:08x}")

#     # 3. KHÔI PHỤC LUỒNG sau khi lấy xong
#     debugger.kernel32.ResumeThread(h_thread)
#     debugger.kernel32.CloseHandle(h_thread)

# debugger.detach()