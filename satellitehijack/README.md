# SatelliteHijack

category: reversing \
points: 1000 \
diff: hard

## Satellite binary

The satellite file is an executable, not stripped, though it seems to be linked against a dynamic library `library.so`, which is stripped. \
It only has the main function.
The main functions prints a banner. Then it sends the "START" string to the `send_satellite_message()` function which belongs to the dynamic library. The function's signature appears to be: `send_satellite_message(int64_t, char *)`, return value is unknown, and `0` is passed as the first argument. \
Next the program allocates a seemingly 1024 byte array on the stack spanning from `rbp-0x410` to `rbp-0x10`, initializing it to zero, then it gets into a `read()` loop, which fills in the array. The number of bytes read will be stored at `rbp-0x8`. The trailing byte will be replaced with *0x00*, so you better not CTRL^D your input. Lastly,  `send_satellite_message(0, char *)` is called with each read, this time with the input buffer passed as the second argument.
It's interesting that apparently a variable on the stack is stored as a struct. How do we know? Because each time a function is called, ghidra will add a `uStack_420 = retaddress` line in the decompilation before the function call. This means its incorrectly displaying the storing of the return address separately (since the stack pointer is already at a 410 byte offset, the return address goes to 420). Now I did a little research and apparently this happens when we involve structs, it should go away if the define a struct with the correct type and size. But let's ignore it for now. \
\
One important thing to note: \
in the call to `read()`, integer 1 is passed as the file descriptor: `read(1, rbp-0x410, 0x400)`. Are we reading from "stdout"? Turns out it doesn't matter with your typicall interactive shell, open a pty device with O_RDWR permissions and duplicate its file descriptor onto fd 0/1/2, so passing STDOUT_FILENO, or STDERR_FILENO to `read()` wouldn't be any different from STDIN_FILENO, as long as we spawned the program from our interactive shell. \
Now why do we call read with 1? that'll come later.

## library.so

### send_satellite_message

This function resides at offset `25d0` \
\
It reserve `0x30` bytes on the stack for locals, using the `rbp-0x10` one for the canary. It stores the string

```plain-text
TBU`QSPE`FOWJSPONFOU
```

on the stack, which it then 'decryptes' to

```plain-text
SAT_PROD_ENVIRONMENT
```

interesting... \
It then calls `getenv("SAT_PROD_ENVIRONMENT)`, if `getenv()` returns NULL, we just load an address to `rax` and returns. But if the variable is found, it first calls another function, `fcn.23e3`, where `23e3` is the offset, then stores the same address as before in `rax` and returns. \
Let's see what happens during dynamic analysis, stepping through the code using **gdb-pwndbg**. \
first time we call `send_satellite_message@plt`, the address is resolved to the function we just examined, we jump into it, since the **SAT_PROD_ENVIRONMENT** environment variable wasn't set, the call to `fcn.2303` is ignored, and the mystertious address is returned. \
Then we observe that the linker (control was returned to `_dl_fixup`) patches the GOT with the address that was just returned... and we jump to it. wait what? \
Also, every next call to `send_satellite_message` resolves to that address instead of the address associated with our symbol. To be specific the address is at offset `24db` from the base of `library.so`, we'll call it `fcn.24db`. \
To break down what happens here, we will run the command `readelf -s library.so`, examining the st_info field of the symbols, one entry looks interesting:

```plain-text
16: 00000000000025d0   166 <OS specific>: 10 GLOBAL DEFAULT   12 send_satellite_m[...]
```

