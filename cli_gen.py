import json
import os
import random
import string
from collections import namedtuple

from Class.seedSettings import ExtraConfigurationData, SeedSettings
from Module import appconfig
from Module.RandomizerSettings import RandomizerSettings
from Module.generate import generateSeedCLI
from Module.seedshare import SharedSeed
from Module.version import LOCAL_UI_VERSION

SeedInfo = namedtuple("SeedInfo",["seed_name","requested_preset","generator_string","hash_icons","spoiler_html"])

requested_preset = "League Spring 2024"

def make_random_seed_from_preset_name(requested_type:str):
    preset_json = {}
    for preset_file_name in os.listdir(appconfig.PRESET_FOLDER):
        preset_name, extension = os.path.splitext(preset_file_name)
        if extension == '.json':
            with open(os.path.join(appconfig.PRESET_FOLDER, preset_file_name), 'r') as presetData:
                try:
                    settings_json = json.load(presetData)
                    preset_json[preset_name] = settings_json
                except Exception:
                    print('Unable to load preset [{}], skipping'.format(preset_file_name))

    # get seed name at random
    characters = string.ascii_letters + string.digits
    seedString = (''.join(random.choice(characters) for i in range(30)))
    makeSpoilerLog = False
    settings = SeedSettings()
    settings.apply_settings_json(preset_json[requested_type])

    shared_seed = SharedSeed(
        generator_version=LOCAL_UI_VERSION,
        seed_name=seedString,
        spoiler_log=makeSpoilerLog,
        settings_string=settings.settings_string(),
        tourney_gen=True
    )
    shared_string_text = shared_seed.to_share_string()

    rando_settings = RandomizerSettings(seedString,makeSpoilerLog,LOCAL_UI_VERSION,settings,shared_string_text)

    extra_data = ExtraConfigurationData(platform="PC", tourney=True, custom_cosmetics_executables=[])

    spoiler_log = generateSeedCLI(rando_settings, extra_data)

    return SeedInfo(
        seed_name=seedString,
        requested_preset=requested_type,
        generator_string=shared_string_text,
        hash_icons=rando_settings.seedHashIcons,
        spoiler_html=spoiler_log
    )


if __name__ == '__main__':
    seed_info = make_random_seed_from_preset_name(requested_preset)
    print(seed_info.generator_string)
    print(seed_info.hash_icons)
