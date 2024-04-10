import peewee

from database import var

database_connection = peewee.SqliteDatabase(var.SQLITE_PATH)


class BaseModel(peewee.Model):
    class Meta:
        database = database_connection


class Account(BaseModel):
    username = peewee.TextField(primary_key=True, index=True, unique=True)
    password = peewee.TextField(default="")

    scrypt = peewee.TextField(default="")

    email = peewee.TextField(default="")
    data = peewee.TextField(default="")


# TODO look for better method of handling this. Not sure if this is the best.
__AVAILABLE_MODELS = [Account]

for model in __AVAILABLE_MODELS:
    if not database_connection.table_exists(model):
        database_connection.create_tables([model])
        database_connection.commit()