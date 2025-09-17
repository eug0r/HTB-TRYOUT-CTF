python
import re
import gdb
counter = 0x10
flag = []

while counter <= 0x100:
    addrspec = f"*(long *)($rsp+{counter})+1" #we skip the push instruct
    disas_cmd = f"disas {addrspec}, +4" #we specify a 4 byte instruct
    out = gdb.execute(disas_cmd, to_string=True)

    #we expect an output in the form cmp dil,0xXX
    #we try to match the pattern and extract the number XX
    pattern = r'cmp\s+dil,\s*0x([0-9a-fA-F]+)'
    match = re.search(pattern, out)
    if match:
        hex_value = match.group(1)
        decimal_value = int(hex_value, 16)
        flag.append(decimal_value)
    else:
        print(f"examining $rsp+{counter}+1, +4")
        print(f"no 'cmp dil, 0xXX' pattern found in output:")
        print(f"{repr(out)}")
    counter += 0x8

print("\n\n" +  "="*50 + "extracted flag:")
print("as hex:  ", [hex(x) for x in flag])
print("as string:     ", ''.join(chr(x) if 32 <= x <= 126 else f'\\x{x:02x}' for x in flag))