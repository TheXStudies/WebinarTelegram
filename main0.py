import os

from telethon import TelegramClient


client = TelegramClient(
    'collect_data',
    api_id=int(os.environ['TELEGRAM_API_ID']),
    api_hash=os.environ['TELEGRAM_API_HASH'])

client.start()
for msg in client.iter_messages(
        entity='ru_python_beginners', limit=10):
    print(msg.message)


