xorcipher = "l5{0v0Y7fVf?u>|:O!|Lx!o$j,;f"
key = list()
for i in range(len(xorcipher)):
    key.append(chr(ord(xorcipher[i]) ^ i))
print(f"the key is: {"".join(key)}\nfull flag should be: HTB{"{"}{"".join(key)}\n")