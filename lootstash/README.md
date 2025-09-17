# lootstash

category: reversing \
diff: very easy \

---
running the binary, we get the following output:

```plain-text
$ ./stash 
Diving into the stash - let's see what we can find.
.....
You got: 'Crucifix, Last Stand of Chaos'. Now run, before anyone tries to steal it!
```

The program seems to sleep after each printed dots, for a moment. The "loot" string appears to be random and changes on each run. \
\
We open the program in gdb-pwndbg, and break at main, examining the assembly. \
First of all `setvbuf()` is called, unbuffering stdout. \
Then `time()` is called and the output is used to seed `srand()` \
We enter a loop with its counter, at `rbi-0x4` set to 0, iterate 5 times, printing those dots to stdout, each time sleeping for one second. \
Once that is done, we call `rand()`, and its result is used in the operation: `randno % 0x7f8 >> 3) * 8` (the details of this operation are complicated, modular multiplicative inverse is used for optimization), but in the end the value obtained is added to the QWORD array base pointer "gear". Basically we calculate randno%arraysizeinbytes, arraysizeinbytes being 2040 (hex 0x7f8), then replace leftmost 3 bits with zero so that it's aligned for our QWORD array. The array itself contains pointers to strings or "loots" that will be printed to stdout. \
That's all. We exit after that. \
**Wait what?** so it just indexes an array of strings and prints it? Should we just look into the strings for the flag? \
It appears we forgot to check the needle and heystack case. We quit gdb and run the following command:

```plain-text
$ strings stash | grep HTB
HTB{REDACTED}
```

It was indeed a needle and heystack problem.
