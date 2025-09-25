msg = "TBU`QSPE`FOWJSPONFOU"
ascii_list = list()
for i in msg:
    ascii_list.append(ord(i))
for i in ascii_list:
    print(chr(i), end="")
print()
for i in ascii_list:
    print(chr(i-1), end="")