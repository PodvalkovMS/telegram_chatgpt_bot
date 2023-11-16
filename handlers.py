from misc import dp, bot
from aiogram.types import Message
from aiogram.filters import Command
from openai import OpenAI
import logging
import os
from pathlib import Path


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
                                                           max_tokens=16,
                                                           n=1,
                                                           model=model)
    return chat_compelation.choices[0].message.content


chat_bot = chatGPT()


@dp.message(Command("start"))
async def start_handler(msg: Message):
  name = msg.chat.first_name if msg.chat.first_name else 'No_name'
  logging.info(f"Chat {name} (ID: {msg.chat.id}) started bot")
  await msg.answer(
      "Hello. I am ChatGPT. Please feel free to ask me any question. And now I even can work with voice messages"
  )


@dp.message()
async def voice_process(msg: Message):
  file_id = msg.voice.file_id
  logging.info(f"Voice message received from {file_id}")
  coorutin_thing = await bot.get_file(file_id)
  logging.info(f"get from bot {coorutin_thing}")
  file_path = coorutin_thing.file_path
  logging.info(f"File path: {file_path}")
  logging.info(f"Voice message file path: {file_path}")
  downloaded_file = await bot.download_file(file_path=file_path)
  file_name = f"{msg.message_id}.mp3"
  logging.info(f"Voice message file name: {file_name}")
  name = msg.chat.first_name if msg.chat.first_name else 'No_name'
  logging.info(f"Chat {name} (ID: {msg.chat.id}) download file {file_name}")
  with open(file_name, 'wb') as new_file:
    logging.info(f"Open file {file_name}")
    new_file.write(downloaded_file.getvalue())
  transcript = chat_bot.client.audio.transcriptions.create(
      model="whisper-1", file=Path(file_name))
  logging.info(f"Transcript: {transcript.text}")
  response = chat_bot.get_completion(transcript.text)
  logging.info(f"Response: {response}")
  response_audio = chat_bot.client.audio.speech.create(model="tts-1",
                                                       voice="alloy",
                                                       input=response)
  logging.info(f"Response audio generation done!")
  response_audio.stream_to_file(file_name)
  return file_name


@dp.message()
async def message_handler(msg: Message):
  if msg.content_type == 'voice':
    response = await voice_process(msg)
    logging.info(f"Response: {response}")
    await msg.answer_voice(open(response, 'rb'))
    os.remove(response)
  elif msg.content_type == 'text':
    await msg.answer(chat_bot.get_completion(prompt=msg.text))

