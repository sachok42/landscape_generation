import sqlite3
from config import DB_NAME


def db_init(db_name=DB_NAME):
	conn = sqlite3.connect(db_name)
	