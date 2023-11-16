from aiogram import Bot, Dispatcher, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import os

router = Router()
bot = Bot(token=os.environ['TOKEN'], parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
router = Router()