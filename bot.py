import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# URL вашего Mini App (после деплоя на BotHost)
MINI_APP_URL = "https://your-app.bothost.ru"

logging.basicConfig(level=logging.INFO)

bot = Bot(token="8927032411:AAG6oxGPxGgs0NvfUxU56FO8_f98FlpmrK8")
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    await message.answer(
        "🎮 **Крестики-нолики против бота!**\n\n"
        "Нажмите кнопку ниже чтобы начать игру.\n"
        "Вы — ❌ (X), бот — ⭕ (O).\n"
        "Минимакс делает бота непобедимым!",
        parse_mode="Markdown",
        reply_markup=types.InlineKeyboardButton(
            text="🎮 Играть",
            web_app={"url": MINI_APP_URL},
        ),
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    await message.answer(
        "🎮 **Крестики-нолики**\n\n"
        "Нажмите кнопку чтобы открыть игру:\n"
        "/new — начать заново",
        parse_mode="Markdown",
        reply_markup=types.InlineKeyboardButton(
            text="🎮 Играть",
            web_app={"url": MINI_APP_URL},
        ),
    )


@dp.message(Command("new"))
async def cmd_new(message: types.Message) -> None:
    await message.answer(
        "🔄 **Новая игра!**\n\n"
        "Нажмите кнопку чтобы открыть Mini App:",
        reply_markup=types.InlineKeyboardButton(
            text="🎮 Играть",
            web_app={"url": MINI_APP_URL},
        ),
    )


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

