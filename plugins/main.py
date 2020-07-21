#!/usr/bin/env python
# encoding: utf-8
import random

from nonebot import on_command, CommandSession, permission, on_natural_language, NLPSession, IntentCommand, _bot
from aiocqhttp.event import Event
import os
import json
from . import player as p
import nonebot

BASEDIR_JSON = os.path.join(os.path.dirname(__file__), 'json')
for filename in ['商店.json', '玩家信息.json', '注册信息.json', '签到信息.json']:
    aim = os.path.join(BASEDIR_JSON, filename)
    # print(aim)
    if not os.path.exists(aim):
        f = open(aim, 'w', encoding='utf-8')
        json.dump({}, f, ensure_ascii=False, indent=4)
        f.close()
        print('创建', aim)


@on_command('菜单', aliases=('出来', '打开菜单', ''), permission=permission.GROUP)
async def menu(session: CommandSession):
    # last_say_at(session)
    msg = '''
┌─菜单
│ 签订契约   商店
│ 契约状态   出征'''
    await session.send(at_sender=True, message=msg)


@on_command('出征', permission=permission.GROUP)
async def menu(session: CommandSession):
    # last_say_at(session)
    msg = '''
┌─菜单
│ 天台(0~20)  
│ 魔都(25~40) 
│ 加载之地(45~60)
│ 小汉堡仓库(65~100)'''
    await session.send(at_sender=True, message=msg)


@on_command('商店', permission=permission.GROUP)
async def shop(session: CommandSession):
    # last_say_at(session)
    msg = '''
┌─商店
│ 武器   防具
│ 道具   被动'''
    await session.send(at_sender=True, message=msg)


@on_command('契约状态', permission=permission.GROUP)
async def state(session: CommandSession):
    # last_say_at(session)
    qq_id = session.ctx['user_id']
    msg = '''
┌───契约状态'''
    try:
        user = p.Player(qq_id)
    except KeyError as e:
        await session.send(at_sender=True, message='先签订契约吧')
        return
    msg += '''
│契约类型：{type}
│生命：{hp}
│攻击：{attack}  防御:{defense}
│挂机时间：{time}  出征：{place}
│防具：{armor}  武器：{weapon}
│被动：{passive}  金币：{money}
│等级:{level}  经验：{exp}/{upexp}
│战绩：
│史莱姆*{史莱姆} 大史莱姆*{大史莱姆}
│巨大史莱姆*{巨大史莱姆} 文佬的痰*{文佬的痰}
│川建国の手风琴*{川建国の手风琴}'''.format(
        type=user['type'],
        hp=user['hp'],
        attack=user['real_attack'], defense=user['real_defense'],
        time=user['time'], place=user['place'],
        armor=user['armor'], weapon=user['weapon'],
        passive=user['passive'], money=user['money'],
        level=user['level'], exp=user['exp'], upexp=user['upexp'],
        史莱姆=user['史莱姆'], 大史莱姆=user['大史莱姆'],
        巨大史莱姆=user['巨大史莱姆'], 文佬的痰=user['文佬的痰'],
        川建国の手风琴=user['川建国の手风琴'])

    await session.send(at_sender=True, message=msg)


@on_command('武器', aliases=('防具', '道具', '被动'), permission=permission.GROUP)
async def item_query(session: CommandSession):
    # last_say_at(session)
    cmd = str(session.ctx['message']).strip()
    msg = '''
─{}'''.format(cmd)
    with open(os.path.join(BASEDIR_JSON, '商店.json'), 'r', encoding='utf-8') as shop:
        itemlist = json.load(shop)[cmd]
    for cell in itemlist:
        msg += '\n*{}'.format(cell)
        with open(os.path.join(BASEDIR_JSON, '商店.json'), 'r', encoding='utf-8') as shop:
            itemattr = json.load(shop)[cell]["介绍"]
            for attr in itemattr:
                msg += '    {}'.format(itemattr[attr])
                if attr == '价格':
                    msg += '円'
        msg += '''回复 购买 物品#物品数量 来购买物品'''
    await session.send(at_sender=True, message=msg)


