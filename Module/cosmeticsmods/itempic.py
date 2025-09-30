import json
import os
import random
from pathlib import Path

from Class.openkhmod import Asset
from List import configDict
from Module import appconfig


class Itempic:

    def __init__(self, itempic_id: str, item_name: str, types: list[str], custom: bool = False):
        super().__init__()
        self.itempic_id = itempic_id
        self.item_name = item_name
        self.types = types
        self.custom = custom

    def filename(self) -> str:
        return f"remastered/itempic/item-{self.itempic_id}.imd/-0.dds"


class ItempicRandomizer:

    @staticmethod
    def directory_name() -> str:
        return "item-pictures"

    @staticmethod
    def itempic_rando_options() -> dict[str, str]:
        return {
            configDict.VANILLA: "Vanilla",
            configDict.RANDOMIZE_IN_GAME_ONLY: "Randomize (in-game only)",
            configDict.RANDOMIZE_CUSTOM_ONLY: "Randomize (custom only)",
            configDict.RANDOMIZE_ALL: "Randomize (in-game + custom)",
        }

    @staticmethod
    def bootstrap_itempic_file() -> Path:
        """Creates the itempic list file if needed."""
        itempic_list_file_path = Path("item-pictures.json")
        if not itempic_list_file_path.is_file():
            with open(itempic_list_file_path, mode="w", encoding="utf-8") as itempic_list_file:
                mapped = []
                for itempic in ItempicRandomizer.replaceable_itempics():
                    mapped.append({
                        "id": itempic.itempic_id,
                        "name": itempic.item_name,
                        "type": itempic.types,
                    })
                json.dump(mapped, itempic_list_file, indent=4)
        return itempic_list_file_path

    @staticmethod
    def randomize_itempics(setting: str) -> list[Asset]:
        if setting == configDict.VANILLA:
            return []

        # We could maybe give an option here, but not sure if it's necessary
        categorize = True

        replacements_by_category: dict[str, list[tuple[bool, str]]] = {}  # (internal, path)

        if setting == configDict.RANDOMIZE_IN_GAME_ONLY or setting == configDict.RANDOMIZE_ALL:
            for category, game_files in ItempicRandomizer._collect_game_itempic_files(categorize).items():
                if category not in replacements_by_category:
                    replacements_by_category[category] = []
                replacements_by_category[category].extend((True, file) for file in game_files)

        if setting == configDict.RANDOMIZE_CUSTOM_ONLY or setting == configDict.RANDOMIZE_ALL:
            for category, custom_files in ItempicRandomizer.collect_custom_itempic_files(categorize).items():
                if category not in replacements_by_category:
                    replacements_by_category[category] = []
                replacements_by_category[category].extend((False, str(path)) for path in custom_files)

        backup_files_by_categories: dict[str, list[tuple[bool, str]]] = {}
        for category, replacements in replacements_by_category.items():
            backup_files_by_categories[category] = replacements.copy()
            random.shuffle(replacements)

        assets: list[Asset] = []

        itempic_list_file_path = ItempicRandomizer.bootstrap_itempic_file()
        with open(itempic_list_file_path, encoding="utf-8") as itempic_list_file:
            itempic_metadata = json.load(itempic_list_file)
        random.shuffle(itempic_metadata)
        for info in itempic_metadata:
            itempic_id: str = info["id"]
            types: list[str] = [
                item_type.lower() for item_type in info["type"] if item_type.lower() in replacements_by_category
            ]
            if len(types) > 0:
                random.shuffle(types)

                for chosen_type in types:
                    itempics_for_chosen_type = replacements_by_category.get(chosen_type, [])

                    # Unlike the music rando we'll just always allow duplicate replacements here to simplify
                    if len(itempics_for_chosen_type) == 0:
                        refill_list = backup_files_by_categories.get(chosen_type, []).copy()
                        random.shuffle(refill_list)
                        replacements_by_category[chosen_type] = refill_list
                        itempics_for_chosen_type = refill_list

                    if len(itempics_for_chosen_type) > 0:
                        internal, chosen_itempic = itempics_for_chosen_type.pop()

                        asset = {
                            "name": f"remastered/itempic/item-{itempic_id}.imd/-0.dds",
                            "platform": "pc",
                            "method": "copy",
                            "source": [{"name": chosen_itempic}]
                        }
                        if internal:
                            asset["source"][0]["type"] = "internal"

                        assets.append(asset)

                        break

        return assets

    @staticmethod
    def replaceable_itempics() -> list[Itempic]:
        def consumable(itempic_id: str, item_name: str) -> Itempic:
            return Itempic(itempic_id=itempic_id, item_name=item_name, types=["Consumable", "Consumable", "Wild"])

        def keyblade(itempic_id: str, item_name: str, custom: bool = False) -> Itempic:
            return Itempic(itempic_id=itempic_id, item_name=item_name, types=["Keyblade"], custom=custom)

        def staff(itempic_id: str, item_name: str) -> Itempic:
            return Itempic(itempic_id=itempic_id, item_name=item_name, types=["Staff"])

        def shield(itempic_id: str, item_name: str) -> Itempic:
            return Itempic(itempic_id=itempic_id, item_name=item_name, types=["Shield"])

        def armor(itempic_id: str, item_name: str) -> Itempic:
            return Itempic(itempic_id=itempic_id, item_name=item_name, types=["Armor", "Armor", "Wild"])

        def accessory(itempic_id: str, item_name: str) -> Itempic:
            return Itempic(itempic_id=itempic_id, item_name=item_name, types=["Accessory", "Accessory", "Wild"])

        def synthesis(itempic_id: str, item_name: str) -> Itempic:
            return Itempic(itempic_id=itempic_id, item_name=item_name, types=["Synthesis", "Synthesis", "Wild"])

        result = [
            Itempic("000", "Map (Large)", types=["Map"]),

            consumable("001", "Potion"),
            consumable("002", "Hi-Potion"),
            consumable("003", "Mega Potion"),
            consumable("004", "Ether"),
            consumable("005", "Hi-Ether"),
            consumable("006", "Mega Ether"),
            consumable("007", "Elixir"),
            consumable("008", "Megalixir"),
            consumable("009", "Drive Recovery"),
            consumable("010", "High Drive Recovery"),

            Itempic("011", "Map (Small)", types=["Map"]),

            Itempic("012", "Action Ability", types=["ActionAbility"], custom=True),
            Itempic("013", "Growth Ability", types=["GrowthAbility"], custom=True),
            Itempic("014", "Support Ability", types=["SupportAbility"], custom=True),
            Itempic("015", "Dummy 23 (HP Up)", types=["StatIncrease", "StatIncrease", "Wild"], custom=True),
            Itempic("016", "Dummy 24 (MP Up)", types=["StatIncrease", "StatIncrease", "Wild"], custom=True),
            Itempic("017", "Dummy 25 (Drive Up)", types=["StatIncrease", "StatIncrease", "Wild"], custom=True),
            Itempic("018", "Dummy 26 (Armor Slot Up)", types=["StatIncrease", "StatIncrease", "Wild"], custom=True),
            Itempic("019", "Dummy 27 (Accessory Slot Up)", types=["StatIncrease", "StatIncrease", "Wild"], custom=True),
            Itempic("020", "Dummy 16 (Item Slot Up)", types=["StatIncrease", "StatIncrease", "Wild"], custom=True),

            Itempic("021", "Torn Pages", types=["TornPage"]),

            consumable("033", "Tent"),
            consumable("034", "Power Boost"),
            consumable("035", "Magic Boost"),
            consumable("036", "Defense Boost"),
            consumable("037", "AP Boost"),

            keyblade("043", "Kingdom Key"),
            keyblade("044", "Oathkeeper"),
            keyblade("045", "Oblivion"),
            keyblade("046", "Star Seeker"),
            keyblade("047", "Hidden Dragon"),
            keyblade("048", "Hero's Crest"),
            keyblade("049", "Monochrome"),
            keyblade("050", "Follow the Wind"),
            keyblade("051", "Circle of Life"),
            keyblade("052", "Photon Debugger"),
            keyblade("053", "Gull Wing"),
            keyblade("054", "Rumbling Rose"),
            keyblade("055", "Guardian Soul"),
            keyblade("056", "Wishing Lamp"),
            keyblade("057", "Decisive Pumpkin"),
            keyblade("058", "Sleeping Lion"),
            keyblade("059", "Sweet Memories"),
            keyblade("060", "Mysterious Abyss"),
            keyblade("061", "Fatal Crest"),
            keyblade("062", "Bond of Flame"),
            keyblade("063", "Fenrir"),
            keyblade("064", "Ultima Weapon"),
            keyblade("065", "Struggle Hammer"),
            keyblade("066", "Struggle Wand"),
            keyblade("067", "Struggle Sword"),

            staff("068", "Mage's Staff"),
            staff("069", "Hammer Staff"),
            staff("070", "Victory Bell"),
            staff("071", "Meteor Staff"),
            staff("072", "Comet Staff"),
            staff("073", "Lord's Broom"),
            staff("074", "Wisdom Wand"),
            staff("075", "Rising Dragon"),
            staff("076", "Nobody Lance"),
            staff("077", "Shaman's Relic"),
            staff("078", "Save the Queen"),

            shield("080", "Knight's Shield"),
            shield("081", "Adamant Shield"),
            shield("082", "Chain Gear"),
            shield("083", "Ogre Shield"),
            shield("084", "Falling Star"),
            shield("085", "Dreamcloud"),
            shield("086", "Knight Defender"),
            shield("087", "Genji Shield"),
            shield("088", "Akashic Record"),
            shield("089", "Nobody Guard"),
            shield("090", "Save the King"),

            Itempic("091", "Dummy 13 (Royal Summons)", types=["RoyalSummons"], custom=True),
            Itempic("092", "Scimitar", types=["Scimitar"]),
            Itempic("093", "Battlefields of War", types=["BattlefieldsOfWar"]),
            Itempic("094", "Sword of the Ancestor", types=["SwordOfTheAncestor"]),
            Itempic("095", "Identity Disk", types=["IdentityDisk"]),
            Itempic("096", "Skill and Crossbones", types=["SkillAndCrossbones"]),
            Itempic("097", "Way to the Dawn", types=["WayToTheDawn"]),
            Itempic("098", "Beast's Claw", types=["BeastsClaw"]),
            Itempic("099", "Bone Fist", types=["BoneFist"]),
            Itempic("100", "Proud Fang", types=["ProudFang"]),

            armor("101", "Elven Bandana"),
            armor("102", "Divine Bandana"),
            armor("103", "Power Band"),
            armor("104", "Buster Band"),
            armor("105", "Protect Belt"),
            armor("106", "Gaia Belt"),
            armor("107", "Cosmic Belt"),
            armor("113", "Fire Bangle"),
            armor("114", "Fira Bangle"),
            armor("115", "Firaga Bangle"),
            armor("116", "Firagun Bangle"),
            armor("118", "Blizzard Armlet"),
            armor("119", "Blizzara Armlet"),
            armor("120", "Blizzaga Armlet"),
            armor("121", "Blizzagun Armlet"),
            armor("123", "Thunder Trinket"),
            armor("124", "Thundara Trinket"),
            armor("125", "Thundaga Trinket"),
            armor("126", "Thundagun Trinket"),
            armor("128", "Shadow Anklet"),
            armor("129", "Dark Anklet"),
            armor("130", "Midnight Anklet"),
            armor("131", "Chaos Anklet"),
            armor("133", "Abas Chain"),
            armor("134", "Aegis Chain"),
            armor("135", "Acrisius"),
            armor("136", "Ribbon"),
            armor("137", "Champion Belt"),
            armor("138", "Petite Ribbon"),
            armor("139", "Acrisius+"),
            armor("140", "Cosmic Chain"),

            accessory("149", "Ability Ring"),
            accessory("150", "Engineer's Ring"),
            accessory("151", "Technician's Ring"),
            accessory("152", "Expert's Ring"),
            accessory("153", "Sardonyx Ring"),
            accessory("154", "Tourmaline Ring"),
            accessory("155", "Aquamarine Ring"),
            accessory("156", "Garnet Ring"),
            accessory("157", "Diamond Ring"),
            accessory("158", "Silver Ring"),
            accessory("159", "Gold Ring"),
            accessory("160", "Platinum Ring"),
            accessory("161", "Mythril Ring"),
            accessory("162", "Orichalcum Ring"),
            accessory("163", "Master's Ring"),
            accessory("164", "Moon Amulet"),
            accessory("165", "Star Charm"),
            accessory("166", "Skill Ring"),
            accessory("167", "Skillful Ring"),
            accessory("168", "Soldier Earring"),
            accessory("169", "Fencer Earring"),
            accessory("170", "Mage Earring"),
            accessory("171", "Slayer Earring"),
            accessory("172", "Cosmic Ring"),
            accessory("173", "Medal"),
            accessory("174", "Cosmic Arts"),
            accessory("177", "Lucky Ring"),
            accessory("179", "Draw Ring"),

            synthesis("181", "Dark Shard"),
            synthesis("182", "Dark Stone"),
            synthesis("183", "Dark Gem"),
            synthesis("184", "Dark Crystal"),
            synthesis("185", "Blazing Shard"),
            synthesis("186", "Blazing Stone"),
            synthesis("187", "Blazing Gem"),
            synthesis("188", "Blazing Crystal"),
            synthesis("189", "Frost Shard"),
            synthesis("190", "Frost Stone"),
            synthesis("191", "Frost Gem"),
            synthesis("192", "Frost Crystal"),
            synthesis("193", "Lightning Shard"),
            synthesis("194", "Lightning Stone"),
            synthesis("195", "Lightning Gem"),
            synthesis("196", "Lightning Crystal"),
            synthesis("197", "Power Shard"),
            synthesis("198", "Power Stone"),
            synthesis("199", "Power Gem"),
            synthesis("200", "Power Crystal"),
            synthesis("201", "Lucid Shard"),
            synthesis("202", "Lucid Stone"),
            synthesis("203", "Lucid Gem"),
            synthesis("204", "Lucid Crystal"),
            synthesis("205", "Dense Shard"),
            synthesis("206", "Dense Stone"),
            synthesis("207", "Dense Gem"),
            synthesis("208", "Dense Crystal"),
            synthesis("209", "Twilight Shard"),
            synthesis("210", "Twilight Stone"),
            synthesis("211", "Twilight Gem"),
            synthesis("212", "Twilight Crystal"),
            synthesis("213", "Mythril Shard"),
            synthesis("214", "Mythril Stone"),
            synthesis("215", "Mythril Gem"),
            synthesis("216", "Mythril Crystal"),
            synthesis("217", "Bright Shard"),
            synthesis("218", "Bright Stone"),
            synthesis("219", "Bright Gem"),
            synthesis("220", "Bright Crystal"),

            Itempic("221", "Lamp Charm", types=["LampCharm"]),
            Itempic("222", "Ukulele Charm", types=["UkuleleCharm"]),
            Itempic("223", "Feather Charm", types=["FeatherCharm"]),
            Itempic("224", "Baseball Charm", types=["BaseballCharm"]),
            Itempic("225", "Munny Pouch", types=["MunnyPouch"]),
            Itempic("226", "Lucky Emblem", types=["LuckyEmblem"]),
            Itempic("227", "Struggle Trophy", types=["OtherItem", "OtherItem", "Wild"]),
            Itempic("228", "Struggle Poster", types=["OtherItem", "OtherItem", "Wild"]),
            Itempic("229", "Poster", types=["OtherItem", "OtherItem", "Wild"]),
            Itempic("230", "???", types=["OtherItem", "OtherItem", "Wild"]),
            Itempic("231", "Namine's Sketches", types=["NaminesSketches"]),
            Itempic("232", "Membership Card", types=["MembershipCard"]),
            Itempic("233", "Olympus Stone", types=["OlympusStone"]),
            Itempic("234", "Auron's Statue", types=["OtherItem", "OtherItem", "Wild"]),
            Itempic("235", "Cursed Medallion", types=["OtherItem", "OtherItem", "Wild"]),
            Itempic("236", "Present", types=["OtherItem", "OtherItem", "Wild"]),
            Itempic("237", "Decoy Presents", types=["OtherItem", "OtherItem", "Wild"]),
            Itempic("238", "Ice Cream", types=["IceCream"]),
            Itempic("239", "Picture", types=["OtherItem", "OtherItem", "Wild"]),

            Itempic("240", "Dummy 15 (Unknown Disk)", types=["UnknownDisk"], custom=True),

            Itempic("241", "Secret Ansem Report", types=["AnsemReport"]),
            Itempic("241", "Cursed Medallion", types=["OtherItem", "OtherItem", "Wild"]),
            Itempic("242", "Promise Charm", types=["PromiseCharm"]),
            Itempic("243", "Synthesis Recipe", types=["Recipe"]),
            Itempic("244", "Hades Cup Trophy", types=["HadesCupTrophy"]),

            Itempic("266", "Valor Form", types=["ValorForm"]),
            Itempic("267", "Wisdom Form", types=["WisdomForm"]),
            Itempic("268", "Master Form", types=["MasterForm"]),
            Itempic("269", "Final Form", types=["FinalForm"], custom=True),
            Itempic("270", "Magic Element", types=["MagicElement"]),

            Itempic("271", "Anti Form", types=["AntiForm"], custom=True),

            synthesis("272", "Energy Shard"),
            synthesis("273", "Energy Stone"),
            synthesis("274", "Energy Gem"),
            synthesis("275", "Energy Crystal"),
            synthesis("276", "Serenity Shard"),
            synthesis("277", "Serenity Stone"),
            synthesis("278", "Serenity Gem"),
            synthesis("279", "Serenity Crystal"),
            synthesis("280", "Orichalcum"),
            synthesis("281", "Orichalcum+"),

            keyblade("296", "Pureblood", custom=True),
            keyblade("297", "Alpha Weapon", custom=True),
            keyblade("298", "Omega Weapon", custom=True),
            keyblade("299", "Kingdom Key D", custom=True),

            keyblade("300", "Two Become One"),
            keyblade("301", "Winner's Proof"),

            staff("302", "Save the Queen+"),
            staff("303", "Centurion"),
            staff("304", "Centurion+"),
            staff("305", "Plain Mushroom"),
            staff("306", "Plain Mushroom+"),
            staff("307", "Precious Mushroom"),
            staff("308", "Precious Mushroom+"),
            staff("309", "Premium Mushroom"),

            shield("310", "Save the King+"),
            shield("311", "Frozen Pride"),
            shield("312", "Frozen Pride+"),
            shield("313", "Joyous Mushroom"),
            shield("314", "Joyous Mushroom+"),
            shield("315", "Majestic Mushroom"),
            shield("316", "Majestic Mushroom+"),
            shield("317", "Ultimate Mushroom"),

            staff("318", "Shaman's Relic+"),
            shield("319", "Akashic Record+"),

            Itempic("320", "Limit Form", types=["LimitForm"]),
            Itempic("321", "Proof of Connection", types=["ProofOfConnection"]),
            Itempic("322", "Proof of Nonexistence", types=["ProofOfNonexistence"]),
            Itempic("323", "Proof of Peace", types=["ProofOfPeace"]),

            Itempic("324", "Fire Element", types=["FireElement"], custom=True),
            Itempic("325", "Blizzard Element", types=["BlizzardElement"], custom=True),
            Itempic("326", "Thunder Element", types=["ThunderElement"], custom=True),
            Itempic("327", "Cure Element", types=["CureElement"], custom=True),
            Itempic("328", "Magnet Element", types=["MagnetElement"], custom=True),
            Itempic("329", "Reflect Element", types=["ReflectElement"], custom=True),

            armor("330", "Shock Charm"),
            armor("331", "Shock Charm+"),
            armor("332", "Grand Ribbon"),

            accessory("340", "Shadow Archive"),
            accessory("341", "Shadow Archive+"),
            accessory("342", "Full Bloom"),
            accessory("344", "Executive's Ring"),

            synthesis("350", "Remembrance Shard"),
            synthesis("351", "Remembrance Stone"),
            synthesis("352", "Remembrance Gem"),
            synthesis("353", "Remembrance Crystal"),
            synthesis("354", "Tranquility Shard"),
            synthesis("355", "Tranquility Stone"),
            synthesis("356", "Tranquility Gem"),
            synthesis("357", "Tranquility Crystal"),
            synthesis("358", "Manifest Illusion"),
            synthesis("359", "Lost Illusion"),
        ]

        return result

    @staticmethod
    def _collect_game_itempic_files(categorize: bool) -> dict[str, list[str]]:
        """Returns game itempic files grouped by category."""
        result: dict[str, list[str]] = {}

        for itempic in ItempicRandomizer.replaceable_itempics():
            if itempic.custom:
                continue

            resolved_category = itempic.types[0].lower()
            if not categorize:
                resolved_category = "wild"
            if resolved_category not in result:
                result[resolved_category] = []
            result[resolved_category].append(itempic.filename())

        return result

    @staticmethod
    def collect_custom_itempic_files(categorize: bool) -> dict[str, list[Path]]:
        """Returns custom itempic files grouped by category."""
        result: dict[str, list[Path]] = {}

        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is not None:
            item_pictures_path = custom_visuals_path / ItempicRandomizer.directory_name()
            if item_pictures_path.is_dir():
                for child in [str(category_file).lower() for category_file in os.listdir(item_pictures_path)]:
                    child_path = item_pictures_path / child
                    if child_path.is_dir():
                        category_pics: list[Path] = []
                        for root, dirs, files in os.walk(child_path):
                            root_path = Path(root)
                            for file in files:
                                _, extension = os.path.splitext(file)
                                if extension.lower() == ".dds" or extension.lower() == ".png":
                                    file_path = root_path / file
                                    category_pics.append(file_path)
                        resolved_category = child
                        if not categorize:
                            resolved_category = "wild"
                        if resolved_category not in result:
                            result[resolved_category] = []
                        result[resolved_category] += category_pics

        return result
