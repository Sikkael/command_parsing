import os

from exception import *

from meta_data_storage import *
from utils import write, append

exists = os.path.exists
join = os.path.join
listdir = os.listdir

DEFAULT_DEC_LOC = "Data\\Decrypted files"

TEST_FILE_LOC = "C:\\Users\\admin\\OneDrive\\Public\\fichiers tests"

root = "C:\\Users\\admin\\PycharmProjects\\command_parsing\\"


class CommandsParser:
    api_key = "6dba0d5c6ab8ee134519b7a119612bb714013fd7"

    commands = ('encrypt', 'decrypt', 'remove', 'list')

    api_index = 1

    com_index = 2

    commands_dict = {k: "" for k in commands}

    cmd_opt_dct = {
        "def": True,
        "oplist": ["opt"],
        "threshold": len(["opt"]) + 3

    }

    _a = "def"
    _opt = "oplist"
    trh = "threshold"

    _error_flag = 0

    def __init__(self, args):
        self._args = args
        self._pos = self.find(self.api_key)
        if self._pos == 1:
            for c in self.commands:
                pos = self.find(c)
                if pos == 2:
                    self._pos = pos

        else:

            self._error_flag = -504
            raise AuthenticationError(-504)

    @property
    def pos(self):

        return self._pos

    @property
    def error_flag(self):
        return self._error_flag

    @property
    def args(self):
        return self._args

    def find(self, a):
        if a in self._args:
            return self._args.index(a)
        else:
            return -1


class SecureStorage:
    poss_loc = [DEFAULT_DEC_LOC, TEST_FILE_LOC]

    def __init__(self, command: CommandsParser):
        self._command = command

        self._actions = {
            "encrypt": self.encrypt,
            "decrypt": self.decrypt,
            "remove": self.remove,
            "list": self.list
        }

        self._action = self._actions[command.args[2]]

    def action(self):
        return self._action()

    def encrypt(self):
        if self._command.pos == len(self._command.args) - 1:
            raise FileStoreError("File argument is missing")

        ptf = self.find_file_to_encrypt()

        if not ptf:
            raise FileStoreError(f"File to encrypt not found"
                                 f"\nGiven file --> {self._command.args[3]}")

        encryptor = Encryptor(ptf)
        res = encryptor.encrypt_file()
        meta_data_storage = MetaDataStorage()

        meta_data_storage.add(res)
        encryptor.dest_file = meta_data_storage.new_encrypted_file()
        encryptor.write(res[0])

        print(
            f"Successfully encrypted {encryptor.src_file} as {encryptor.dest_file}\n"
            f"id:--> {meta_data_storage.new_id()}")

    def decrypt(self):
        if self._command.pos == len(self._command.args) - 1:
            raise FileStoreError("File argument is missing")
        meta_data_storage = MetaDataStorage()
        meta_data = meta_data_storage.find_by_id(int(self._command.args[3]))
        if meta_data:
            file_decryptor = Decryptor(src_file=meta_data.encrypted_file_location,
                                       dest_file=os.path.join(DEFAULT_DEC_LOC, meta_data.name))

            res = file_decryptor.decrypt_file(meta_data.key_aes.encode('ISO-8859-1'),
                                              meta_data.key_chacha.encode('ISO-8859-1'))

            file_decryptor.write(res)

            if os.path.exists(file_decryptor.dest_file):
                os.remove(meta_data.encrypted_file_location)
                meta_data_storage.remove(meta_data.file_key)

                print(
                    f"Successfully decrypted {meta_data.encrypted_file_location} as {file_decryptor.dest_file}")
            else:
                raise FileStoreError("Something went terribly wrong")
        else:
            raise FileStoreError("Can't find file to decrypt")

    def remove(self):
        if self._command.pos == len(self._command.args) - 1:
            raise FileStoreError("File argument is missing")
        meta_data_storage = MetaDataStorage()
        meta_data_obj = meta_data_storage.find_by_id(int(self._command.args[3]))
        if meta_data_obj:
            if meta_data_storage.remove(meta_data_obj.file_key):
                if os.path.exists(meta_data_obj.encrypted_file_location):
                    os.remove(meta_data_obj.encrypted_file_location)

                print(f"File--> {meta_data_obj.file_key} remove with success")

        else:
            print("Can't find file with id--> ", self._command.args[3])

    def list(self, verbose=True):

        _dct_ = MetaDataStorage().get_files

        count = 0
        _tab = "id -> name -> date\n"
        _lines = ""
        for ky in _dct_:
            _d_ = _dct_[ky]
            count += 1
            _line = f"{_d_['id']} -> {_d_['name']} -> {_d_['date']}\n"
            _lines = f"{_lines}{_line}"

        _tab = f"{_tab}{_lines}"
        if verbose:
            print(_tab)
        write("log\\list_log.txt", _tab)

    def find_file_to_encrypt(self):
        basename = str.join(" ", self._command.args[3:])

        if os.path.exists(basename):
            return self._command.args[3]
        else:
            for folder in self.poss_loc:

                if basename in os.listdir(folder):
                    return os.path.join(folder, basename)
            return None


if __name__ == "__main__":

    try:
       log = os.listdir("log")

       for fn in log:
           append("log.txt", f"{fn}")
           append("error_log.txt", f"{fn}")
           with open(os.path.join("log", fn), "r") as reader:

               while reader:
                    line = reader.readline()
                    print(line)
                    argv = line.replace('python ', '').split(' ')
                    if line == "":
                       break

                    com_parser = CommandsParser(argv)
    except Exception as e:
        argv = ["python", "main.py", "6dba0d5c6ab8ee134519b7a119612bb714013fd7", "list"]
        com_parser = CommandsParser(argv)
