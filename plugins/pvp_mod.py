# from . import enemy as e
from . import player as p
from nonebot import scheduler, on_command, CommandSession, permission
from .main import update_user, PLAYER_JSON
import json
import time
import random


@on_command('PVP', aliases=('pvp', '打人'), permission=permission.GROUP)
async def init_pvp(session: CommandSession):
    player1_id = session.ctx['user_id']
    try:
        player2_id = int(str(session.get('player2_id', prompt='你想和谁PVP(艾特ta即可)')).strip().replace('[CQ:at,qq=', '')[:-1])
    except ValueError as e:
        await session.send(at_sender=True, message='没找到这个人，PVP请求已取消')
        return
    # print(player2_id, type(player2_id))
    if player1_id == player2_id:
        msg = ['这边建议先自宫呢', '是谁杀了你，而你又杀了谁', '不会吧不会吧，不会真的有人要打自己吧', '哦']
        await session.send(at_sender=True, message=random.choice(msg))
        return
    player1 = p.Player(player1_id)
    try:
        player2 = p.Player(player2_id)
    except KeyError as e:
        await session.send(at_sender=True, message='没找到这个人，PVP请求已取消')
        return
    if (player1["type"] not in ["科学使", "魔法使"]) or (player2["type"] not in ["科学使", "魔法使"]):
        await session.send(at_sender=True, message='回复 签订契约 再PVP')
        return
    pvp_info = []
    if random.randint(1, 10) < 7:
        pvp_info.append(f'发起PVP的[CQ:at,qq={player1_id}] 发动突袭(先手)\n')
        p1_first = True
    else:
        pvp_info.append(f'被挑战[CQ:at,qq={player2_id}] 提前埋伏了对手(先手)\n')
        p1_first = False
    while True:
        p1_damage_p2 = player1.attr["real_attack"] - player2.attr["real_defense"] + random.randint(40, 50)
        p2_damage_p1 = player2.attr["real_attack"] - player1.attr["real_defense"] + random.randint(40, 50)
        if p1_damage_p2 <= 0:
            p1_damage_p2 = random.randint(40, 50)
        if p2_damage_p1 <= 0:
            p2_damage_p1 = random.randint(40, 50)
        if p1_first:
            player2.attr["hp"] -= p1_damage_p2
            pvp_info.append(f'对方受到了{p1_damage_p2:.2f}点伤害，剩余生命:{player2.attr["hp"]:.2f}\n')
            if player2.attr["hp"] <= 0:
                pvp_info.append(f'你赢了')
                break
            player1.attr["hp"] -= p2_damage_p1
            pvp_info.append(f'你受到了{p2_damage_p1:.2f}点伤害，剩余生命:{player1.attr["hp"]:.2f}\n')
            if player1.attr["hp"] <= 0:
                pvp_info.append(f'你输了')
                break
        else:
            player1.attr["hp"] -= p2_damage_p1
            pvp_info.append(f'你受到了{p2_damage_p1:.2f}点伤害，剩余生命:{player1.attr["hp"]:.2f}\n')
            if player1.attr["hp"] <= 0:
                pvp_info.append(f'你输了')
                break
            player2.attr["hp"] -= p1_damage_p2
            pvp_info.append(f'对方受到了{p1_damage_p2:.2f}点伤害，剩余生命:{player2.attr["hp"]:.2f}\n')
            if player2.attr["hp"] <= 0:
                pvp_info.append(f'你赢了')
                break
    if len(pvp_info) > 10:
        pvp_info = pvp_info[:5] + ['...'] + pvp_info[-4:]
    await session.send(at_sender=True, message=''.join(pvp_info) + '    没有奖励')
