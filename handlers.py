from aiogram import types, F
from misc import dp
from aiogram.types import Message
from aiogram.filters import Command
from openai import OpenAI
import os


class chatGPT():

  def __init__(self) -> None:
    self.client = OpenAI(api_key=os.environ['API_KEY'])

  def get_completion(self, prompt, model="gpt-3.5-turbo"):
    chat_compelation = self.client.chat.completions.create(messages=[{
        "role":
        "user",
        "content":
        prompt
    }],
                                                           model=model)
    return chat_compelation.choices[0].message.content


chat_bot = chatGPT()


@dp.message(Command("start"))
async def start_handler(msg: Message):
  await msg.answer("Hello you can ask me question")


@dp.message()
async def message_handler(msg: Message):
  await msg.answer(chat_bot.get_completion(prompt=msg.text))
