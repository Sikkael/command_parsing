from typing import List, Any

from meta_data import MetaData
from keystore import Keystore
from random import randint
from datetime import datetime
from file_helper import meta_enc, enc_loc, poubelle
import os
import pathlib
from utils import sha256, create_key
import time
from shutil import copy
from json import loads, dumps
from files_store import *


class MetaDataStorage:
    meta_data_loc = "Data\\meta_data.ENCRYPTED"

    def __init__(self, key=False):
        if not key:
            key = Keystore().key
        self._key = key
        if not os.path.exists(self.meta_data_loc):
            self.init_files()

        self._files_meta_data = self.load_data()
        self.metadata_keys = [fmeta for fmeta in self._files_meta_data]
        self.meta_data = MetaData()

    @property
    def get_files(self):
        return self._files_meta_data

    def load_data(self):
        try:
            file_decryptor = Decryptor(self.meta_data_loc)

            _files_ = loads(file_decryptor.decrypt_file(self._key, self._key))

            _dat_ = {k: _files_[k] for k in _files_ if os.path.exists(_files_[k]["encrypted_file_location"])}

            return _dat_
        except FileNotFoundError:

            raise FileStoreError("Meta data file not found!")

    def add(self, dats):
        if not isinstance(dats, tuple):
            raise AssertionError(f"argument type --> {type(dats)}\n"
                                 f"tuple needed")
        """"string, key_aes.decode('ISO-8859-1'), key_chacha.decode('ISO-8859-1'), \
               self.src_file, self.dest_file, self.get_filehash()"""

        self.meta_data.key_aes = dats[1]
        self.meta_data.key_chacha = dats[2]
        self.meta_data.decrypted_file_location = dats[3]
        self.meta_data.name = os.path.basename(dats[3])
        self.meta_data.filehash = dats[5]
        self.meta_data.date = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')

        self.meta_data.file_key = create_key()
        self.meta_data.encrypted_file_location = os.path.join(enc_loc, f"{self.meta_data.file_key}.ENCRYPTED")

        idl_ist = [self._files_meta_data[dct_key]["id"] for dct_key in self._files_meta_data]

        if len(idl_ist) > 0:

            self.meta_data.id = max(idl_ist) + 1
        else:
            self.meta_data.id = 0

        self._files_meta_data[self.meta_data.file_key] = self.meta_data.dict()
        file_encryptor = Encryptor(dest_file=self.meta_data_loc)
        res = file_encryptor.encrypt_plaintext(str.encode(dumps(self._files_meta_data, ensure_ascii=False)),
                                               self._key, self._key)
        file_encryptor.write(res[0])

    def find_by_id(self, int_id):
        _met_ = [mdk for mdk in self._files_meta_data
                 if self._files_meta_data[mdk]["id"] == int_id]
        if len(_met_) <= 0:
            return False
        obj = self.find(_met_[0])

        return obj

    def find(self, str_ind):
        if str_ind in self._files_meta_data:
            _met_ = {}
            return MetaData.copy_from_dict(str_ind, self._files_meta_data)
        else:
            raise FileStoreError(f"Key--> {str_ind} not found")

    def remove(self, str_ind):
        if str_ind in self._files_meta_data:
            _dct_ = self._files_meta_data
            _dct_.pop(str_ind)
            self._files_meta_data = _dct_
            file_encryptor = Encryptor(self.meta_data_loc)
            res = file_encryptor.encrypt_file(str.encode(dumps(self._files_meta_data, ensure_ascii=False)),
                                              self._key, self._key)
            file_encryptor.dest_file = self.meta_data_loc
            file_encryptor.write(res[0])
        else:
            raise FileStoreError(f"Key--> {str_ind} not found")
        return str_ind not in self._files_meta_data

    def is_unique_key(self, meta_data: MetaData):
        return meta_data.file_key in self._files_meta_data

    def is_duplicate(self, meta_data: MetaData):
        for meta in self._files_meta_data:
            if meta_data.is_duplicate(MetaData.copy_from_dict(meta, self._files_meta_data[meta])):
                return True
        return False

    def list_metadata_key(self):
        k_list = [fmeta for fmeta in self._files_meta_data]
        return k_list

    def list_enc_files(self):

        enc_list = [self._files_meta_data[d]["encrypted_file_location"] for d in self._files_meta_data if
                    os.path.exists(self._files_meta_data[d]["encrypted_file_location"])]
        return enc_list

    def get_meta_data_obj(self, key):
        try:
            dct = self._files_meta_data[key]
            return MetaData.copy_from_dict(key, dct)
        except KeyError:
            raise FileStoreError(f"Key--> {key} not found")

    def init_files(self):
        file_encryptor = Encryptor(dest_file=self.meta_data_loc)
        res = file_encryptor.encrypt_file(b"{}", self._key, self._key)
        file_encryptor.write(res[0])

    def new_encrypted_file(self):
        return self.meta_data.encrypted_file_location

    def new_id(self):
        return self.meta_data.id

    @staticmethod
    def create_meta_data():
        met_dat = MetaData()
        met_dat.file_key = create_key()
        met_dat.encrypted_file_location = os.path.join(enc_loc, f"{met_dat.file_key}.ENCRYPTED")
        return met_dat

    """""    def safeguard(self, _meta_data_object: MetaData):
        if not os.path.exists(poubelle):
            os.makedirs(poubelle)
        h = sha256(
            f"{_meta_data_object.name}{_meta_data_object.file_key}"
            f"{_meta_data_object.filehash}{time.time_ns()}"
            f"{create_key()}")
        new_dirname = os.path.join(poubelle, h)
        os.makedirs(new_dirname)
        print(f"_meta_data_object.encrypted_file_location--> {_meta_data_object.encrypted_file_location}")
        copy(_meta_data_object.encrypted_file_location, new_dirname)
        h1 = sha256(f"{h}{create_key()}")
        meta_backup = os.path.join(new_dirname, f"{h1}.META.ENCRYPTED")
        saveFiles(_meta_data_object.dict(), self._key, meta_backup)"""


if __name__ == "__main__":
    k = Keystore("012").key

    meta_store = MetaDataStorage(k)

    _files = meta_store.get_files
    print(_files)
