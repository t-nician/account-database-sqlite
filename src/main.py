# TODO
# Setup peewee models - DONE
# Setup scrypt & aes lib - DONE
# Setup interface classes for accounts
# Setup vars lib that uses enums & settings.json in workspace/settings.json

import database

print(database.secure.scrypt_hash("password"))


database.handler.create_account("username")

print(database.handler.get_account("username"))