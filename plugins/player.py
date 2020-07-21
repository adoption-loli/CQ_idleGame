import os
import json

BASEDIR_JSON = os.path.join(os.path.dirname(__file__), 'json')


class Player:
    def __init__(self, qq_id):
        self.id = qq_id
        self.attr = {
            "type": '未签订',
            "hp": 0,
            "attack": 0,
            "defense": 0,
            "time": 0,
            "place": '未出征',
            "exp": -1,
            "upexp": 0,
            "armor": '无',
            "weapon": '无',
            "passive": '无',
            "real_attack": 0,
            "real_defense": 0,
            "level": 0,
            "money": 0,
            'last_group': 0,
            "史莱姆": 0,
            "巨大史莱姆": 0,
            "文佬的痰": 0,
            "大史莱姆": 0,
            "川建国の手风琴": 0
        }
        self.read()

    def __getitem__(self, item):
        return self.attr[item]

    def read(self):
        players = {}
        with open(os.path.join(BASEDIR_JSON, '玩家信息.json'), 'r', encoding='utf-8') as f:
            players = json.load(f)[str(self.id)]
        for key in self.attr:
            try:
                self.attr[key] = players[key]
            except KeyError:
                pass
        if self.attr['type'] not in ['未签订', '签订中']:
            item = {}
            atk_addition, def_addition = 0, 0
            if self.attr['weapon'] != '无':
                with open(os.path.join(BASEDIR_JSON, '商店.json'), 'r', encoding='utf-8') as f:
                    item = json.load(f)[self.attr['weapon']]
                atk_addition = float(item["攻击"])
                atk_addition += float(item[self.attr['type']]["攻击"])
                def_addition = float(item["防御"])
                def_addition += float(item[self.attr['type']]["防御"])
            if self.attr['armor'] != '无':
                with open(os.path.join(BASEDIR_JSON, '商店.json'), 'r', encoding='utf-8') as f:
                    item = json.load(f)[self.attr['armor']]
                atk_addition = float(item["攻击"])
                atk_addition += float(item[self.attr['type']]["攻击"])
                def_addition = float(item["防御"])
                def_addition += float(item[self.attr['type']]["防御"])
            self.attr['real_attack'] = self.attr['attack'] * (1 + atk_addition)
            self.attr['real_defense'] = self.attr['defense'] * (1 + def_addition)