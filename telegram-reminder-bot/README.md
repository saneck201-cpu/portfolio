# Telegram Reminder & Currency Bot

A small Telegram bot built with Python and [aiogram 3](https://docs.aiogram.dev/).

## Features
- `/remind 10m Buy milk` - sends you a reminder after the given time (`s`, `m`, `h`, `d`, up to 7 days)
- `/rate USD` - official exchange rate in rubles from the Central Bank of Russia
- Input validation and friendly error messages
- Helper logic is separated into `utils.py` and covered by unit tests

## Run it
1. Create a bot with [@BotFather](https://t.me/BotFather) and copy the token.
2. Install and start:
   ```bash
   pip install -r requirements.txt
   export BOT_TOKEN="your-token"     # Windows PowerShell: $env:BOT_TOKEN="your-token"
   python bot.py
   ```

## Tests
```bash
python -m unittest -v
```

## Notes
Reminders are kept in memory, so they are lost if the bot restarts. For production use they can be stored in SQLite and restored on startup.
