# BOF
Buffer Overflow

In case you missed my RE repo (take a look though- its neat 😊 ), as part of my CS B.Sc I took a class in cyber security. In this exercise, I needed to exploit a real vulnerability in existing code on my course VM, and leverage that to gain temporary root permissions. I then use these permissions to install a “backdoor”, to allow myself to regain these root permissions whenever I want to. 

# Attack motivation 
The program I attacked is sudo - a standard program included on Unix systems, and used to execute commands with root permissions.
Like most file systems, each file is owned by a user/group. One of the permissions bits on a file is the setuid bit. When set, this bit causes a program to automatically run under the permissions of the user owning the file. 
The sudo program is owned by the **root** user and has the setuid bit on
When a user tries to use sudo, it checks the user belongs to the sudo’ers user group, and then executes the command. meaning, that if we managed to trick the sudo program believe we are part of the cool kids belong to the group, we going to basically gain root's permissions. 

It should now be clear why it’s attractive to attack the sudo program. With our goal set clearly, let’s begin 😈.

# Part A 
## The Vulnerability
well, as implicit from the repo's name, we are going to take advantage of BOF vulnerability in our sudo program. Lets take a look inside sudo.c: 
![image](https://user-images.githubusercontent.com/112778430/190005433-5cb0e90a-fa8a-4887-8b40-8d4307bcfa16.png)

* sudo.c inside part A

lets notice the fact that the buff array is of size 20. the salt is of size 11, and the input validation validate that the password is not bigger then 10. The check password function concatenating the password to the salt using strcat. Meaning, that if we will give a password of length 10, the last char of the password will actually be in the memory area on the stack allocated for the auth variable, in the first 2 bytes. this very good for us .

## The Attack Itself
in order to get authenticated by sudo, we want that auth will be one: 
meaning that the first 8 bytes of auth need to be : 01000000 (beacue we are in little indian). so, we need that our last char in our password will be 0x01.
meaning that if we will give the password: /x01 * 10 times, we will change auth to 1, and will gain root abilities and could run our command as root:

![image](https://user-images.githubusercontent.com/112778430/190004297-5b9fc5e0-239b-4305-8284-5eee1a59dcc1.png)

Ok so we gained the option to run commands as root. What's now? 
Lets give ourself that for good by adding ourself to the sudo's users group! 

![image](https://user-images.githubusercontent.com/112778430/190006494-c5582e93-604f-4a45-a401-d8d8b17e5d67.png)

# Part B
ok, so rom now on, we will be able to run commands using the real sudo program, not just the one provided by the course. we’ll use this for the next part.

now, the vulnerability from the first question was fixed, a new and much more interesting vulnerability was introduced in a new program We will exploit this vulnerability to open an interactive shell (using /bin/sh) with root privileges. 

## The (new) Vulnerability
again, let's take a quick look at the new sudo program we got:
![image](https://user-images.githubusercontent.com/112778430/190007591-7ea1580b-ec20-499d-981e-9c90d452f035.png)
 
-   sudo.c inside part B

The allocated buff array is of size 65. again, the program concatenating the given password to the salt, this time with no verification of the size of the input. Clearly we can use Buffer over flow here. But, we want to do somethin a bit more sophisticated- open a shell. 
Lucky us, if we manage to override the return address from the function with the vulnerability with assembly commands, the commands we wrote are going to be executed instead of the return to the caller function. 

**First step:**
we want to understand where **exactly** the return address of the function is located on the stack, comparing to the base of the array.
in order to do so, we are going to run aggressively big part of the stack and cause a buffer overflow which will crash the program. this will generate a core dumped file (with the memory image at the moment of the crash!).

how to do it? 
the python code generates the folowing string as input:
AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYY

we are running the sudo program with this string as the first argument (the password) and some command (the command is irrelevant, it is just there so we could get to the check_password function, and not stop on the input validation (The validation on the number of arguments).

this input is to big for the buffer, and resulting a core dumped because we are running over the return adsress of the strcat function with the string.

**Why I chose this string?**
the reason I chose this specific string is because a word is 4 chars, so it will be quite convinient to analyze the memory image when the program crashed using this string string as an input. 

**Second step:**
Because the program ran with the setuid bit on only root level users can view its crash debug file. Luckily for us, we gained exactly that in the first part!

I used GDB for that, and fond where the buffer begins (let’s call this X), and the offset from the beginning of the buffer, we have the value we want to “update” (let’s call this offset Y). Now, we know what we should do - create a buffer of size Y, beginning with the shellcode, followed by padding (if needed) until we reach a length of Y, and then finally add the address X.

Illustration: 
**![](https://lh5.googleusercontent.com/bNfjmV5ip01s9NC4-XiLtwqKCgZVfBPrvrsO_ToyG8eOvZNQ5tpgu5pEX6QNyHYWkk1aoJsBZ0sjLNoYwnYtNMgT92pKd_z4NVpUu21rfYTjR8bE_EekDapv7cS7utTegqWcrpj5sJkvBGLHhtURTNeFKMhz3u92g7iH_R-QRUu4GoZVmpmYh0Hk)**

**Final Part:**
This is the fun part. inside *shellcode.asm I wrote a shellcode that open a terminal for the user. 
we are going to do it by using a syscall to 0x80 (exec), with the following arguments:
1. eax= 0xb (exec command)
2. ebx= /bin/sh (open teminal)
3. ecx= arguments (we'll just put null here) 
4. edx = env varible. null as well. 

**what's the tricky part here?** 
well, there's two actully:
1. Lets remember the fact that this part is copied to the memory by the strcat command. this command stop copying the string when it's arrive to a null terminator char. What does it mean for us? we cant use null terminator (or 0) in our shellcode. We need zero's for the registers. for that, we can xor any register with itself and get zero, without the need of actually writing 0. Also, we will need 0 as null terminator to terminate our "/bin/sh" string. for that, we are simply going to put "@" where the 0 is spose to be, and change the memory of the program dynamically (after the strcat command has already happend) using the lea instruction. 
2. We don't know what is the memory address of the array (And accordantly, of our string of bin/sh). This will be allocated dynamically. 
so, we are going to put the address we want in a "want" segment. At the begging we are going to jump to want, and from there call got. when we are going to call got, the address of the next instruction (which is the /bin/sh string here) is going to be pushed into the stack.
now, we can use this address using our stack, and also nullify the end of (as explained in 1.)
![image](https://user-images.githubusercontent.com/112778430/190011083-8331e9e8-558e-4517-b2db-33c8d783a05d.png)

And that is! 

![image](https://user-images.githubusercontent.com/112778430/190013989-55ac59ce-232e-4ed4-9081-47023d31863b.png)
