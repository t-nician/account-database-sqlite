from database import var

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt

from Crypto.Random import get_random_bytes


def scrypt_hash(
        password: str | bytes,

        hash_length: int | None = var.SCRYPT_HASH_LENGTH,
        hash_amount: int | None = 1,

        salt_length: int | None = var.SCRYPT_SALT_LENGTH,
        salt_override: bytes | None = None,

        N: int | None = var.SCRYPT_PARAM_N,
        r: int | None = var.SCRYPT_PARAM_R,
        p: int | None = var.SCRYPT_PARAM_P
    ) -> tuple[bytes, bytes] | tuple[list[bytes], bytes]:
    """Primary hashing function for passwords.

    Args:
        password (str | bytes): target password to hash.
        hash_length (int | None, optional): byte/char length of hashes. Defaults to var.SCRYPT_HASH_LENGTH.
        hash_amount (int | None, optional): how many hashes are generated. Defaults to 1.
        salt_length (int | None, optional): length of salt. Defaults to var.SCRYPT_SALT_LENGTH.
        salt_override (bytes | None, optional): use premade salt instead of making new one.. Defaults to None.
        N (int | None, optional): CPU resource amount. Defaults to var.SCRYPT_PARAM_N.
        r (int | None, optional): block size. Defaults to var.SCRYPT_PARAM_R.
        p (int | None, optional): parallelization. Defaults to var.SCRYPT_PARAM_P.

    Returns:
        tuple[bytes, bytes] | tuple[list[bytes], bytes]: hash, salt | list[hash], salt
    """
    return scrypt(
        password=password,
        salt=salt_override or get_random_bytes(salt_length),
        key_len=hash_length,
        N=N,
        r=r,
        p=p,
        num_keys=hash_amount
    )


def aes_encrypt(key: bytes | str, data: bytes, nonce_override: bytes | None = None) -> tuple[bytes, bytes]:
    """Encrypt data with aes.

    Args:
        key (bytes | str): 16 bytes for AES128, 32 bytes for AES256
        data (bytes): Target data to encrypt.

    Returns:
        tuple[bytes, bytes]: encrypted data, nonce.
    """
    key = type(key) is str and key.encode() or key

    cipher = AES.new(key=key, mode=AES.MODE_EAX, nonce=nonce_override)

    return cipher.encrypt(data), cipher.nonce


def aes_decrypt(key: bytes | str, nonce: bytes, data: bytes) -> bytes:
    """Decrypt data with aes.

    Args:
        key (bytes | str): Key for decrypting data.
        nonce (bytes): Seed for decrypting data.
        data (bytes): Target data to decrypt.

    Returns:
        bytes: Decrypted data.
    """
    key = type(key) is str and key.encode() or key

    return AES.new(key=key, mode=AES.MODE_EAX, nonce=nonce).decrypt(data)


