import ctypes

msvcrt = ctypes.cdll.msvcrt
message_string = b"Hello World!\n"
msvcrt.printf(b"Testing %s", message_string)
