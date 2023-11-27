from copy import deepcopy
from typing import Any, Optional, Iterator
from zipfile import ZipFile

import yaml, re

Asset = dict[str, Any]


def write_yaml_to_zip_file(zip_file: ZipFile, name: str, data, sort_keys: bool):
    zip_file.writestr(name, yaml.dump(data, line_break="\r\n", sort_keys=sort_keys))


def write_unicode_yaml_to_zip_file(zip_file: ZipFile, name: str, data, sort_keys: bool):
    yaml_string = yaml.dump(data, line_break="\r\n", sort_keys=sort_keys)
    yaml_string = re.sub(
        r"en: ([a-zA-Z0-9\\]+)", r'en: "\1"', yaml_string
    )  # surround text of the journal with double quotes to allow for automatic unicode conversion
    yaml_string = yaml_string.replace("NEWLINE", "\\n")
    zip_file.writestr(name, yaml_string)


class ModYml:
    """Builder for a mod.yml file to be used within an OpenKH Mods Manager mod."""

    def __init__(self, title: str, description: Optional[str]):
        self.data: dict[str, Any] = {"title": title}
        if description is not None:
            self.data["description"] = description
        self.data["assets"] = []

    def add_assets(self, assets: list[Asset]):
        existing = self.data["assets"]
        # Using deepcopy to avoid YAML anchors and aliases being used
        for asset in assets:
            existing.append(deepcopy(asset))

    def add_asset(self, asset: Asset):
        self.add_assets([asset])

    def find_assets(self, asset_name: str) -> Iterator[Asset]:
        return (asset for asset in self.data["assets"] if asset["name"] == asset_name)

    def find_asset(self, asset_name: str) -> Optional[Asset]:
        return next(self.find_assets(asset_name), None)

    def add_asset_source(self, asset_name: str, source: dict[str, Any]):
        asset = self.find_asset(asset_name)
        if asset is None:
            raise Exception(f"Unable to find {asset_name} in the mod being built")
        else:
            # Using deepcopy to avoid YAML anchors and aliases being used
            asset["source"].append(deepcopy(source))

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, "mod.yml", self.data, sort_keys=False)


class Bonuses:
    """YAML builder for listpatch for bonuses. See https://openkh.dev/kh2/file/type/00battle.html#bons."""

    def __init__(self, source_name: str):
        self.data: dict[int, dict[str, dict[str, int]]] = {}
        self.source_name = source_name

    def add_bonus(
        self,
        reward_id: int,
        character_name: str,
        character_id: int,
        hp_increase: int,
        mp_increase: int,
        drive_gauge_increase: int,
        item_slot_upgrade: int,
        accessory_slot_upgrade: int,
        armor_slot_upgrade: int,
        bonus_item_1: int,
        bonus_item_2: int,
        padding: int,
    ):
        if reward_id not in self.data:
            self.data[reward_id] = {}
        self.data[reward_id][character_name] = {
            "RewardId": reward_id,
            "CharacterId": character_id,
            "HpIncrease": hp_increase,
            "MpIncrease": mp_increase,
            "DriveGaugeUpgrade": drive_gauge_increase,
            "ItemSlotUpgrade": item_slot_upgrade,
            "AccessorySlotUpgrade": accessory_slot_upgrade,
            "ArmorSlotUpgrade": armor_slot_upgrade,
            "BonusItem1": bonus_item_1,
            "BonusItem2": bonus_item_2,
            "Padding": padding,
            # "Description": ?,
            # "Unknown0c": ?,
        }

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=True)


class FormLevels:
    """YAML builder for listpatch for form levels. See https://openkh.dev/kh2/file/type/00battle.html#fmlv."""

    def __init__(self, source_name: str):
        self.data: dict[str, list[dict[str, int]]] = {}
        self.source_name = source_name

    def add_form_level(
        self,
        form_name: str,
        form_id: int,
        form_level: int,
        ability: int,
        experience: int,
        growth_ability_level: int,
    ):
        if form_name not in self.data:
            self.data[form_name] = []
        self.data[form_name].append(
            {
                "FormId": form_id,
                "FormLevel": form_level,
                "Experience": experience,
                "Ability": ability,
                "GrowthAbilityLevel": growth_ability_level,
            }
        )

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=False)


