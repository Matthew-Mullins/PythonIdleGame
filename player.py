import os
import json

class Player:
    SAVE_FP = "save.json"

    def __init__(self, game):
        self.game = game

        # Inialize Values
        self.currency = 0
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
            "investments": investment_data
        }
        with open("save.json", "w") as f:
            json.dump(save_data, f)

    def load(self):
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
        


        # # Try to Load Player Data from File
        # try:
        #     f = open("player_data.json", "r")
        #     player_data = json.load(f)
        #     self.currency = player_data['currency']
        #     for investment in self.investments.values():
        #         if investment.type == 'lemonade_stand' and player_data['investments'][investment.type] == 0:
        #             investment.upgrade()
        #             continue
        #         for i in range(player_data['investments'][investment.type]):
        #             investment.upgrade()
        #     f.close()
        # except:
        #     for investment in self.investments.values():
        #         if investment.type == 'lemonade_stand':
        #             investment.upgrade()