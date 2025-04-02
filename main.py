from sys import *

from console_parser import CommandsParser, SecureStorage

if __name__ == "__main__":

    com_parser = CommandsParser(argv)
    sec = SecureStorage(com_parser)
    sec.action()
# migration