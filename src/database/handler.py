import json

from database import var, model, secure


class AccountHandler():
    def __init__(self, account: model.Account):
        self.account_model = account
        self.scrypt_params = json.loads(self.account_model.scrypt)


def get_account(username: str) -> AccountHandler | None:
    """_summary_

    Args:
        username (str): _description_

    Returns:
        AccountHandler | None: _description_
    """
    account_model = model.Account.get(
        model.Account.username == username
    )

    if account_model is not None:
        return AccountHandler(account_model)


def create_account(username: str, password: str, email: str | None = None) -> AccountHandler | None:
    """_summary_

    Args:
        username (str): _description_
        password (str): _description_
        email (str | None, optional): _description_. Defaults to None.

    Returns:
        AccountHandler | None: _description_
    """
    hashes, salt = secure.scrypt_hash(
        password,
        hash_amount=2
    )

    authorization_password, encryption_password = hashes[0], hashes[1]

    encrypted_data, nonce = secure.aes_encrypt(encryption_password, "{}")

    new_account = model.Account.create(
        username=username,
        password=authorization_password.hex(),

        email=email or "",
        
        scrypt=json.dumps({
            "salt": salt.hex(),
            "N": var.SCRYPT_PARAM_N,
            "r": var.SCRYPT_PARAM_R,
            "p": var.SCRYPT_PARAM_P
        }),

        data=json.dumps({
            "nonce": nonce.hex(),
            "data": encrypted_data.hex()
        })
    )

    model.Account.save(new_account)

    # TODO handle scrypt hashing & first pass of aes encryption.

    return AccountHandler(new_account)