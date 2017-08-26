"""

"""
import os


# You need to replace the next values with the appropriate values for your configuration
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
PORT = 5000
HOST = "127.0.0.1"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(
    DB_USER="postgres", DB_PASS="a", DB_ADDR="127.0.0.1", DB_NAME="db_repository")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
TESTING = True
# Disable CSRF protection in the testing configuration
WTF_CSRF_ENABLED = False
