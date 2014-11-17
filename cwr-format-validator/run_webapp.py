import os
from webapp import app

__author__ = 'Borja'

if __name__ == '__main__':
    app.debug = True
    app.secret_key = os.urandom(24)
    app.run(
        host="0.0.0.0",
        port=int("5001")
    )
