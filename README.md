# BOF
Buffer Overflow

In case you missed my RE repo (take a look though- its neet 😊 ), as part of my CS B.Sc I took a class in cybey secuirty. In this exercise, I needed to exploit a real vulnerability in existing code on my course VM, and leverage that to gain temporary root permissions. I then use these permissions to install a “backdoor”, to allow myself to regain these root permissions whenever I want to. 

# Attack motivation 
The program I attacked is sudo - a standard program included on Unix systems, and used to execute commands with root permissions.
Like most file systems, each file is owned by a user/group. One of the permissions bits on a file is the setuid bit. When set, this bit causes a program to automatically run under the permissions of the user owning the file. 
The sudo program is owned by the **root** user and has the setuid bit on
When a user tries to use sudo, it checks the user belongs to the sudo’ers user group, and then executes the command. meaning, that if we managed to trick the sudo program belive we are part of the cool kids belong to the group, we going to basiclly gain root's permissions. 

It should now be clear why it’s attractive to attack the sudo program. With our goal set clearly, let’s begin 😈.

# Part A 





