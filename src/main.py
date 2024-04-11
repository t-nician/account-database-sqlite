# TODO
# Setup peewee models - DONE
# Setup scrypt & aes lib - DONE
# Setup handler class for accounts
# Setup vars lib that uses enums & settings.json in workspace/settings.json - DONE

import database

if database.handler.get_account("username") is None:
    database.handler.create_account("username", "password")

account = database.handler.get_account("username")

print(account.get_and_decrypt_data("password"))