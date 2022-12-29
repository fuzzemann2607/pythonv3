import os

import aiomysql
from aiomysql import Pool

async def get_pool(autocommit: bool = True) -> Pool:
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_NAME = os.getenv('DB_NAME')

    HOST, PORT = DB_HOST.split(":")
    return await aiomysql.create_pool(
        host=HOST,
        port=int(PORT),
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
        autocommit=autocommit
    )