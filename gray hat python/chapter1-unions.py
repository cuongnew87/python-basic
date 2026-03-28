from ctypes import *

class barley_amount(Union):
    _fields_ = [
        ("barley_long", c_long),
        ("barley_int", c_int),
        ("barley_char", c_char * 8),
    ]

value = input("Enter the amount of barley to put into the beer vat:")
my_barley = barley_amount(int(value))
print("Barley amount as a long: %ld" % my_barley.barley_long)
print("Barley amount as an int: %d" % my_barley.barley_int)
print("Barley amount as a char: %s" % my_barley.barley_char)

# Union là gì? (Phần quan trọng nhất)
# Trong sách Gray Hat Python, việc hiểu về Union là chìa khóa để bạn làm việc với bộ nhớ (memory) và các gói tin mạng (packets).
# Sự khá biệt với Structure: Trong một Structure, mỗi trường (field) có một vùng nhớ riêng. 
# Nhưng trong một Union, tất cả các trường dùng chung một vùng nhớ duy nhất. 
# Kích thước của Union bằng kích thước của trường lớn nhất.
# Mục đích: Union cho phép bạn nhìn cùng một dữ liệu dưới nhiều "ống kính" khác nhau.