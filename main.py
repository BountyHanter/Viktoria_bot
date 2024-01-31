import asyncio
import logging

from routers import commands
from settings import settings
from aiogram import Bot, Dispatcher


# Старт бота
async def start_bot():
    bot = Bot(token=settings.bots.bot_token)

    dp = Dispatcher()
    dp.include_router(
        commands.router
    )
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s") # выводим логи в консоль

    await bot.delete_webhook(drop_pending_updates=True) # Удаляем сообщения которые получил бот до запуска
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start_bot())
