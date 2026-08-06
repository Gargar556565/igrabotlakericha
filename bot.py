import asyncio
import logging
from typing import Any

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from game import Cell, TicTacToe

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
bot = Bot(token="")
router = Router()
games: dict[int, TicTacToe] = {}  # chat_id -> active game


@router.message(Command(["start", "help"]))
async def cmd_start(message: types.Message) -> None:
    await message.answer(
        "Привет! Я бот для игры в крестики-нолики.\n\n"
        "**Как играть:**\n"
        "1. Нажми /new чтобы начать игру\n"
        "2. Кладём крестик (X) и нолик (O) по очереди\n"
        "3. Собираем три в ряд чтобы победить!\n\n"
        "Нажимай на ячейки внизу чтобы сделать ход.",
        parse_mode="Markdown",
    )


@router.message(Command("new"))
async def cmd_new(message: types.Message) -> None:
    games[message.chat.id] = TicTacToe()
    await _render(message, preview=False)


async def _render(
    message: types.Message,
    *,
    preview: bool = True,
) -> None:
    chat_id = message.chat.id
    if chat_id not in games:
        if preview:
            return  # nothing to show yet
        await message.answer("Новая игра! Напиши /new чтобы начать.")
        return

    game = games[chat_id]
    board_str = game.display_board()
    status = game.status

    kb = [[InlineKeyboardButton(cell.name, callback_data=f"m:{i}")] for i in range(9)]
    await message.answer(
        f"{board_str}\n\n{status}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb),
    )


@router.callback_query(F.data.str.startswith("m:"))
async def cb_move(callback: types.CallbackQuery) -> None:
    chat_id = callback.message.chat.id
    if chat_id not in games:
        await callback.answer("Сначала напиши /new!", show_alert=True)
        return

    index = int(callback.data.split(":")[1])
    game = games[chat_id]
    ok = game.make_move(index)

    if not ok:
        await callback.answer("Эта ячейка занята или игра окончена.", show_alert=True)
        return

    await _render(callback.message, preview=False)
    await callback.answer()


async def main() -> None:
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
