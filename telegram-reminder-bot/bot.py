"""Telegram reminder + currency rate bot (aiogram 3).

Commands:
  /start                 - greeting and help
  /remind 10m Buy milk   - remind me in 10 minutes (units: s, m, h, d)
  /rate USD              - official CBR exchange rate in RUB
"""
import asyncio
import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from utils import extract_rate, humanize, parse_delay

CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"

dp = Dispatcher()

HELP_TEXT = (
    "Hi! I can remind you of things and show currency rates.\n\n"
    "/remind 10m Buy milk - reminder (s, m, h, d)\n"
    "/rate USD - exchange rate in RUB"
)


@dp.message(Command("start", "help"))
async def cmd_start(message: Message) -> None:
    await message.answer(HELP_TEXT)


@dp.message(Command("remind"))
async def cmd_remind(message: Message, command: CommandObject) -> None:
    args = (command.args or "").split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Usage: /remind 10m Buy milk")
        return
    try:
        delay = parse_delay(args[0])
    except ValueError as err:
        await message.answer(f"⚠️ {err}")
        return

    await message.answer(f"✅ Okay, I'll remind you in {humanize(delay)}.")
    await asyncio.sleep(delay)
    await message.answer(f"⏰ Reminder: {args[1]}")


@dp.message(Command("rate"))
async def cmd_rate(message: Message, command: CommandObject) -> None:
    code = (command.args or "USD").strip().upper()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(CBR_URL, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                data = await resp.json(content_type=None)
        value = extract_rate(data, code)
    except KeyError:
        await message.answer(f"Unknown currency: {code}")
    except (aiohttp.ClientError, asyncio.TimeoutError):
        await message.answer("Couldn't reach the exchange rate service, try again later.")
    else:
        await message.answer(f"💱 1 {code} = {value:.2f} ₽")


async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise SystemExit("Set the BOT_TOKEN environment variable (get one from @BotFather).")
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