class Items:
    """YAML builder for listpatch for items. See https://openkh.dev/kh2/file/type/03system.html#item."""

    def __init__(self, source_name: str):
        self.data: dict[str, list[dict[str, int]]] = {
            "Stats": [],
            "Items": [],
        }
        self.source_name = source_name

    def add_stats(
        self,
        location_id: int,
        attack: int,
        magic: int,
        defense: int,
        ability: int,
        ability_points: int,
        unknown_08: int,
        fire_resistance: int,
        ice_resistance: int,
        lightning_resistance: int,
        dark_resistance: int,
        unknown_0d: int,
        general_resistance: int,
        unknown: int,
    ):
        self.data["Stats"].append(
            {
                "Id": location_id,
                "Attack": attack,
                "Magic": magic,
                "Defense": defense,
                "Ability": ability,
                "AbilityPoints": ability_points,
                "Unknown08": unknown_08,
                "FireResistance": fire_resistance,
                "IceResistance": ice_resistance,
                "LightningResistance": lightning_resistance,
                "DarkResistance": dark_resistance,
                "Unknown0d": unknown_0d,
                "GeneralResistance": general_resistance,
                "Unknown": unknown,
            }
        )

    def add_item(
        self,
        item_id: int,
        item_type: str,
        flag_0: int,
        flag_1: int,
        rank: str,
        stat_entry: int,
        name: int,
        description: int,
        shop_buy: int,
        shop_sell: int,
        command: int,
        slot: int,
        picture: int,
        icon_1: int,
        icon_2: int,
    ):
        self.data["Items"].append(
            {
                "Id": item_id,
                "Type": item_type,
                "Flag0": flag_0,
                "Flag1": flag_1,
                "Rank": rank,
                "StatEntry": stat_entry,
                "Name": name,
                "Description": description,
                "ShopBuy": shop_buy,
                "ShopSell": shop_sell,
                "Command": command,
                "Slot": slot,
                "Picture": picture,
                "Icon1": icon_1,
                "Icon2": icon_2,
            }
        )

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=False)


class LevelUps:
    """YAML builder for listpatch for level ups. See https://openkh.dev/kh2/file/type/00battle.html#lvup."""

    def __init__(self, source_name: str):
        self.data: dict[str, dict[int, dict[str, Any]]] = {"Sora": {}}
        self.source_name = source_name

    def add_sora_level(
        self,
        level: int,
        experience: int,
        strength: int,
        magic: int,
        defense: int,
        ap: int,
        sword_ability: int,
        shield_ability: int,
        staff_ability: int,
        padding: int,
    ):
        self.data["Sora"][level] = {
            "Character": "Sora",
            "Level": level,
            "Exp": experience,
            "Strength": strength,
            "Magic": magic,
            "Defense": defense,
            "Ap": ap,
            "SwordAbility": sword_ability,
            "ShieldAbility": shield_ability,
            "StaffAbility": staff_ability,
            "Padding": padding,
        }

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=True)


class Messages:
    """YAML builder for listpatch for items. See the kh2msg section at https://openkh.dev/tool/GUI.ModsManager."""

    def __init__(self, source_name: str, unicode_output: bool = False):
        self.data: list[dict[str, Any]] = []
        self.source_name = source_name
        self.unicode_output = unicode_output

    def add_message(
        self, message_id: int, en: Optional[str] = None, jp: Optional[str] = None
    ):
        entry = {"id": message_id}
        if en is not None:
            entry["en"] = en
        if jp is not None:
            entry["jp"] = jp
        self.data.append(entry)

    def write_to_zip_file(self, zip_file: ZipFile):
        if not self.unicode_output:
            write_yaml_to_zip_file(
                zip_file, self.source_name, self.data, sort_keys=False
            )
        else:
            write_unicode_yaml_to_zip_file(
                zip_file, self.source_name, self.data, sort_keys=False
            )


class PlayerParams:
    """YAML builder for listpatch for player params. See https://openkh.dev/kh2/file/type/00battle.html#plrp."""

    def __init__(self, source_name: str):
        self.data: list[dict] = []
        self.source_name = source_name

    def add_player(
        self,
        character_id: int,
        identifier: int,
        hp: int,
        mp: int,
        ap: int,
        armor_slot_max: int,
        accessory_slot_max: int,
        item_slot_max: int,
        items: list[int],
        padding: list[int],
    ):
        self.data.append(
            {
                "Character": character_id,
                "Id": identifier,
                "Hp": hp,
                "Mp": mp,
                "Ap": ap,
                "ArmorSlotMax": armor_slot_max,
                "AccessorySlotMax": accessory_slot_max,
                "ItemSlotMax": item_slot_max,
                "Items": items,
                "Padding": padding,
            }
        )

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=False)