@on_command('天台', aliases=('魔都', '加载之地', '小汉堡仓库'), permission=permission.GROUP)
async def item_query(session: CommandSession):
    # last_say_at(session)
    cmd = str(session.ctx['message']).strip()
    qq_id = session.ctx['user_id']
    player = p.Player(qq_id)
    if (player.attr["type"] not in ['未签订', '签订中']) and (player.attr["place"] == '未出征'):
        player.attr["place"] = cmd
        up_player = player.attr
        up_player["id"] = qq_id
        update_user(up_player)
        msg = '''成功出征，回复 回家 可取消出征'''
    else:
        msg = '''正在出征状态中，不能重复出征，回复 回家 可取消出征'''
    await session.send(at_sender=True, message=msg)


@on_command('回家', aliases=('回来'), permission=permission.GROUP)
async def item_query(session: CommandSession):
    # last_say_at(session)
    cmd = str(session.ctx['message']).strip()
    qq_id = session.ctx['user_id']
    player = p.Player(qq_id)
    if (player.attr["type"] not in ['未签订', '签订中']) and (player.attr["place"] != '未出征'):
        player.attr["place"] = "未出征"
        up_player = player.attr
        up_player["id"] = qq_id
        update_user(up_player)
        msg = '''回家了(*^▽^*)'''
    else:
        msg = '''有号吗你?'''
    await session.send(at_sender=True, message=msg)


@on_command('签订契约', aliases=('契约签订', '签订'), permission=permission.GROUP)
async def fallen(session: CommandSession):
    # last_say_at(session)
    users = {}
    qq_id = session.ctx['user_id']
    group = session.ctx['group_id']
    with open(os.path.join(BASEDIR_JSON, '玩家信息.json'), 'r', encoding='utf-8') as player:
        users = json.load(player)
    user = {
        # 没有用户则是无用户，有用户则是用户字典
        'info': users.get(str(qq_id), '无用户')
    }
    if user['info'] == '无用户':
        new_player = {
            'id': qq_id,
            'last_group': group,
            'type': '签订中',
        }
        update_user(new_player)
        msg = '''
┌─契约类型
│ 科学使
│ 魔法使
│ 富二代'''
        await session.send(at_sender=True, message=msg)


@on_command('签到', permission=permission.GROUP)
async def type_choose(session: CommandSession):
    qq_id = session.ctx['user_id']
    with open(os.path.join(BASEDIR_JSON, '签到信息.json'), 'r', encoding='utf-8') as player:
        player_list = dict(json.load(player))
    if len(player_list.get("list", [])) <= 0:
        player_list["list"] = []
    if qq_id in player_list["list"]:
        await session.send(at_sender=True, message="签过到了，爬。签到状态每天早上六点刷新。")
        return
    else:
        player_list["list"].append(qq_id)
        randtime = random.randint(10, 15)
        player = p.Player(qq_id)
        player.attr["time"] += randtime
        up_player = player.attr
        up_player["id"] = qq_id
        update_user(up_player)
        with open(os.path.join(BASEDIR_JSON, '签到信息.json'), 'w', encoding='utf-8') as player:
            json.dump(player_list, player)
        await session.send(at_sender=True, message=f"签到成功，获得挂机时间{randtime}分钟")


@nonebot.scheduler.scheduled_job('cron', hour='6')
async def day_after():
    player_list = {
        'list': []
    }
    with open(os.path.join(BASEDIR_JSON, '签到信息.json'), 'w', encoding='utf-8') as player:
        json.dump(player_list, player)


@on_command('魔法使', aliases=('科学使', '富二代'), permission=permission.GROUP)
async def type_choose(session: CommandSession):
    # last_say_at(session)
    qq_id = session.ctx['user_id']
    cmd = str(session.ctx['message']).strip()
    with open(os.path.join(BASEDIR_JSON, '玩家信息.json'), 'r', encoding='utf-8') as player:
        users = json.load(player)
    if users[str(qq_id)]["type"] != '签订中':
        return
    if cmd == '魔法使':
        new_player = p.Player(qq_id)
        new_player.attr["type"] = '魔法使'
        new_player.attr["hp"] = 200
        new_player.attr["attack"] = 25
        new_player.attr["defense"] = 5
        new_player.attr["time"] = 30
        new_player.attr["level"] = 0
        new_player.attr["exp"] = 0
        new_player.attr["upexp"] = 40
        add_player = new_player.attr
        add_player["id"] = qq_id
        update_user(add_player)
        await session.send(at_sender=True, message='签订成功，打开菜单履行契约吧')
    elif cmd == '科学使':
        new_player = p.Player(qq_id)
        new_player.attr["type"] = '科学使'
        new_player.attr["hp"] = 200
        new_player.attr["attack"] = 15
        new_player.attr["defense"] = 15
        new_player.attr["time"] = 30
        new_player.attr["level"] = 0
        new_player.attr["exp"] = 0
        new_player.attr["upexp"] = 40
        add_player = new_player.attr
        add_player["id"] = qq_id
        update_user(add_player)
        await session.send(at_sender=True, message='签订成功，打开菜单履行契约吧')
    else:
        await session.send(at_sender=True, message='请认清现实后再次签订契约')


