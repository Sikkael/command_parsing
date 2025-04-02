import abc
import glob
import os.path
import shutil
import zipfile
from pathlib import Path

from utils import sha256_hashfile
from os import urandom, path, getpid
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from exception import FileStoreError


def compress_files(dirname):
    with zipfile.ZipFile(f'{dirname}.zip', 'w') as fs:
        for file in glob.glob(f'{dirname}/*', recursive=True):
            if os.path.isdir(file):
                for fn in glob.glob(f'{file}/*', recursive=True):
                    fs.write(fn)
            else:
                fs.write(file)


def uncompress_files(zipfilename: str):
    with zipfile.ZipFile(zipfilename, 'r') as f:
        f.extractall("Data\\Decrypted files")


class FileStore(abc.ABC):

    def __init__(self, src_file, dest_file=None):
        self._src_file = src_file
        self._dest_file = dest_file

    def read(self):
        try:
            if os.path.isdir(self.src_file):
                filedir = Path(self.src_file)

                os.chdir(filedir)
                # os.chdir("C:\\Users\\admin\\PycharmProjects\\command_parsing\\Data\\Decrypted files")
                os.chdir("..")
                compress_files(filedir.name)
                self.src_file = os.path.join('Data\\Decrypted files\\', filedir.name + ".zip")
                os.chdir("C:\\Users\\admin\\PycharmProjects\\command_parsing\\")

            with open(self.src_file, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise

    def write(self, res):
        if not self._dest_file:
            self._dest_file = f"tmp--{getpid()}"
            with open(self.dest_file, "wb") as f:
                f.write(res)
            raise FileStoreError(f"Destination file not set\n"
                                 f"Temporary file created--> {self._dest_file}")
        with open(self.dest_file, "wb") as f:
            f.write(res)

        if self.dest_file.rpartition('.')[2] == "zip":
            uncompress_files(self.dest_file)
            os.remove(self.dest_file)
            self.dest_file = self.dest_file.rpartition('.')[0]

    @property
    def src_file(self):
        return self._src_file

    @src_file.setter
    def src_file(self, value):
        self._src_file = value

    @property
    def dest_file(self):
        return self._dest_file

    @dest_file.setter
    def dest_file(self, value):
        self._dest_file = value

    @abc.abstractmethod
    def get_filehash(self):
        raise NotImplementedError()


class Encryptor(FileStore):

    def __init__(self, src_file=False, dest_file=False):

        super(Encryptor, self).__init__(src_file, dest_file)

    def get_filehash(self):
        if not self.src_file:
            return False
        return sha256_hashfile(self.src_file)

    def encrypt_file(self, string=False, key_aes=False, key_chacha=False):
        res = self.encrypt_plaintext(string, key_aes, key_chacha)
        return res[0], res[1], res[2], \
            self.src_file, self.dest_file, self.get_filehash()

    def encrypt_plaintext(self, string=False, key_aes=False, key_chacha=False):
        if not string:
            string = self.read()
        if not key_aes:
            key_aes = urandom(32)
        if not key_chacha:
            key_chacha = urandom(32)

        nonce = urandom(12)
        nonce2 = urandom(12)
        try:
            if not isinstance(string, bytes):
                raise FileStoreError(f"Wrong type -> needed {type(b'')} got -> {type(string)}"
                                     f"string ---> {string}")
            string = nonce + AESGCM(key_aes).encrypt(nonce, string, None)
            string = nonce2 + ChaCha20Poly1305(key_chacha).encrypt(nonce2, string, None)
        except (TypeError, FileStoreError) as err:
            raise err
        return string, key_aes.decode('ISO-8859-1'), key_chacha.decode('ISO-8859-1')


class Decryptor(FileStore):

    def __init__(self, src_file, dest_file=False):
        super(Decryptor, self).__init__(src_file, dest_file)

    def get_filehash(self):
        return sha256_hashfile(self.dest_file)

    def decrypt_file(self, key_aes
                     , key_chacha, string=False
                     ):

        if not string:
            string = self.read()
        try:

            string = ChaCha20Poly1305(key_chacha).decrypt(string[:12], string[12:], None)
        except (ValueError, OverflowError) as err:

            raise err

        return AESGCM(key_aes).decrypt(string[:12], string[12:], None)
