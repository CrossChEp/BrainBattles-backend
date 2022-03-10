""" Module for configs
    SECRET_KEY: str
        secret key for authentication
    ALGORITHM: str
        algorithm for creating jwt token
    ACCESS_TOKEN_EXPIRE_MINUTES: int
        minutes for token expiration
    ranks: dict
        all ranks
"""

from configs.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, ranks,\
    redis
