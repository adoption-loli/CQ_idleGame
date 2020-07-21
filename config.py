from nonebot.default_config import *

# 配置一个超级 QQ 用户，我们可以为这个超级用户配置一些特殊的操作
SUPERUSERS = {}
# 配置命令起始字符，我们增加了空字符串，所以不需要任何起始字符也能调用命令；
COMMAND_START = {'', '/', '!', '／', '！'}  #
HOST = '0.0.0.0'
PORT = 9983
API_ROOT = 'http://120.78.74.113:5700'  # 这里 IP 和端口应与 CQHTTP 配置中的 `host` 和 `port` 对应