class PrizeTable:
    """YAML builder for listpatch for prize table. See https://openkh.dev/kh2/file/type/00battle.html#przt."""

    def __init__(self, source_name: str):
        self.data: list[dict[str, int]] = []
        self.source_name = source_name

    def has_entries(self):
        return len(self.data) > 0

    def add_prize(
        self,
        identifier: int,
        small_hp_orbs: int,
        big_hp_orbs: int,
        big_money_orbs: int,
        medium_money_orbs: int,
        small_money_orbs: int,
        small_mp_orbs: int,
        big_mp_orbs: int,
        small_drive_orbs: int,
        big_drive_orbs: int,
        item_1: int,
        item_1_percentage: int,
        item_2: int,
        item_2_percentage: int,
        item_3: int,
        item_3_percentage: int,
    ):
        self.data.append(
            {
                "Id": identifier,
                "SmallHpOrbs": small_hp_orbs,
                "BigHpOrbs": big_hp_orbs,
                "BigMoneyOrbs": big_money_orbs,
                "MediumMoneyOrbs": medium_money_orbs,
                "SmallMoneyOrbs": small_money_orbs,
                "SmallMpOrbs": small_mp_orbs,
                "BigMpOrbs": big_mp_orbs,
                "SmallDriveOrbs": small_drive_orbs,
                "BigDriveOrbs": big_drive_orbs,
                "Item1": item_1,
                "Item1Percentage": item_1_percentage,
                "Item2": item_2,
                "Item2Percentage": item_2_percentage,
                "Item3": item_3,
                "Item3Percentage": item_3_percentage,
            }
        )

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=False)


class Treasures:
    """YAML builder for listpatch for treasures. See https://openkh.dev/kh2/file/type/03system.html#trsr."""

    def __init__(self, source_name: str):
        self.data: dict[int, dict[str, int]] = {}
        self.source_name = source_name

    def add_treasure(self, location_id: int, item_id: int):
        self.data[location_id] = {"ItemId": item_id}

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=True)
        
class ATKPObject:
    def __init__(self, SubId: int, Id: int, Type: str, CriticalAdjust: int, Power: int, Team: int,
                 Element: int, EnemyReaction: int, EffectOnHit: int, KnockbackStrength1: int, KnockbackStrength2: int, 
                 Unknown: int, Flags, RefactSelf: str, RefactOther: str, ReflectedMotion: int, ReflectedHitBack: int,
                 ReflectAction: int, ReflectHitSound: int, ReflectRC: int, ReflectRange: int, ReflectAngle: int, 
                 DamageEffect: int, Switch: int, Interval: int, FloorCheck: int, DriveDrain: int, RevengeDamage: int,
                 AttackTrReaction: str, ComboGroup: int, RandomEffect: int, Kind, HPDrain: int):
        self.SubId = SubId
        self.Id = Id
        self.Type = Type
        self.CriticalAdjust = CriticalAdjust
        self.Power = Power
        self.Team = Team
        self.Element = Element
        self.EnemyReaction = EnemyReaction
        self.EffectOnHit = EffectOnHit
        self.KnockbackStrength1 = KnockbackStrength1
        self.KnockbackStrength2 = KnockbackStrength2
        self.Unknown = Unknown
        self.Flags = Flags
        self.RefactSelf = RefactSelf
        self.RefactOther = RefactOther
        self.ReflectedMotion = ReflectedMotion
        self.ReflectedHitBack = ReflectedHitBack
        self.ReflectAction = ReflectAction
        self.ReflectHitSound = ReflectHitSound
        self.ReflectRC = ReflectRC
        self.ReflectRange = ReflectRange
        self.ReflectAngle = ReflectAngle
        self.DamageEffect = DamageEffect
        self.Switch = Switch
        self.Interval = Interval
        self.FloorCheck = FloorCheck
        self.DriveDrain = DriveDrain
        self.RevengeDamage = RevengeDamage
        self.AttackTrReaction = AttackTrReaction
        self.ComboGroup = ComboGroup
        self.RandomEffect = RandomEffect
        self.Kind = Kind
        self.HPDrain = HPDrain

