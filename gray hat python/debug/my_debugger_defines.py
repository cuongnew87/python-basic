from ctypes import *

# --- Định nghĩa các kiểu dữ liệu Windows sang ctypes ---
BYTE      = c_ubyte
WORD      = c_ushort
DWORD     = c_ulong
DWORD64   = c_uint64
HANDLE    = c_void_p
PVOID     = c_void_p
LPVOID    = c_void_p
SIZE_T    = c_size_t
UINT_PTR  = c_uint64
LONG_PTR  = c_int64

# --- Các hằng số điều khiển ---
PROCESS_ALL_ACCESS = 0x001F0FFF
THREAD_ALL_ACCESS  = 0x001F03FF
INFINITE           = 0xFFFFFFFF
TH32CS_SNAPTHREAD = 0x00000004

# Các hằng số sự kiện Debug
EXCEPTION_DEBUG_EVENT      = 0x1
CREATE_THREAD_DEBUG_EVENT  = 0x2
CREATE_PROCESS_DEBUG_EVENT = 0x3
EXIT_THREAD_DEBUG_EVENT    = 0x4
EXIT_PROCESS_DEBUG_EVENT   = 0x5
LOAD_DLL_DEBUG_EVENT       = 0x6
UNLOAD_DLL_DEBUG_EVENT     = 0x7
OUTPUT_DEBUG_STRING_EVENT  = 0x8
RIP_EVENT                  = 0x9

# Các mã ngoại lệ (Exception codes)
EXCEPTION_ACCESS_VIOLATION = 0xC0000005
EXCEPTION_BREAKPOINT       = 0x80000003
EXCEPTION_GUARD_PAGE       = 0x80000001
EXCEPTION_SINGLE_STEP      = 0x80000004
DBG_CONTINUE                = 0x00010002
DBG_EXCEPTION_NOT_HANDLED   = 0x80010001

# Context Flags cho x64
CONTEXT_AMD64 = 0x00100000
CONTEXT_CONTROL = (CONTEXT_AMD64 | 0x00000001)
CONTEXT_INTEGER = (CONTEXT_AMD64 | 0x00000002)
CONTEXT_SEGMENTS = (CONTEXT_AMD64 | 0x00000004)
CONTEXT_FLOATING_POINT = (CONTEXT_AMD64 | 0x00000008)
CONTEXT_DEBUG_REGISTERS = (CONTEXT_AMD64 | 0x00000010)

CONTEXT_FULL = (CONTEXT_CONTROL | CONTEXT_INTEGER | CONTEXT_SEGMENTS)

# Cấu trúc M128A cho phần Floating Point (bắt buộc phải có để đủ kích thước)
class M128A(Structure):
    _fields_ = [
        ("Low", DWORD64),
        ("High", DWORD64),
    ]

class CONTEXT(Structure):
    _pack_ = 16 # Bắt buộc phải căn lề 16-byte cho Windows x64
    _fields_ = [
        ("P1Home", DWORD64), ("P2Home", DWORD64), ("P3Home", DWORD64),
        ("P4Home", DWORD64), ("P5Home", DWORD64), ("P6Home", DWORD64),
        ("ContextFlags", DWORD),
        ("MxCsr", DWORD),
        ("SegCs", WORD), ("SegDs", WORD), ("SegEs", WORD),
        ("SegFs", WORD), ("SegGs", WORD), ("SegSs", WORD),
        ("EFlags", DWORD),
        ("Dr0", DWORD64), ("Dr1", DWORD64), ("Dr2", DWORD64),
        ("Dr3", DWORD64), ("Dr6", DWORD64), ("Dr7", DWORD64),
        ("Rax", DWORD64), ("Rcx", DWORD64), ("Rdx", DWORD64),
        ("Rbx", DWORD64), ("Rsp", DWORD64), ("Rbp", DWORD64),
        ("Rsi", DWORD64), ("Rdi", DWORD64),
        ("R8",  DWORD64), ("R9",  DWORD64), ("R10", DWORD64),
        ("R11", DWORD64), ("R12", DWORD64), ("R13", DWORD64),
        ("R14", DWORD64), ("R15", DWORD64),
        ("Rip", DWORD64),
        ("Header", M128A * 2),
        ("Legacy", M128A * 8),
        ("Xmm0",  M128A), ("Xmm1",  M128A), ("Xmm2",  M128A), ("Xmm3",  M128A),
        ("Xmm4",  M128A), ("Xmm5",  M128A), ("Xmm6",  M128A), ("Xmm7",  M128A),
        ("Xmm8",  M128A), ("Xmm9",  M128A), ("Xmm10", M128A), ("Xmm11", M128A),
        ("Xmm12", M128A), ("Xmm13", M128A), ("Xmm14", M128A), ("Xmm15", M128A),
        # ... còn một số trường vector khác nhưng tới đây là đủ để lấy Rip/Rax
    ]

# --- Các cấu trúc khác giữ nguyên như cũ ---
class THREADENTRY32(Structure):
    _fields_ = [
        ("dwSize",             DWORD),
        ("cntUsage",           DWORD),
        ("th32ThreadID",       DWORD),
        ("th32OwnerProcessID", DWORD),
        ("tpBasePri",          DWORD),
        ("tpDeltaPri",         DWORD),
        ("dwFlags",            DWORD),
    ]

class EXCEPTION_RECORD(Structure):
    pass

EXCEPTION_RECORD._fields_ = [
    ("ExceptionCode",        DWORD),
    ("ExceptionFlags",       DWORD),
    ("ExceptionRecord",      POINTER(EXCEPTION_RECORD)),
    ("ExceptionAddress",     PVOID),
    ("NumberParameters",     DWORD),
    ("ExceptionInformation", UINT_PTR * 15),
]

class EXCEPTION_DEBUG_INFO(Structure):
    _fields_ = [
        ("ExceptionRecord", EXCEPTION_RECORD),
        ("dwFirstChance",   DWORD),
    ]

class CREATE_THREAD_DEBUG_INFO(Structure):
    _fields_ = [
        ("hThread",           HANDLE),
        ("lpThreadLocalBase", LPVOID),
        ("lpStartAddress",    LPVOID),
    ]

class CREATE_PROCESS_DEBUG_INFO(Structure):
    _fields_ = [
        ("hFile",                 HANDLE),
        ("hProcess",              HANDLE),
        ("hThread",               HANDLE),
        ("lpBaseOfImage",         LPVOID),
        ("dwDebugInfoFileOffset", DWORD),
        ("nDebugInfoSize",        DWORD),
        ("lpThreadLocalBase",     LPVOID),
        ("lpStartAddress",        LPVOID),
        ("lpImageName",           LPVOID),
        ("fUnicode",              WORD),
    ]

# Cấu trúc Union quan trọng nhất
class DEBUG_EVENT_UNION(Union):
    _fields_ = [
        ("Exception",         EXCEPTION_DEBUG_INFO),
        ("CreateThread",      CREATE_THREAD_DEBUG_INFO),
        ("CreateProcess",     CREATE_PROCESS_DEBUG_INFO),
    ]

class DEBUG_EVENT(Structure):
    _fields_ = [
        ("dwDebugEventCode", DWORD),
        ("dwProcessId",      DWORD),
        ("dwThreadId",       DWORD),
        ("u",                DEBUG_EVENT_UNION),
    ]