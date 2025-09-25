Dump ssembler code from 0x7ffff7fbb000 to 0x7ffff7fbd000:
   0x7ffff7fbb000:	push   r15
   0x7ffff7fbb002:	push   r14
   0x7ffff7fbb004:	push   r13
   0x7ffff7fbb006:	push   r12
   0x7ffff7fbb008:	push   rbp
   0x7ffff7fbb009:	push   rbx
   0x7ffff7fbb00a:	sub    rsp,0x8
   0x7ffff7fbb00e:	mov    ebx,edi
   0x7ffff7fbb010:	mov    r13,rsi
   0x7ffff7fbb013:	mov    rbp,rdx
   0x7ffff7fbb016:	call   0x7ffff7fbb1a4
   0x7ffff7fbb01b:	mov    r12,rax
   0x7ffff7fbb01e:	cmp    ebx,0x1
   0x7ffff7fbb021:	jne    0x7ffff7fbb07a
   0x7ffff7fbb023:	test   rax,rax
   0x7ffff7fbb026:	js     0x7ffff7fbb07a
   0x7ffff7fbb028:	mov    r15,rax
   0x7ffff7fbb02b:	cmp    rax,0x4
   0x7ffff7fbb02f:	jbe    0x7ffff7fbb07a
   0x7ffff7fbb031:	lea    rbx,[r13+0x4]
   0x7ffff7fbb035:	lea    r14,[r13+rax*1+0x0]
   0x7ffff7fbb03a:	add    rbp,r13
   0x7ffff7fbb03d:	jmp    0x7ffff7fbb048
   0x7ffff7fbb03f:	add    rbx,0x1
   0x7ffff7fbb043:	cmp    rbx,r14
   0x7ffff7fbb046:	je     0x7ffff7fbb07a
   0x7ffff7fbb048:	cmp    DWORD PTR [rbx-0x4],0x7b425448
   0x7ffff7fbb04f:	jne    0x7ffff7fbb03f
   0x7ffff7fbb051:	mov    rsi,rbp
   0x7ffff7fbb054:	sub    rsi,rbx
   0x7ffff7fbb057:	mov    rdi,rbx
   0x7ffff7fbb05a:	call   0x7ffff7fbb08c
   0x7ffff7fbb05f:	test   eax,eax
   0x7ffff7fbb061:	je     0x7ffff7fbb03f
   0x7ffff7fbb063:	mov    rdx,r15
   0x7ffff7fbb066:	mov    esi,0x0
   0x7ffff7fbb06b:	mov    rdi,r13
   0x7ffff7fbb06e:	call   0x7ffff7fbb109
   0x7ffff7fbb073:	mov    r12,0xffffffffffffffff
   0x7ffff7fbb07a:	mov    rax,r12
   0x7ffff7fbb07d:	add    rsp,0x8
   0x7ffff7fbb081:	pop    rbx
   0x7ffff7fbb082:	pop    rbp
   0x7ffff7fbb083:	pop    r12
   0x7ffff7fbb085:	pop    r13
   0x7ffff7fbb087:	pop    r14
   0x7ffff7fbb089:	pop    r15
   0x7ffff7fbb08b:	ret
   
   0x7ffff7fbb08c:	movabs rax,0x37593076307b356c
   0x7ffff7fbb096:	movabs rdx,0x3a7c3e753f665666
   0x7ffff7fbb0a0:	mov    QWORD PTR [rsp-0x28],rax
   0x7ffff7fbb0a5:	mov    QWORD PTR [rsp-0x20],rdx
   0x7ffff7fbb0aa:	movabs rax,0x784c7c214f3a7c3e
   0x7ffff7fbb0b4:	movabs rdx,0x663b2c6a246f21
   0x7ffff7fbb0be:	mov    QWORD PTR [rsp-0x1b],rax
   0x7ffff7fbb0c3:	mov    QWORD PTR [rsp-0x13],rdx
   0x7ffff7fbb0c8:	mov    eax,0x0
   0x7ffff7fbb0cd:	lea    rcx,[rsp-0x28]
   0x7ffff7fbb0d2:	test   rsi,rsi
   0x7ffff7fbb0d5:	je     0x7ffff7fbb0fc
   0x7ffff7fbb0d7:	movzx  edx,BYTE PTR [rdi+rax*1]
   0x7ffff7fbb0db:	xor    dl,BYTE PTR [rax+rcx*1]
   0x7ffff7fbb0de:	movsx  rdx,dl
   0x7ffff7fbb0e2:	cmp    rdx,rax
   0x7ffff7fbb0e5:	jne    0x7ffff7fbb103
   0x7ffff7fbb0e7:	add    rax,0x1
   0x7ffff7fbb0eb:	cmp    rsi,rax
   0x7ffff7fbb0ee:	je     0x7ffff7fbb0fd
   0x7ffff7fbb0f0:	cmp    rax,0x1c
   0x7ffff7fbb0f4:	jne    0x7ffff7fbb0d7
   0x7ffff7fbb0f6:	mov    eax,0x1
   0x7ffff7fbb0fb:	ret
   0x7ffff7fbb0fc:	ret
   0x7ffff7fbb0fd:	mov    eax,0x0
   0x7ffff7fbb102:	ret
   0x7ffff7fbb103:	mov    eax,0x0
   0x7ffff7fbb108:	ret
   0x7ffff7fbb109:	test   rdx,rdx
   0x7ffff7fbb10c:	je     0x7ffff7fbb120
   0x7ffff7fbb10e:	mov    rax,rdi
   0x7ffff7fbb111:	add    rdi,rdx
   0x7ffff7fbb114:	mov    BYTE PTR [rax],sil
   0x7ffff7fbb117:	add    rax,0x1
   0x7ffff7fbb11b:	cmp    rax,rdi
   0x7ffff7fbb11e:	jne    0x7ffff7fbb114
   0x7ffff7fbb120:	ret


   0x7ffff7fbb121:	push   r14
   0x7ffff7fbb123:	push   r13
   0x7ffff7fbb125:	push   r12
   0x7ffff7fbb127:	push   rbp
   0x7ffff7fbb128:	push   rbx
   0x7ffff7fbb129:	mov    r11d,edi
   0x7ffff7fbb12c:	mov    QWORD PTR [rsp-0x28],rsi
   0x7ffff7fbb131:	mov    QWORD PTR [rsp-0x20],rdx
   0x7ffff7fbb136:	mov    QWORD PTR [rsp-0x18],rcx
   0x7ffff7fbb13b:	mov    QWORD PTR [rsp-0x10],r8
   0x7ffff7fbb140:	mov    QWORD PTR [rsp-0x8],r9
   0x7ffff7fbb145:	lea    rax,[rsp+0x30]
   0x7ffff7fbb14a:	mov    QWORD PTR [rsp-0x40],rax
   0x7ffff7fbb14f:	lea    rax,[rsp-0x30]
   0x7ffff7fbb154:	mov    QWORD PTR [rsp-0x38],rax
   0x7ffff7fbb159:	mov    rbx,rsi
   0x7ffff7fbb15c:	mov    rbp,rdx
   0x7ffff7fbb15f:	mov    r12,rcx
   0x7ffff7fbb162:	mov    r13,r8
   0x7ffff7fbb165:	mov    DWORD PTR [rsp-0x48],0x30
   0x7ffff7fbb16d:	mov    r14,r9
   0x7ffff7fbb170:	mov    rcx,QWORD PTR [rsp-0x40]
   0x7ffff7fbb175:	lea    rax,[rcx+0x8]
   0x7ffff7fbb179:	mov    QWORD PTR [rsp-0x40],rax
   0x7ffff7fbb17e:	mov    eax,r11d
   0x7ffff7fbb181:	mov    rdi,rbx
   0x7ffff7fbb184:	mov    rsi,rbp
   0x7ffff7fbb187:	mov    rdx,r12
   0x7ffff7fbb18a:	mov    r10,r13
   0x7ffff7fbb18d:	mov    r8,r14
   0x7ffff7fbb190:	mov    r9,QWORD PTR [rcx]
   0x7ffff7fbb193:	syscall
   0x7ffff7fbb195:	mov    r11,rax
   0x7ffff7fbb198:	mov    rax,r11
   0x7ffff7fbb19b:	pop    rbx
   0x7ffff7fbb19c:	pop    rbp
   0x7ffff7fbb19d:	pop    r12
   0x7ffff7fbb19f:	pop    r13
   0x7ffff7fbb1a1:	pop    r14
   0x7ffff7fbb1a3:	ret

   0x7ffff7fbb1a4:	mov    rcx,rdx
   0x7ffff7fbb1a7:	mov    rdx,rsi
   0x7ffff7fbb1aa:	mov    esi,edi
   0x7ffff7fbb1ac:	mov    edi,0x0
   0x7ffff7fbb1b1:	mov    eax,0x0
   0x7ffff7fbb1b6:	call   0x7ffff7fbb121
   0x7ffff7fbb1bb:	ret
