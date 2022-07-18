from contextlib import closing

import requests
from websocket import create_connection


def add_user():
    response = requests.post(
        'http://127.0.0.1:8000/api/token',
        data={
            "username": "3",
            "password": "3"
        }
    )
    print(response.text)

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6M30.cMaWbyBFsaUe8JW_9KI891pRx0KCApXsH0mEjSQjbFI


def create_socket_connection():
    with closing(create_connection('ws://127.0.0.1:8000/api/websocket_game/hello/1', headers={
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6M30'
                         '.cMaWbyBFsaUe8JW_9KI891pRx0KCApXsH0mEjSQjbFI'
    })) as conn:
        conn.send('hello!')


if __name__ == '__main__':
    print(create_socket_connection())
