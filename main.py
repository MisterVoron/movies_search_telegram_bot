from config_data import config
from aiogram import Bot, Dispatcher
from handlers import user_handlers
import asyncio


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user_handlers.router)

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run((main()))
