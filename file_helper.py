import glob
import os
import zipfile
from sys import *
from random import randint

fold = ["C:\\Users\\mouel\\OneDrive\\Bureau\\fichiers tests\\CrystalReportViewer.xlsx",
        "C:\\Users\\mouel\\OneDrive\\Bureau\\fichiers tests\\Formulaires personnalisés_2022_03_28.pdf",
        "C:\\Users\\mouel\\OneDrive\\Bureau\\fichiers "
        "tests\\how-to-think-like-a-computer-scientist-c-plus-plus-version.pdf",
        "C:\\Users\\mouel\\OneDrive\\Bureau\\fichiers tests\\Net.html",
        "C:\\Users\\mouel\\OneDrive\\Bureau\\fichiers tests\\Nouveau Feuille de calcul Microsoft Excel.xlsx",
        ]

enc_loc = "Data\\Encrypted files"

default_dec_loc = "C:\\Users\\mouel\\PycharmProjects\\SecureStorage\\Data\\Decrypted files\\"
test_dec_loc = "C:\\Users\\admin\\OneDrive\\Public\\fichiers tests\\"

poss_loc = ['', default_dec_loc, test_dec_loc]

poubelle = "C:\\Users\\mouel\\OneDrive\\Bureau\\poubelle"

dec_loc = [
    default_dec_loc,
    "C:\\Users\\mouel\\OneDrive\\Bureau\\fichiers tests\\"

]

LOG_FILES_LOC = "C:\\Users\\admin\\OneDrive\\Public\\log"

meta_enc = 'Data\\files.ENCRYPTED'

tmp_dec_loc = "C:\\Users\\mouel\\PycharmProjects\\SecureStorage\\Data\\Temp decrypted files"

tmp_enc_loc = "C:\\Users\\mouel\\PycharmProjects\\SecureStorage\\Data\\Temp Encrypted files"

enc_loc_trash = "C:\\Users\\mouel\\PycharmProjects\\SecureStorage\\Data\\Encrypted files trash"


def random_filename():
    file_name = str(randint(1000000000, 9999999999))
    return file_name


def random_filename_in_folder(pth, ext):
    if ext == '':
        xt = ''
    else:
        xt = f".{ext}"
    filename = f"{pth}\\{random_filename()}{xt}"

    return filename


def create_filename_exist(pth, ext):
    if ext == '':
        xt = ''
    else:
        xt = f".{ext}"
    rand_name = random_filename()
    p = f"{pth}\\{rand_name}{xt}"
    extless_filename = p.rpartition('.')[0].rpartition('\\')[2]
    return os.path.exists(p), p, extless_filename


def do_until_unique(pth, ext):
    exist, p, extless_filename = create_filename_exist(pth, ext)
    count = 0
    if exist:
        while True:
            p: str
            exist, p, extless_filename = create_filename_exist(pth, ext)
            if not exist:
                return p
            else:
                count += 1
            if count >= 1000:
                print("problem creating encrypted filename")
                exit(-7000)


def compress_files(dirname):
    with zipfile.ZipFile(f'{dirname}.zip', 'w') as f:
        for file in glob.glob(f'{dirname}/*'):
            f.write(file)


class FileHelper:

    def __init__(self, file_path_name):
        self._file_path_name = file_path_name
        self._filename = self._file_path_name.rpartition('\\')[2]
        self._folder_path = self._file_path_name.rpartition('\\')[0]

        if self._folder_path == '':
            self._file_path_name = os.path.abspath(self._filename)
            self._folder_path = self._file_path_name.rpartition('\\')[0]

        self._ext = self._file_path_name.rpartition('.')[2]
        if len(self._ext) <= 1:
            self._ext = ''
        self._extless_filename = self._file_path_name.rpartition('.')[0].rpartition('\\')[2]
        if self._ext == '':
            ext = ''
        else:
            ext = f".{self._ext}"
        self._tmp_filename = f"{self._folder_path}\\temp\\tmp--{random_filename()}--{random_filename()}{ext}"
        print("self._ext--->", self._ext)

    @property
    def file_path_name(self):
        return self._file_path_name

    @property
    def folder_path(self):
        return self._folder_path

    @property
    def filename(self):
        return self._filename

    @property
    def ext(self):
        return self._ext

    @property
    def extless_filename(self):
        return self._extless_filename

    @property
    def tmp_filename(self):
        return self._tmp_filename

    @tmp_filename.setter
    def tmp_filename(self, value):
        self._tmp_filename = value

    def __str__(self):
        _strg_ = f".file_path_name --> {self.file_path_name}\n" \
                 f"._folder_path -->{self._folder_path}\n" \
                 f"._filename -->{self._filename}\n" \
                 f"._ext -->{self._ext}\n" \
                 f"._extless_filename-->{self._extless_filename}\n" \
                 f"._tmp_filename-->{self._tmp_filename}\n"
        return _strg_


if __name__ == "__main__":

    old_str = "secure_storage.py d4b578ba300babd8b4ce2afde8aa3b3e"
    new_str = "main.py 6dba0d5c6ab8ee134519b7a119612bb714013fd7"
    if not os.path.exists("log"):
        os.makedirs("log")
    list_dir = os.listdir(LOG_FILES_LOC)
    join = os.path.join
    for fs in list_dir:
        fns = join(LOG_FILES_LOC, fs)
        with open(fns, "r") as fr:
            line = fr.read()

            new_line = line.replace(old_str, new_str)
            print(new_line)
            with open(join("log", fs), "w") as fw:
                fw.write(new_line)
    """    for fs in list_dir:
        fns = join(LOG_FILES_LOC,fs)
        with open(fns, "r") as fr:
            with open(fns, "w") as fw:
                line = fr.read()
                if line.find(old_str) > -1:
                    line.replace(old_str, new_str)
                fw.write(line)"""
