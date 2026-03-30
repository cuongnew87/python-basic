from ctypes import *

print(c_int())
c_char_p(b"Hello!")
print(c_ushort(-5).value)
seitz = c_char_p(b"python")
print(seitz.value)

# Đoạn văn này trong sách Gray Hat Python đang giải thích về cách khai báo và khởi tạo các kiểu dữ liệu của C ngay trong Python thông qua thư viện ctypes.
# Nói cách khác, nó hướng dẫn bạn cách tạo ra các biến mà ngôn ngữ C có thể hiểu được (như số nguyên int, con trỏ chuỗi char*, hay số nguyên ngắn ushort).