corresponding to the *type* field we have *OS specific* value **10**. What does that mean?
[https://maskray.me/blog/2021-01-18-gnu-indirect-function]

```plaintext
ifunc has a dedicated symbol type STT_GNU_IFUNC to mark it different from a regular function (STT_FUNC). The value 10 is in the OS-specific range (10~12). readelf -s tell you that the symbol is ifunc if OSABI is ELFOSABI_GNU or ELFOSABI_FREEBSD.

On Linux, by default GNU as uses ELFOSABI_NONE (0). If ifunc is used, the OSABI will be changed to ELFOSABI_GNU. Similarly, GNU ld sets the OSABI to ELFOSABI_GNU if ifunc is used. 
```

So what is an IFUNC? [https://sourceware.org/glibc/wiki/GNU_IFUNC]

```plain-text
The GNU indirect function support (IFUNC) is a feature of the GNU toolchain that allows a developer to create multiple implementations of a given function and to select amongst them at runtime using a resolver function which is also written by the developer.
```

Basically, that first function returns the address of the actual function we want to call to. Now we will examine that, and the other function that was called beforehand (fcn.2303)

---

### fcn.24db, the real send_message

`fcn.24db(uint32_t arg1, char *msg)` \
This function takes arg1, checks if it is larger than 4, and errors out (returns `-2`) if it is. Why? because arg1 is then used to index into an array 5 QWORDs: `void *arr[5]`. The array is at offset `0x5080`. The function also checks if the input string is empty and errors out if it is (returns `-22`). \
The QWORDs in the array seem to be string pointers. The array is filled with zeros (NULL pointers) at first, the program checks for this, and if that is the case, it will allocate storage on the heap, copy the input string there, and store the address in the array entry selected via `arg1`. If the array entry wasn't NULL, it will try to **realloc** it to **strcat** the input string to the already existing string. \
So multiple calls to this function would strcat the messages on top of eachother in the corresponding entries of the array, that's all. Although the caller program, `satellite` only ever uses 0 as arg1. \

---

### fcn.23e3, hooked your syscalls

It calls `getauxval(3)`, 3 corresponds to the macro AT_PHDR, so `getauxval` returns the address of the program headers of the executable. Then, the function ANDs this return value with `0xfffffffffffff000`. Which is interesting because program header is generally located at a 64 byte offset, 0x40, for 64-bit binaries. So using that mask, we will be left with the address of the executable's base. \
Then it passes that and the string literal "read" to `fcn.21a9`. Now fcn.21a9 is a very, very messy function, that we haven't gotten into yet, but from dynamic analysis we can figure that it returns the entry for "read" function in the process's **Global Offset Table**, we'll see how that's relevant. \
\
Next it allocates 8k of writable, executable anonymous memory using mmap, `mmap(0, 0x2000, 7, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0)`, and copies 4k bytes at the **11a9** offset from **library.so**'s base into the mapped memory, and it calls `memfrob(mmaped_pointer, 0x1000)`, on that 4k byte. \
\
Now examining what resides at offset **11a9**, we don't find anything interesting at first, but remember memfrob? memfrob XORs each byte of the memory region with the number 42, in an attempt to obfuscate the content. It's probably more of a joke function. So to reverse that we simply copy that whole region over and XOR it with 42 manually. The result is indeed meaningful instructions, saved at `obfusc-code.asm`/`obfusc-code.bin`. \
\
Finally, it rewrites the address pointed by the return value of `fcn.21a9` with the address of our memory-mapped region (the deobfuscated code). \
So... normally, when the `satellite` program, which is dynamically linked, runs and calls read, we lookup the address for it in .got.plt section, some magic happens or has already happened and we'd have the address of `read()` where `libc` is loaded in the memory. However, since that entry in .got.plt has been overwritten by `fcn.23e3` (given that the environment variable **SAT_PROD_ENVIRONMENT** was present and `fcn.23e3` was called by the send_satellite_message runtime ifunc), now each call to `read()` will cause the control to jump into the mysterious deobfuscated code instead. \
There we go, `read` has been hooked.

---

## The alternative read()

There are a couple of functions here, named using their offsets:
`fcn.000` `fcn.8c` `fcn.109` `fcn.121` `fcn.1a4` \

### fcn.000: entering

We obviously jump into `fcn.000(int32_t fd, void *buf, uint64_t count)` which is the entry point. Starting there, `fcn.1a4` gets called, which in turn calls `fcn.121`, `fcn.121` is the part where we directly use the `syscall` instruction with the same arguments that the user passed. By the time we return the control to `fcn.000`, that's the only important thing that has happened. \
Now from here multiple checks are performed, each failure causes the return to the caller program, with the number of read bytes as the return value: *normal read behavior*, you wouldn't notice anything funky going on. \
The checks are as follows:

- file descriptor should equal 1 (remember how that was brought up earlier?)
- return value of the read syscall should be positive
- return value of the read syscall should be larger than 4, we need to read more than 4 bytes.

the next check happens by comparing the first 4 bytes of the read buffer against a DWORD that consists of four ascii chars (you must account for the endianness). If the check fails, we simply increment the buffer address by one and check again, until we reach the end of the buffer.

- The checked 4 bytes of the buffer should equal to "HTB{"

Interesting, this seems like the start of the flag check. Next, `fcn.8c` is called. the arguments passed to it is the address of the first byte into the buffer past where 'HTB{' was located. Along with the number of remaining bytes. \

### fcn.8c: flag check, finally

Inside `fcn.8c`, we load a cipher string of 28 characters onto the stack, starting from `rsp-0x28` and ending before `rsp-0xc`. then we use rax as an index, indexing into the cipher string and the input string, selecting bytes at the corresponding index. \
Here is the magic:

1. the byte/character selected from the cipher string and the input string will be XOR'ed together
2. the result is compared against the index (rax), if they aren't equal, flag check fails, we return from this function, and `fcn.000`, as if only a normal read happened.
3. if they are equal, we continue on, until the end of the cipher string. If the flag check succeeds, the function returns 1, and `fcn.000` returns -1, indicating to the caller program that **read "failed"**... so no congratulation messages. \

A little boolean algebra:

```plain_text
Cipher_byte ^ Input_Byte = index

then:
Cipher_byte ^ Input_Byte ^ index = index ^ index = 0

then:
Cipher_byte ^ Input_Byte ^ index ^ Input_Byte = 0 ^ Input_byte = Input_byte

and the LHS simplifies to:
Cipher_byte ^ (Input_Byte ^ Input_Byte) ^ index = Cipher_byte ^ index

so we have:
Cipher_byte ^ index = Input_byte
```

Basically, all we have to do is to XOR each byte from the cipher text to recover the desired input (flag). The following python script does just that:

```python
xorcipher = "l5{0v0Y7fVf?u>|:O!|Lx!o$j,;f"
key = list()
for i in range(len(xorcipher)):
    key.append(chr(ord(xorcipher[i]) ^ i))
print(f"the key is: {"".join(key)}\nfull flag should be: HTB{"{"}{"".join(key)}\n")
```

Running it we get:

```plain-text
full flag should be: HTB{REDACTED}
```
