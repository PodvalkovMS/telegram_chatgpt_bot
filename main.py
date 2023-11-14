import misc
import handlers
import asyncio
import logging
from background import keep_alive


async def main():
  keep_alive()
  await misc.bot.delete_webhook(drop_pending_updates=True)
  await misc.dp.start_polling(
      misc.bot, allowed_updates=misc.dp.resolve_used_update_types())


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  asyncio.run(main())
