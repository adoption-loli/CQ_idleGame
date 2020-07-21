import asyncio
import random
import time
import os
import threading
import json
from . import player as p
from nonebot import IntentCommand, on_command, CommandSession
import nonebot

bot = nonebot.get_bot()


class Enemy:
    def __init__(self):
        self.hp = 0
        self.attack = 0
        self.defense = 0
        self.money_max = 0
        self.money_min = 0
        self.exp_max = 0
        self.exp_min = 0
        self.exp = 0
        self.money = 0

    def random_money_exp(self):
        self.exp = random.randint(self.money_min, self.money_max)
        self.money = random.randint(self.money_min, self.money_max)


class Slime(Enemy):
    def __init__(self):
        super(Slime, self).__init__()
        self.name = "史莱姆"
        self.hp = 100
        self.attack = 12
        self.defense = 10
        self.money_max = 20
        self.money_min = 10
        self.exp_max = 24
        self.exp_min = 28
        self.random_money_exp()


class BigSlime(Enemy):
    def __init__(self):
        super(BigSlime, self).__init__()
        self.name = "大史莱姆"
        self.hp = 570
        self.attack = 65
        self.defense = 40
        self.money_max = 40
        self.money_min = 20
        self.exp_max = 50
        self.exp_min = 36
        self.random_money_exp()


class SoBigSlime(Enemy):
    def __init__(self):
        super(SoBigSlime, self).__init__()
        self.name = "巨大史莱姆"
        self.hp = 700
        self.attack = 350
        self.defense = 300
        self.money_max = 80
        self.money_min = 40
        self.exp_max = 125
        self.exp_min = 100
        self.random_money_exp()


class WzcDeTan(Enemy):
    def __init__(self):
        super(WzcDeTan, self).__init__()
        self.name = "文佬的痰"
        self.hp = 2000
        self.attack = 1000
        self.defense = 1600
        self.money_max = 200
        self.money_min = 150
        self.exp_max = 150
        self.exp_min = 125
        self.random_money_exp()


class JgDeSfq(Enemy):
    def __init__(self):
        super(JgDeSfq, self).__init__()
        self.name = "川建国の手风琴"
        self.hp = 5000
        self.attack = 2000
        self.defense = 4300
        self.money_max = 490
        self.money_min = 480
        self.exp_max = 200
        self.exp_min = 150
        self.random_money_exp()


