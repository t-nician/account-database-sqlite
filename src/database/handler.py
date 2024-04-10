from database import var, model


class AccountHandler():
    def __init__(self, account: model.Account):
        self.account_model = account

    
    


def get_account(username: str) -> AccountHandler | None:
    pass


def create_account(username: str) -> AccountHandler | None:
    new_account = model.Account.create(
        username=username
    )

    # TODO handle scrypt hashing & first pass of aes encryption.

    return AccountHandler(new_account)