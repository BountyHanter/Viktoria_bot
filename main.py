import asyncio
import logging
import json
import sys

from routers import commands
from settings import settings
from aiogram import Bot, Dispatcher
from bot_commands.bot_commands import set_commands

class StreamToLogger(object):
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level

    def write(self, buffer):
        for line in buffer.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass

class JsonFormatter(logging.Formatter):
    def format(self, record):
        result = super().format(record)
        return json.dumps(result)

# Старт бота
async def start_bot():
    bot = Bot(token=settings.bots.bot_token)
    await set_commands(bot)

    dp = Dispatcher()
    dp.include_router(
        commands.router
    )
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")  # выводим логи в консоль
    logHandler = logging.FileHandler('bot_logs.json')
    formatter = JsonFormatter("%(asctime)s - [%(levelname)s] - %(name)s - "
                              "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    logHandler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)

    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl

    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl

    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем сообщения которые получил бот до запуска
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error("An error occurred: ", exc_info=True)

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start_bot())