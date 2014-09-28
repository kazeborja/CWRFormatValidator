__author__ = 'Borja'
from api import app

if __name__ == '__main__':
    app.debug = True
    app.run(
        host="0.0.0.0",
        port=int("5002"),
    )