def update_user(user):
    '''
    更新整个玩家，所有数值都更新
    user必需带有id键，id键将在此处被删除
    :param user:
    :return:
    '''
    qq_id = user['id']
    del user['id']
    with open(os.path.join(BASEDIR_JSON, '玩家信息.json'), 'r', encoding='utf-8') as player:
        users = json.load(player)
        users[str(qq_id)] = user
    with open(os.path.join(BASEDIR_JSON, '玩家信息.json'), 'w', encoding='utf-8') as player:
        json.dump(users, player, ensure_ascii=False, indent=4)


@_bot.on_message('group')
async def last_say_any_at(event: Event):
    # print(event)
    group = event['group_id']
    qq_id = event['sender']['user_id']
    try:
        with open(os.path.join(BASEDIR_JSON, '玩家信息.json'), 'r', encoding='utf-8') as player:
            users = json.load(player)
        users[str(qq_id)]["last_group"] = group
        with open(os.path.join(BASEDIR_JSON, '玩家信息.json'), 'w', encoding='utf-8') as player:
            json.dump(users, player, ensure_ascii=False, indent=4)
    except KeyError as e:
        print(e)


@on_natural_language(keywords={'购买'})
async def buy(session: NLPSession):
    '''
    没注册账号的根本就没钱，买不了！！！！
    '''
    cmd = str(session.ctx['message']).replace('购买', '')
    cmd = cmd.strip()
    cmd = cmd.split('#')
    if len(cmd) < 2:
        cmd.append('1')
    item, num = cmd
    try:
        qq_id = session.ctx['user_id']
        num = int(num)
        print(item, num)
        with open(os.path.join(BASEDIR_JSON, '商店.json'), 'r', encoding='utf-8') as shop:
            iteminfo = json.load(shop)[item]
        player = p.Player(qq_id)
        player_money = player["money"]
        if iteminfo['属性'] in ['武器', '防具', '被动技能']:
            num = 1
            price = int(iteminfo['价格']) * num
            if price > player_money:
                await session.send(at_sender=True, message="你上哪去找这那多钱，穷鬼")
                return
            if iteminfo['属性'] == '武器':
                player.attr["weapon"] = item
            if iteminfo['属性'] == '防具':
                player.attr["armor"] = item
            if iteminfo['属性'] == '被动':
                if player.attr["type"] == '魔法使' and item == "吟唱略过":
                    player.attr["passive"] = item
                if player.attr["type"] == '科学使' and item == "矢量操作":
                    player.attr["passive"] = item
            player.attr["money"] -= price
            buy_player = player.attr
            buy_player["id"] = qq_id
            update_user(buy_player)
        elif iteminfo['属性'] == '道具':
            price = int(iteminfo['价格']) * num
            if price > player_money:
                await session.send(at_sender=True, message="你上哪去找这那多钱，穷鬼")
                return
            player.attr["money"] -= price
            add_exp = iteminfo["信息"]["经验"]
            add_time = iteminfo["信息"]["挂机时间"]
            player.attr["exp"] += add_exp
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
            if item == '更换契约':
                delete_player(qq_id)
                await session.send(at_sender=True, message='删号成功')
                return
            player.attr["time"] += add_time * num
            buy_player = player.attr
            buy_player["id"] = qq_id
            update_user(buy_player)
        await session.send(at_sender=True, message='成功购买{item}*{num}'.format(item=item, num=num))
    except Exception as e:
        print(e)


def delete_player(qq_id):
    with open(os.path.join(BASEDIR_JSON, '玩家信息.json'), 'r', encoding='utf-8') as player:
        users = json.load(player)
    del users[str(qq_id)]
    with open(os.path.join(BASEDIR_JSON, '玩家信息.json'), 'w', encoding='utf-8') as player:
        json.dump(users, player, ensure_ascii=False, indent=4)
