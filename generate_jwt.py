import logging
import time

import jwt

logging.basicConfig(level=logging.INFO)
APP_IDENTIFIER = 80570


def generate_jwt():
    logging.info("Generating new jwt token..")
    with open('./testrayy.2020-09-13.private-key.pem', 'r') as f:
        PRIVATE_KEY = f.read()
    payload = {"iat": int(time.time()),
               "exp": int(time.time()) + (10 * 60),
               "iss": APP_IDENTIFIER}

    return jwt.encode(payload, PRIVATE_KEY, algorithm='RS256').decode()
