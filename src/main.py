# TODO
# Setup peewee models - DONE
# Setup scrypt & aes lib - DONE
# Setup handler class for accounts
# Setup vars lib that uses enums & settings.json in workspace/settings.json - DONE

import database

database.handler.create_account("username", "password")

print(database.handler.get_account("username").scrypt_params)