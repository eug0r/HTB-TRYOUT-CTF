Category: Reversing \
Points: 950 \
Diff: very easy

Description: The team stumbles into a long-abandoned casino. As you enter, the lights and music whir to life, and a staff of robots begin moving around and offering games, while skeletons of prewar patrons are slumped at slot machines. A robotic dealer waves you over and promises great wealth if you can win - can you beat the house and gather funds for the mission?

---

The challenge contains only a simple binary, we run a few commands to assess it:
```
$ file casino                                                                                             
casino: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=ac3d9d8a2c65ca7a0cb88af07efaec8c991c315d, for GNU/Linux 3.2.0, not stripped

$ ldd casino 
linux-vdso.so.1 (0x00007f7410fd9000)
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f7410dbe000)
/lib64/ld-linux-x86-64.so.2 (0x00007f7410fdb000)
```

After running it, it displays a banner and asks for an input value, trying out a random input, you are most likely going to see this response:
```
[ * INCORRECT * ]
[ *** ACTIVATING SECURITY SYSTEM - PLEASE VACATE *** ]
```
Assessing it with `strings` also doesn't show anything interesting, besides the potential output for the correct value:
```
[ * CORRECT *]
[ * INCORRECT * ]
[ *** ACTIVATING SECURITY SYSTEM - PLEASE VACATE *** ]
[ ** HOUSE BALANCE $0 - PLEASE COME BACK LATER ** ]
```

So we proceed to open the file in vanilla **gdb** (because elementary Reversing challenges don't deserve a decompiler or control flow view):
```
$ gdb casino
(gdb) disass main

   0x0000000000001185 <+0>:     push   rbp                                       
   0x0000000000001186 <+1>:     mov    rbp,rsp
   0x0000000000001189 <+4>:     sub    rsp,0x10                                  
   0x000000000000118d <+8>:     lea    rdi,[rip+0xf24]        # 0x20b8          
   0x0000000000001194 <+15>:    call   0x1030 <puts@plt>                        
   0x0000000000001199 <+20>:    lea    rdi,[rip+0xe80]        # 0x2020 <banner>  
   0x00000000000011a0 <+27>:    call   0x1030 <puts@plt>                        
   0x00000000000011a5 <+32>:    lea    rdi,[rip+0xf2c]        # 0x20d8           
   0x00000000000011ac <+39>:    call   0x1030 <puts@plt>                        
   0x00000000000011b1 <+44>:    mov    DWORD PTR [rbp-0x4],0x0   
   0x00000000000011b8 <+51>:    jmp    0x1258 <main+211>   
   0x00000000000011bd <+56>:    lea    rdi,[rip+0xf35]        # 0x20f9    
   0x00000000000011c4 <+63>:    mov    eax,0x0        
   0x00000000000011c9 <+68>:    call   0x1040 <printf@plt>
   0x00000000000011ce <+73>:    lea    rax,[rbp-0x5]
   0x00000000000011d2 <+77>:    mov    rsi,rax
   0x00000000000011d5 <+80>:    lea    rdi,[rip+0xf20]        # 0x20fc
   0x00000000000011dc <+87>:    mov    eax,0x0
   0x00000000000011e1 <+92>:    call   0x1060 <__isoc99_scanf@plt>
   0x00000000000011e6 <+97>:    cmp    eax,0x1
   0x00000000000011e9 <+100>:   je     0x11f5 <main+112>
   0x00000000000011eb <+102>:   mov    edi,0xffffffff
   0x00000000000011f0 <+107>:   call   0x1070 <exit@plt>
   0x00000000000011f5 <+112>:   movzx  eax,BYTE PTR [rbp-0x5]
   0x00000000000011f9 <+116>:   movsx  eax,al
   0x00000000000011fc <+119>:   mov    edi,eax
   0x00000000000011fe <+121>:   call   0x1050 <srand@plt>
   0x0000000000001203 <+126>:   call   0x1080 <rand@plt>
   0x0000000000001208 <+131>:   mov    edx,DWORD PTR [rbp-0x4]
   0x000000000000120b <+134>:   movsxd rdx,edx
   0x000000000000120e <+137>:   lea    rcx,[rdx*4+0x0]
   0x0000000000001216 <+145>:   lea    rdx,[rip+0x2e63]        # 0x4080 <check>
   0x000000000000121d <+152>:   mov    edx,DWORD PTR [rcx+rdx*1]
   0x0000000000001220 <+155>:   cmp    eax,edx
   0x0000000000001222 <+157>:   jne    0x1232 <main+173>
   0x0000000000001224 <+159>:   lea    rdi,[rip+0xed5]        # 0x2100
   0x000000000000122b <+166>:   call   0x1030 <puts@plt>
   0x0000000000001230 <+171>:   jmp    0x1254 <main+207>
   0x0000000000001232 <+173>:   lea    rdi,[rip+0xed6]        # 0x210f
   0x0000000000001239 <+180>:   call   0x1030 <puts@plt>
   0x000000000000123e <+185>:   lea    rdi,[rip+0xee3]        # 0x2128
   0x0000000000001245 <+192>:   call   0x1030 <puts@plt>
   0x000000000000124a <+197>:   mov    edi,0xfffffffe
   0x000000000000124f <+202>:   call   0x1070 <exit@plt>
   0x0000000000001254 <+207>:   add    DWORD PTR [rbp-0x4],0x1
   0x0000000000001258 <+211>:   mov    eax,DWORD PTR [rbp-0x4]
   0x000000000000125b <+214>:   cmp    eax,0x1c
   0x000000000000125e <+217>:   jbe    0x11bd <main+56>
   0x0000000000001264 <+223>:   lea    rdi,[rip+0xef5]        # 0x2160
   0x000000000000126b <+230>:   call   0x1030 <puts@plt>
   0x0000000000001270 <+235>:   mov    eax,0x0
   0x0000000000001275 <+240>:   leave
   0x0000000000001276 <+241>:   ret

```

It seems that the main logic is wrapped in a loop, whose counter is stored at `rbp-0x4`, and incremented by 1 at each iteration. The loop continues for `0x1c + 0x1` or 29 iterations. \
Inside the loop, on each iteration, the program reads a single byte (`char`) from the input stream with `scanf`, stores that at `rbp-0x5`. Then it uses the sign-extended double-word conversion of that input to seed libc's `srand` function, and immediately calls `rand` to fill `eax` with the first number (dword) in that seed's generated pseudo-random sequence. \
While `eax` holds the not-so-random number, the program uses the loop counter at `rbp-0x4`, to index into a static array of integers (DWORDs) called "check," and loads a DWORD into `edx`.
Then it compares `eax`, and `edx`. If they are not equal, it prints `**Incorrect**`, else we get `**Correct**` and continue until the counter hits 29. \
So it seems like there is no flag directly involved, but if we print a such a list:
```C
#include <stdlib.h>
#include <stdio.h>
int main(void){
	for(int i = 0; i < 256; i++){
		srand(i);
		int r = rand();
		printf("first random num for seed %d (ascii: %c): %u, hex: 0x%x\n", i, i, r, r);
	}
}
```
and compare it against the first entries of the "check" array, we notice that the seed for the first four entries corresponds to the ASCII encoding of **HTB{** which happens to be the signature of our flag.
So all that's left to do is to automate this matching with a script.
We will use `pwntools` for this:

```python
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
for i in range(29):
	val = target.u32(target.symbols["check"] + i*4)
	#print(f"check val at {i} is {val}")
	flag += randmapping[val]
print(flag)
```
