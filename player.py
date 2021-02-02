import os
import json

from investment import Investment

class Player:
    SAVE_FP = "save.json"

    def __init__(self, game):
        self.game = game

        # Inialize Values
        self.currency = 0
        self.revenue_scale = 1
        self.unlocks = {}
        self.upgrades = {}
        self.managers = {}
        self.investors = {}
        self.investments = {}

    def save(self):
        investment_data = {}
        for _type, investment in self.investments.items():
            investment_data[_type] = investment.quantity
        save_data = {
            "currency": self.currency,
            "revenue_scale": self.revenue_scale,
            "investments": investment_data
        }
        with open("save.json", "w") as f:
            json.dump(save_data, f)

    def load(self, investments_fp):
        # Load Investment Json and Create Objects
        with open(investments_fp, "r") as f:
            data = json.load(f)
            for investment_dict in data.get('investments'):
                self.investments[investment_dict.get('type')] = Investment(self.game, investment_dict)

        # Load Save Data
        if os.path.exists(Player.SAVE_FP):
            # Load File
            with open(Player.SAVE_FP, "r") as f:
                player_data_json = json.load(f)
                self.currency = player_data_json.get('currency')
                for _type, quantity in player_data_json.get('investments').items():
                    for _ in range(quantity):
                        self.investments.get(_type).upgrade()
        else:
            # Upgrade First Lemonade Stand
            self.investments.get('lemonade_stand').upgrade()