import os
import json

from investment import Investment
from upgrade import Upgrade
from manager import Manager

class Player:
    SAVE_FP = "save.json"

    def __init__(self, game):
        self.game = game

        # Inialize Values
        self.currency = 0
        self.lifetime_earnings = 0
        self.starting_lifetime_earnings = 0
        self.unlocks = {}
        self.upgrades = {}
        self.managers = {}
        self.investors = 0
        self.investments = {}

    def save(self):
        investment_data = {}
        for _type, investment in self.investments.items():
            investment_data_type = investment.serialize()
            investment_data[_type] = investment_data_type
        upgrades_unlocked = []
        for upgrade in self.upgrades.values():
            if upgrade.unlocked:
                upgrades_unlocked.append(upgrade.name)
        managers_unlocked = []
        for manager in self.managers.values():
            if manager.unlocked:
                managers_unlocked.append(manager.name)
        save_data = {
            "currency": self.currency,
            "lifetime_earnings": self.lifetime_earnings,
            "starting_lifetime_earnings": self.starting_lifetime_earnings,
            "investors": self.investors,
            "upgrades": upgrades_unlocked,
            "managers": managers_unlocked,
            "investments": investment_data
        }
        with open("save.json", "w") as f:
            json.dump(save_data, f, indent=4)

    def load(self, investments_fp, upgrades_fp, managers_fp):
        # Load Investment Json and Create Objects
        with open(investments_fp, "r") as f:
            data = json.load(f)
            for investment_dict in data.get('investments'):
                self.investments[investment_dict.get('type')] = Investment(self.game, investment_dict)

        # Load Upgrades
        with open(upgrades_fp, "r") as f:
            data = json.load(f)
            for upgrade in data.get('upgrades'):
                self.upgrades[upgrade.get('name')] = Upgrade(self.game, upgrade)

        # Load Managers
        with open(managers_fp, "r") as f:
            data = json.load(f)
            for manager in data.get('managers'):
                self.managers[manager.get('name')] = Manager(self.game, manager)

        # Load Save Data
        if os.path.exists(Player.SAVE_FP):
            # Load File
            with open(Player.SAVE_FP, "r") as f:
                player_data_json = json.load(f)
                self.currency = player_data_json.get('currency')
                self.lifetime_earnings = player_data_json.get('lifetime_earnings')
                self.starting_lifetime_earnings = player_data_json.get('starting_lifetime_earnings')
                self.investors = player_data_json.get('investors')
                for _type, data in player_data_json.get('investments').items():
                    self.investments.get(_type).deserialize(data)
                for upgrade_name in player_data_json.get('upgrades'):
                    for upgrade in self.upgrades.values():
                        if upgrade_name == upgrade.name:
                            upgrade.unlock()
                for manager_name in player_data_json.get('managers'):
                    for manager in self.managers.values():
                        if manager_name == manager.name:
                            manager.unlock()
        else:
            # Upgrade First Lemonade Stand
            self.investments.get('lemonade_stand').upgrade(1)
        
        print(self.unlocks)
        print(self.upgrades)
        print(self.managers)
        print(self.investments)