from misc import dp, bot, router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F
from aiogram.types.input_file import InputFile
from openai import OpenAI
import logging
import os
from pathlib import Path
from gtts import gTTS
from langdetect import detect




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
                                                           model=model,
                                                           timeout=30)

    return chat_compelation.choices[0].message.content


chat_bot = chatGPT()


@dp.message(Command("start"))
async def start_handler(msg: Message):
  name = msg.chat.first_name if msg.chat.first_name else 'No_name'
  logging.info(f"Chat {name} (ID: {msg.chat.id}) started bot")
  await msg.answer(
      "Hello. I am ChatGPT. Please feel free to ask me any question. And now I even can work with voice messages"
  )


@router.message(F.content_type.in_(['voice']))
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
  response = "I don not know" if response is None else response
  detector = detect(response)
  logging.info(f"Code of languge responce {detector}")
  tts = gTTS(text=response, lang=detector)
  tts.save(file_name)
  #AudioSegment.from_mp3(file_name).export('result.ogg', format='ogg')
  logging.info(f"Response audio generation in {file_name} done!")
  await bot.send_audio(msg.chat.id, file_name)
  os.remove(file_name)
  #os.remove('result.ogg')


@router.message(F.content_type.in_(['text']))
async def message_handler(msg: Message):
  logging.info("Recived Text Message")
  await msg.answer(chat_bot.get_completion(prompt=msg.text))
