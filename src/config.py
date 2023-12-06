"""Development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# # Secret key for encrypting cookies
# SECRET_KEY = b'>\xbf\x92\xf8\xd3\x8f\xcd\xce\x99h' \
#              b'+\xf7D\x1c\x91!Qs$\xe8\xcc\xbc9s'
# SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
SRC_ROOT = pathlib.Path(__file__).resolve().parent
SQL_ROOT = pathlib.Path(__file__).resolve().parent
UPLOAD_FOLDER = pathlib.Path('/var/www/uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# # Database file is var/input.db
DATABASE_FILENAME = SRC_ROOT/'var'/'chat.db'