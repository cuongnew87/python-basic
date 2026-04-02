from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32

class debugger():
    def __init__(self):
        self.h_process       = None
        self.pid             = None
        self.debugger_active = False
        self.kernel32        = windll.kernel32

        # KHAI BÁO KIỂU DỮ LIỆU CHO READPROCESSMEMORY (QUAN TRỌNG)
        self.kernel32.ReadProcessMemory.argtypes = [
            HANDLE,   # hProcess
            LPVOID,   # lpBaseAddress (Đây là nơi gây ra lỗi overflow)
            LPVOID,   # lpBuffer
            SIZE_T,   # nSize
            POINTER(c_ulonglong) # lpNumberOfBytesRead
        ]
        self.get_debug_privileges()

    def open_process(self, pid):
        # Lấy quyền kiểm soát toàn bộ tiến trình (PROCESS_ALL_ACCESS)
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        return h_process

    def attach(self, pid):
        self.h_process = self.open_process(pid)
        
        # Cố gắng đính kèm vào tiến trình đang chạy
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid = int(pid)
            print(f"[*] Attached to process: {pid}")
        else:
            print("[*] Unable to attach to the process.")

    def run(self):
        # Vòng lặp Debug chính
        print("[*] Waiting for debug events...")
        while self.debugger_active:
            self.get_debug_event()

    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE
        
        # Đợi vô hạn cho đến khi có sự kiện (như Breakpoint, Exception...)
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            # Hiện tại chưa xử lý gì, chỉ dừng lại để bạn quan sát
            # input("Press Enter to continue the debuggee...")
            print(f"[*] Event Code: {debug_event.dwDebugEventCode} từ Thread ID: {debug_event.dwThreadId}")

            # Nếu muốn biết chi tiết hơn về loại sự kiện:
            if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
                exception_code = debug_event.u.Exception.ExceptionRecord.ExceptionCode
                print(f"[!] EXCEPTION xảy ra! Mã lỗi: {hex(exception_code)}")
            
            # Sau khi nhấn Enter, cho phép chương trình chạy tiếp
            kernel32.ContinueDebugEvent(
                debug_event.dwProcessId,
                debug_event.dwThreadId,
                continue_status
            )
            
            # Tạm thời thoát vòng lặp sau 1 sự kiện để thử nghiệm
            # self.debugger_active = False

    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print("[*] Finished debugging. Exiting...")
            return True
        else:
            print("[*] There was an error detaching.")
            return False
        
    def open_thread (self, thread_id):
        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, False, thread_id)
        if h_thread:
            return h_thread
        else:
            print("[*] Could not obtain a valid thread handle.")
            return False

    def enumerate_threads(self):
        thread_entry = THREADENTRY32()
        thread_list = []
        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, self.pid)
        if snapshot  != -1:
            # You have to set the size of the struct
            # or the call will fail
            thread_entry.dwSize = sizeof(thread_entry)
            success = kernel32.Thread32First(snapshot, byref(thread_entry))

            while success:
                if thread_entry.th32OwnerProcessID == self.pid:
                    thread_list.append(thread_entry.th32ThreadID)
                success = kernel32.Thread32Next(snapshot, byref(thread_entry))
            kernel32.CloseHandle(snapshot)
            return thread_list
        else:
            return False

    def get_thread_context (self, thread_id):
        context = CONTEXT()
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS
        # Obtain a handle to the thread
        h_thread = self.open_thread(thread_id)
        if kernel32.GetThreadContext(h_thread, byref(context)):
            kernel32.CloseHandle(h_thread)
            return context
        else:
            print(f"[!] GetThreadContext failed. Error: {kernel32.GetLastError()}")
            kernel32.CloseHandle(h_thread)
        return False
    
    def get_debug_privileges(self):
        import win32api, win32con, win32security
        # Mở token của tiến trình hiện tại (Python)
        h_token = win32security.OpenProcessToken(win32api.GetCurrentProcess(), 
                  win32con.TOKEN_ADJUST_PRIVILEGES | win32con.TOKEN_QUERY)
        # Tìm ID của quyền Debug
        luid = win32security.LookupPrivilegeValue(None, win32con.SE_DEBUG_NAME)
        # Kích hoạt quyền
        win32security.AdjustTokenPrivileges(h_token, 0, [(luid, win32con.SE_PRIVILEGE_ENABLED)])

    def read_process_memory(self, address, length):
        data = create_string_buffer(length)
        read_bytes = c_ulonglong(0) # Dùng ulonglong cho 64-bit

        if kernel32.ReadProcessMemory(self.h_process, address, data, length, byref(read_bytes)):
            return data.raw
        else:
            return False
        
# 1. Hàm open_thread(self, thread_id)
# Mục đích: Xin quyền truy cập vào một Luồng (Thread) cụ thể.
# Cơ chế: Trong Windows, bạn không thể tự tiện đọc dữ liệu của một Thread chỉ bằng ID của nó. Bạn phải gửi một yêu cầu đến Kernel (nhân hệ điều hành) để lấy một Handle (tay cầm).
# Tham số THREAD_ALL_ACCESS: Bạn đang xin quyền cao nhất: dừng luồng, chạy luồng, đọc thanh ghi, ghi đè thanh ghi...
# Tại sao cần nó? Vì các hàm tiếp theo như GetThreadContext bắt buộc phải có "chiếc chìa khóa" Handle này mới hoạt động được.
# 2. Hàm enumerate_threads(self
# Mục đích: Lập danh sách ID của TẤT CẢ các luồng đang chạy trong tiến trình mục tiêu.
# Tại sao phải làm vậy? Một chương trình (như Chrome hay Game) không chỉ có 1 luồng. Nó có hàng chục luồng chạy song song. Nếu bạn muốn dừng chương trình hoặc đặt Hardware Breakpoint, bạn phải tác động lên từng luồng một.
# Cơ chế CreateToolhelp32Snapshot: Hàm này chụp một "bức ảnh" toàn cảnh hệ thống tại thời điểm đó.
# Vòng lặp Thread32First / Thread32Next: Bạn duyệt qua "bức ảnh" đó, kiểm tra xem luồng nào có th32OwnerProcessID trùng với PID của bạn thì bỏ vào danh sách.
# 3. Hàm get_thread_context(self, thread_id)
# Mục đích: Trích xuất giá trị các Thanh ghi CPU (EAX, EBX, EIP, ESP...) của một luồng. Đây là phần "hack" nhất!
# CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS: Dòng này cực kỳ quan trọng. Bạn đang nói với CPU: "Hãy đưa cho tôi toàn bộ các thanh ghi đa năng VÀ cả các thanh ghi dùng để Debug (Dr0-Dr7)".
# Cơ chế: Khi một chương trình bị Debugger dừng lại (ví dụ gặp Soft Breakpoint), CPU sẽ tạm thời lưu trạng thái của nó vào bộ nhớ. Hàm GetThreadContext sẽ copy trạng thái đó vào struct CONTEXT trong Python của bạn.
# Ứng dụng: * Xem EIP: Biết chương trình sắp chạy lệnh nào tiếp theo.
# Xem EAX: Biết kết quả trả về của một hàm (ví dụ hàm kiểm tra Serial Key đúng hay sai).
# Xem ESP: Biết dữ liệu trên Stack.