class AttackEntriesOrganizer:
    
    def __init__(self, source_name: str):
        self.data: list[dict] = []
        self.source_name = source_name
    
    def convert_atkp_object_to_dict_and_add_to_data(self, atkp_object: ATKPObject):
        self.data.append({
            "SubId": atkp_object.SubId,
            "Id": atkp_object.Id, 
            "Type": atkp_object.Type, 
            "CriticalAdjust": atkp_object.CriticalAdjust, 
            "Power": atkp_object.Power, 
            "Team": atkp_object.Team, 
            "Element": atkp_object.Element, 
            "EnemyReaction": atkp_object.EnemyReaction, 
            "EffectOnHit": atkp_object.EffectOnHit, 
            "KnockbackStrength1": atkp_object.KnockbackStrength1, 
            "KnockbackStrength2": atkp_object.KnockbackStrength2, 
            "Unknown": atkp_object.Unknown, 
            "Flags": atkp_object.Flags, 
            "RefactSelf": atkp_object.RefactSelf, 
            "RefactOther": atkp_object.RefactOther, 
            "ReflectedMotion": atkp_object.ReflectedMotion, 
            "ReflectedHitBack": atkp_object.ReflectedHitBack, 
            "ReflectAction": atkp_object.ReflectAction, 
            "ReflectHitSound": atkp_object.ReflectHitSound, 
            "ReflectRC": atkp_object.ReflectRC, 
            "ReflectRange": atkp_object.ReflectRange, 
            "ReflectAngle": atkp_object.ReflectAngle, 
            "DamageEffect": atkp_object.DamageEffect, 
            "Switch": atkp_object.Switch,
            "Interval": atkp_object.Interval,
            "FloorCheck": atkp_object.FloorCheck, 
            "DriveDrain": atkp_object.DriveDrain, 
            "RevengeDamage": atkp_object.RevengeDamage, 
            "AttackTrReaction": atkp_object.AttackTrReaction, 
            "ComboGroup": atkp_object.ComboGroup, 
            "RandomEffect": atkp_object.RandomEffect, 
            "Kind": atkp_object.Kind, 
            "HPDrain": atkp_object.HPDrain,
        })
        
    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=False)
        
    def has_entries(self):
        return len(self.data) > 0

    def attack_entry_constructor(self, values):
        return ATKPObject(
            values['SubId'],
            values['Id'],
            values['Type'], 
            values['CriticalAdjust'], 
            values['Power'], 
            values['Team'], 
            values['Element'], 
            values['EnemyReaction'], 
            values['EffectOnHit'], 
            values['KnockbackStrength1'], 
            values['KnockbackStrength2'], 
            values['Unknown'], 
            values['Flags'], 
            values['RefactSelf'], 
            values['RefactOther'], 
            values['ReflectedMotion'], 
            values['ReflectedHitBack'], 
            values['ReflectAction'], 
            values['ReflectHitSound'], 
            values['ReflectRC'], 
            values['ReflectRange'], 
            values['ReflectAngle'], 
            values['DamageEffect'], 
            values['Switch'], 
            values['Interval'], 
            values['FloorCheck'], 
            values['DriveDrain'], 
            values['RevengeDamage'], 
            values['AttackTrReaction'], 
            values['ComboGroup'], 
            values['RandomEffect'], 
            values['Kind'], 
            values['HPDrain'])
    
    def get_attack_using_ids(self, SubId, Id):
        with open('static/AtkpList.yml', 'r') as file:
            list_data = yaml.safe_load(file)
            
        for attack_entry in list_data:
            if(attack_entry['SubId'] == SubId and attack_entry['Id'] == Id):
                return self.attack_entry_constructor(attack_entry)
            
    #Used specifically for moves with two Ids that have the same number and same SubId but with different power and uses (like goofy tornado) 
    def get_attack_using_ids_plus_power(self, SubId, Id, Power):
        with open('static/AtkpList.yml', 'r') as file:
            list_data = yaml.safe_load(file)
            
        for attack_entry in list_data:
            if(attack_entry['SubId'] == SubId and attack_entry['Id'] == Id and attack_entry['Power'] == Power):
                return self.attack_entry_constructor(attack_entry)
        