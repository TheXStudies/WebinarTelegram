import yaml

from collector import collect_tg_messages

CHANNEL_NAME = 'ru_python_beginners'


if __name__ == '__main__':
    with open(f"{CHANNEL_NAME}.yml", 'w') as f:
        yaml.safe_dump_all(collect_tg_messages(CHANNEL_NAME, msg_count=10000), f)
