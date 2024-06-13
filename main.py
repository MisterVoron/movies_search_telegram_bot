from config_data import config
from keyboards.main_menu import set_main_menu
from aiogram import Bot, Dispatcher
import asyncio


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run((main()))
