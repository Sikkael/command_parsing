from datetime import datetime
import os

new_dict = {0: {
    'name': "",
    'date': datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
    'keyAES': "",
    'keyChaCha': "",
    'original file location': "",
    "file sha256 hash": ""
}}


class MetaData:

    def __init__(self):
        self._file_key = None
        self._name = None
        self._date = None
        self._key_aes = None
        self._key_chacha = None
        self._decrypted_file_location = None
        self._filehash = None
        self._encrypted_file_location = os.path.join("Data\\Encrypted files", f"{self.file_key}.ENCRYPTED")
        self._duplicate_name_id = 0
        self._id = 0

    def dict(self):
        return {
            'name': self._name,
            'date': self._date,
            'keyAES': self._key_aes,
            'keyChaCha': self._key_chacha,
            'decrypted file location': self._decrypted_file_location,
            "file sha256 hash": self._filehash,
            "encrypted_file_location": self._encrypted_file_location,
            "id": self._id
        }

    @property
    def file_key(self):
        return self._file_key

    @file_key.setter
    def file_key(self, value):
        assert isinstance(value, str)
        self._file_key = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = os.path.basename(value)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def key_aes(self):
        return self._key_aes

    @key_aes.setter
    def key_aes(self, value):
        self._key_aes = value

    @property
    def key_chacha(self):
        return self._key_chacha

    @key_chacha.setter
    def key_chacha(self, value):
        self._key_chacha = value

    @property
    def decrypted_file_location(self):
        return self._decrypted_file_location

    @decrypted_file_location.setter
    def decrypted_file_location(self, value):
        self._decrypted_file_location = value

    @property
    def filehash(self):
        return self._filehash

    @filehash.setter
    def filehash(self, value):
        self._filehash = value

    @property
    def encrypted_file_location(self):
        return self._encrypted_file_location

    @encrypted_file_location.setter
    def encrypted_file_location(self, value):
        self._encrypted_file_location = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def is_duplicate(self, other):
        return self.name == other.name and self.filehash == self.filehash

    def as_same_name(self, other):
        return self.name == other.name

    def __str__(self):
        s = f"self.file_key -->{self.file_key}\n" \
            f"self.name -->{self.name}\n" \
            f"self.date -->{self.date}\n" \
            f"self._key_aes {self._key_aes}\n" \
            f"self._key_chacha-->{self._key_chacha}\n" \
            f"self._decrypted_file_location--> {self._decrypted_file_location}\n" \
            f"self._encrypted_file_location--> {self._encrypted_file_location}\n" \
            f"self._filehash-->{self._filehash}\n" \
            f"self._id-->{self._id}\n"
        return s

    @classmethod
    def copy_from_dict(cls, k, meta_dat_dict: dict):
        meta_dat_obj = MetaData()
        meta_dat_obj.file_key = k
        meta_dat_obj.name = meta_dat_dict[k]['name']
        meta_dat_obj.date = meta_dat_dict[k]['date']
        meta_dat_obj.key_aes = meta_dat_dict[k]['keyAES']
        meta_dat_obj.key_chacha = meta_dat_dict[k]['keyChaCha']
        meta_dat_obj.decrypted_file_location = meta_dat_dict[k]['decrypted file location']
        meta_dat_obj.filehash = meta_dat_dict[k]['file sha256 hash']
        meta_dat_obj.encrypted_file_location = meta_dat_dict[k]['encrypted_file_location']
        meta_dat_obj.id = meta_dat_dict[k]['id']
        return meta_dat_obj


def meta_data_filename():
    meta_data_loc = "Data\\meta_data.ENCRYPTED"
    return meta_data_loc


"""" 'name': self._name,
            'date': self._date,
            'keyAES': self._key_aes,
            'keyChaCha': self._key_chacha,
            'decrypted file location': self._decrypted_file_location,
            "file sha256 hash": self._filehash,
            "encrypted_file_location":self._encrypted_file_location,
            "duplicate_name_id":self._id"""
