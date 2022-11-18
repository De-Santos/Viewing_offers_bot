"""HERE YOU CAN CHANGE VARIABLES AND CUSTOMIZE BOT"""
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

"""__WARNING____WARNING____WARNING____WARNING____WARNING____WARNING____WARNING____WARNING____WARNING____WARNING__"""
"""---------------------------------BEFORE CUSTOMIZE PLEASE READ README.txt FILE---------------------------------"""
"""__WARNING____WARNING____WARNING____WARNING____WARNING____WARNING____WARNING____WARNING____WARNING____WARNING__"""

load_dotenv()
storage = MemoryStorage()
bot = Bot(token=os.getenv("API_KEY"))
dp = Dispatcher(bot, storage=storage)


# """FOR BOT CUSTOMIZE"""
class BotSet:
    # """FROM USERS"""
    USER_CHANCES: int = 3  # Please write here how much chance can have user
    ADMIN: id = [728740521, 1170698301]  # Here write telegram id admin(s)
    HELP_AND_START_TEXT: str = """Hello"""  # This message bot send Users , command - /help, /start


# """FOR DATA BASE"""
class DataBaseSet:
    """::::::::::::PART ABOUT DATABASE CONNECTION::::::::::::"""

    HOST: str = "localhost"
    PORT: int = 5432
    DATABASE: str = "test_db"
    USER: str = "postgres"
    PASSWORD: str = "password"

    """:::::::::::::::::PART ABOUT USER TABEL:::::::::::::::::"""

    """user tabel name"""
    USER_TABLE: str = "users"  # default "users"

    """-------------------USER TABEL FIELDS-------------------"""

    """automatic id name"""
    AUTO_ID_COL: str = "id"  # default "id"

    """user id column name"""
    USER_ID_COL: str = "user_id"  # default "user_id"

    """user chances column name"""
    CHANCES_COL: str = "chance"  # default "chances"

    """user first name column"""
    FIRST_NAME_COL: str = "first_name"  # default "first_name"

    """:::::::::::::::PART ABOUT MESSAGE TABEL:::::::::::::::"""

    """name of message table"""
    MESSAGE_TABLE: str = "messages"  # default "messages"

    """-----------------MESSAGE TABLE FIELDS-----------------"""

    """automatic id name"""
    MESSAGE_AUTO_ID_COL: str = "id"  # default "id"
    """user_id column name"""
    MESSAGE_USER_ID_COL: str = "user_id"  # default "user_id"

    """message column name"""
    MESSAGE_COL: str = "message"  # default "message"

    """column name for bot internals"""
    MESSAGE_SEEN_COL: str = "seen"  # default "seen"
