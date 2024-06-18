from config_data import config
from aiogram import Bot, Dispatcher
import asyncio


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run((main()))
