import ctypes
from pwn import *

randmapping = {}
libc = ctypes.CDLL("libc.so.6")
libc.srand.argtypes = [ctypes.c_uint]
libc.srand.restype = None
libc.rand.argtypes = []
libc.rand.restype = ctypes.c_uint32
for ascii_val in range(32, 127):
    char = chr(ascii_val)
    libc.srand(ascii_val)
    rand_result = libc.rand()
    randmapping[rand_result] = chr(ascii_val)
    #print(f"'{char}' ({ascii_val}) produced {rand_result} hex: 0x{rand_result:08x}")

#print(randmapping.items)

flag = ""
target = ELF("./casino", checksec=False)
target.symbols['check']
for i in range(29):
    val = target.u32(target.symbols["check"] + i*4)
    #print(f"check val at {i} is {val}")
    flag += randmapping[val]
print(flag)