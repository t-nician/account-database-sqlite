import json

from database import var, model, secure


class AccountHandler():
    def __init__(self, account: model.Account):
        self.account_model = account
        self.scrypt_params = json.loads(self.account_model.scrypt)
        self.encrypted_data = json.loads(self.account_model.data)


    def get_and_decrypt_data(self, password: str) -> bytes:
        hashes, _ = secure.scrypt_hash(
            password,
            hash_length=var.SCRYPT_HASH_LENGTH,
            hash_amount=2,
            salt_override=bytes.fromhex(self.scrypt_params["salt"]),
            N=self.scrypt_params["N"],
            r=self.scrypt_params["r"],
            p=self.scrypt_params["p"]
        )

        authorization_key, encryption_key = hashes[0], hashes[1]

        if bytes.fromhex(self.account_model.password) != authorization_key:
            raise Exception("Password does not match the accounts!")
        
        encrypted_data = bytes.fromhex(self.encrypted_data["data"])
        aes_nonce = bytes.fromhex(self.encrypted_data["nonce"])

        return secure.aes_decrypt(encryption_key, aes_nonce, encrypted_data)




def get_account(username: str) -> AccountHandler | None:
    """_summary_

    Args:
        username (str): _description_

    Returns:
        AccountHandler | None: _description_
    """

    account_model: model.Account | None = None

    try:
        account_model = model.Account.get(
            model.Account.username == username
        )
    except Exception:
        pass

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
    if get_account(username) is not None:
        raise Exception("Account already exists!")

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