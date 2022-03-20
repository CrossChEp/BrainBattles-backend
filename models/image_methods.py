import base64
import string


def encode_image(image: bytes) -> str:
    return base64.encodebytes(image).hex()


def decode_image(hex_digit: str) -> bytes:
    hex_digit = hex_digit.replace("0x", "")
    if not (all(c in string.hexdigits for c in hex_digit)):
        raise ValueError("String is not a valid hex-string")

    return base64.decodebytes(b''.fromhex(hex_digit))
