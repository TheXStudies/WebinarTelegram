import os

from telethon import TelegramClient


def collect_tg_messages(channel_name, msg_count=40):
    client = TelegramClient(
        'collect_data',
        api_id=int(os.environ['TELEGRAM_API_ID']),
        api_hash=os.environ['TELEGRAM_API_HASH'])

    client.start()
    for msg in client.iter_messages(entity=channel_name, limit=msg_count):
        yield {
            'id': msg.id,
            'date': msg.date,
            'out': msg.out,
            'mentioned': msg.mentioned,
            'media_unread': msg.media_unread,
            'silent': msg.silent,
            'post': msg.post,
            'reply_to_msg_id': msg.reply_to_msg_id,
            'message': msg.message,
            'via_bot_id': msg.via_bot_id,
            'author': msg.from_id,
        }


