import json

__settings_dictionary: dict

with open("workspace/settings.json", "r") as file:
    __settings_dictionary = json.loads(file.read())

# Path for the sqlite file
SQLITE_PATH = __settings_dictionary["sqlite_path"]

# Scrypt parameters & options.
SCRYPT_SALT_LENGTH = __settings_dictionary["scrypt"]["salt_length"]
SCRYPT_HASH_LENGTH = __settings_dictionary["scrypt"]["hash_length"]

SCRYPT_PARAM_N = __settings_dictionary["scrypt"]["params"]["N"]
SCRYPT_PARAM_R = __settings_dictionary["scrypt"]["params"]["r"]
SCRYPT_PARAM_P = __settings_dictionary["scrypt"]["params"]["p"]

