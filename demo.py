import nonebot
import config
from os import path

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(path.join(path.dirname(__file__), 'plugins'), 'plugins')
    nonebot.run()
    # nonebot_thread = threading.Thread(target=nonebot.run, name="nonebot")
    # fight_thread = threading.Thread(target=fight.main, name="fight")
    # nonebot_thread.start()
    # fight_thread.start()
    # nonebot.run(host='127.0.0.1', port=8080)