@nonebot.scheduler.scheduled_job('interval', seconds=10)
async def main():
    BASEDIR_JSON = os.path.join(os.path.dirname(__file__), 'json')
    FILE = os.path.join(BASEDIR_JSON, '玩家信息.json')
    with open(FILE, 'r', encoding='utf-8') as player:
        player_list = json.load(player)
    fightlist = []
    for player in player_list:
        if player_list[player].get("place", '未出征') in ['天台', '魔都', '加载之地', '小汉堡仓库']:
            fightlist.append(player)
    # print(f'{len(fightlist)}人进行了一场战斗')
    for qq_id in fightlist:
        player = p.Player(int(qq_id))
        enemy = []
        if player["place"] == '天台':
            enemy = tiantai()
        if player["place"] == '魔都':
            enemy = modu()
        if player["place"] == '加载之地':
            enemy = jiazaizhidi()
        if player["place"] == '小汉堡仓库':
            enemy = xiaohanbaocangku()
        p_hp = player["hp"]
        while True:
            if p_hp <= 0 or len(enemy) <= 0:
                break
            p_damage_e = player["real_attack"] - enemy[-1].defense + random.randint(10, 20)
            if p_damage_e <= 0:
                p_damage_e = random.randint(10, 20)
            e_hp = enemy[-1].hp
            e_hp -= p_damage_e
            enemy[-1].hp = e_hp
            if player.attr["passive"] == "吟唱略过":
                e_hp = enemy[-1].hp
                e_hp -= p_damage_e
                enemy[-1].hp = e_hp

            if e_hp <= 0:
                player.attr["money"] += enemy[-1].money
                player.attr["exp"] += enemy[-1].exp
                player.attr[enemy[-1].name] += 1
                enemy.pop()
                continue


            for cell in enemy:
                e_damage_p = cell.attack - player["real_defense"] + random.randint(10, 20)
                if e_damage_p <= 0:
                    e_damage_p = random.randint(10, 20)
                if player.attr["passive"] == "矢量操作":
                    enemy[enemy.index(cell)].hp -= e_damage_p*2
                    e_damage_p /= 2
                p_hp -= e_damage_p
        while player["exp"] >= player["upexp"]:
            player.attr["exp"] -= player["upexp"]
            player.attr["level"] += 1
            aim_level = player["level"] + 1
            player.attr["upexp"] = (20 + aim_level * 20 + aim_level // 10 * 10) * aim_level
            if player["type"] == "魔法使":
                player.attr["hp"] += 10 * (aim_level // 10 + 1)
                player.attr["attack"] += 15 * (aim_level // 10 + 1)
                player.attr["defense"] += 3 * (aim_level // 10 + 1)
            elif player["type"] == "科学使":
                player.attr["hp"] += 10 * (aim_level // 10 + 1)
                player.attr["attack"] += 7 * (aim_level // 10 + 1)
                player.attr["defense"] += 7 * (aim_level // 10 + 1)
        if p_hp <= 0:
            await bot.send_group_msg(group_id=player["last_group"],
                                     message=f'[CQ:at,qq={qq_id}] 已阵亡，成功回家')
            player.attr["place"] = "未出征"
        up_player = player.attr
        up_player["id"] = qq_id
        update_user(up_player)


@nonebot.scheduler.scheduled_job('interval', seconds=60)
async def time_lost():
    BASEDIR_JSON = os.path.join(os.path.dirname(__file__), 'json')
    FILE = os.path.join(BASEDIR_JSON, '玩家信息.json')
    with open(FILE, 'r', encoding='utf-8') as player:
        player_list = json.load(player)
    fightlist = []
    for player in player_list:
        if player_list[player].get("place", '未出征') in ['天台', '魔都', '加载之地', '小汉堡仓库']:
            fightlist.append(player)
    print(fightlist)
    for qq_id in fightlist:
        player = p.Player(int(qq_id))
        player.attr["time"] -= 1
        if player.attr["time"] <= 0:
            player.attr["place"] = "未出征"
            await bot.send_group_msg(group_id=player["last_group"],
                                     message=f'[CQ:at,qq={qq_id}] 时间耗尽，成功回家')
            up_player = player.attr
            up_player["id"] = qq_id
            update_user(up_player)


def tiantai():
    cnt = random.randint(1, 2)
    enemy = []
    for cell in range(cnt):
        t = random.randint(1, 100)
        if t <= 100:
            enemy.append(Slime())
    return enemy


def modu():
    cnt = random.randint(4, 8)
    enemy = []
    for cell in range(cnt):
        t = random.randint(1, 100)
        if t <= 50:
            enemy.append(Slime())
        elif t <= 80:
            enemy.append(BigSlime())
        else:
            enemy.append(SoBigSlime())
    return enemy


def jiazaizhidi():
    cnt = random.randint(10, 12)
    enemy = []
    for cell in range(cnt):
        t = random.randint(1, 100)
        if t <= 50:
            enemy.append(SoBigSlime())
        elif t <= 80:
            enemy.append(WzcDeTan())
        else:
            enemy.append(JgDeSfq())
    return enemy


def xiaohanbaocangku():
    cnt = random.randint(12, 20)
    enemy = []
    for cell in range(cnt):
        t = random.randint(1, 100)
        if t <= 60:
            enemy.append(WzcDeTan())
        else:
            enemy.append(JgDeSfq())
    return enemy


def update_user(user):
    '''
    更新整个玩家，所有数值都更新
    user必需带有id键，id键将在此处被删除
    :param user:
    :return:
    '''
    BASEDIR_JSON = os.path.join(os.path.dirname(__file__), 'json')
    qq_id = user['id']
    del user['id']
    with open(os.path.join(BASEDIR_JSON, '玩家信息.json'), 'r', encoding='utf-8') as player:
        users = json.load(player)
        users[str(qq_id)] = user
    with open(os.path.join(BASEDIR_JSON, '玩家信息.json'), 'w', encoding='utf-8') as player:
        json.dump(users, player, ensure_ascii=False, indent=4)
