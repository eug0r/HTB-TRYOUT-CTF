# dontpanic

category: Reversing \
diff: easy

Run the program, it asks for an input string, and unless you are very lucky, you get the "panic" message printed. \
Examining the program with `gdb-pwndbg` we find out it's a rust program(good thing this isn't pwn lol), starting from `__start`, `__libc_ start_call_main` is called, then that in turn calls C's main function which doesn't do anything important other than jumping to `std::rt::lang_start_internal` and after some work, `src::main`, the actual rust main function is called.

---
**src::main** \
inside the main function we push registers, then make 0x58 bytes on the stack (`sub rsp, 0x58`), interestingly enough `rbp`'s value is *zero*, "local" variables are addressed using `rsp` \
inside the main, the flag is passed to a newline trimmer function, which decreases the strlen if it reads trailing newlines. \
Then we call **check_flag**

---
**src::check_flag** \
In check flag, some mysterious stuff happens. Some function pointers are stored on the stack. in the end the only two arguments passed to it and used in the function are the input string and its length (after removing newline, note that removing newline only affects the length, not the memory where the string is stored). \
First we check if strlen is equal to **0x1f** or **31**, we exit if it isn't. \
we supply it with: \
abcdf01239012345678901234567891 \
\
A counter is stored at `r14`! \
it gets copied to `rax` and used with `rbx` (which holds the base of string address), to index into the string and copy it, sign extended to a DWORD, to `edi`. Then the counter, rax, is used again to index into the stack and call one of the functions whose pointer was stored on the stack! On the first iteration, the called function **compares `dil` (input char) against 0x48, the ascii for H**. \
The program panics if the comparison fails. \
 \
We realize that each of those function pointers stored on the stack **point to a function that compares the input against a particular character**, matter of fact, exactly 31 function pointer are stored on the stack, and not all of them are unique: some point to the same function, to account for recurring characters. \
\
So all that's left to do is to interrupt the program after all the functions are stored on the stack, and then read what character they are comparing against. To get that in the correct order, we need to read the function pointers starting from `$rsp+0x10`, upto `$rsp+0x100` \
Here is the script to get the job done, we run it in gdb after all functions are added on the stack:

```python
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
```

After inputting the extracted flag to the program, we get the following output:

```plain-text
🤖💬 < Have you got a message for me? > 🗨️ 🤖: HTB{REDACTED}
😌😌😌 All is well 😌😌😌
```
