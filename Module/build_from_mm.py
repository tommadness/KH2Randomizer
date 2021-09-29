import sys, os, shutil, subprocess, json, time, argparse
from gooey import Gooey, GooeyParser
from zipfile import ZipFile

# CLI usage example
#In [1]: import build_from_mm

#In [2]: build_from_mm.main(cli_args=["-game=kh2", "-mode=patch"])

# TODO blacklist bad directory paths, hide most output and make obvious errors more obvious (try to bulletproof it for non technical people)
# TODO make the mod folder not required
# TODO add music only extract
# TODO verify kh3d extract works
# TODO recom name needs to be capital???
# TODO make a pypi package

# todo make it a library
class KingdomHearts1Patcher:
    def __init__(self, region):
        self.region = region
        self.name = "kh1"
        self.pkgs = ["kh1_first.pkg", "kh1_second.pkg", "kh1_third.pkg", "kh1_fourth.pkg", "kh1_fifth.pkg"]
    def translate_path(self, path):
        if path.startswith(os.sep):
            path = path[1:]
        return path

class KingdomHearts2Patcher:
    def __init__(self, region):
        self.region = region
        self.name = "kh2"
        self.pkgs = ["kh2_first.pkg", "kh2_second.pkg", "kh2_third.pkg", "kh2_fourth.pkg", "kh2_fifth.pkg", "kh2_sixth.pkg"]
    def translate_path(self, path):
        if path.startswith(os.sep):
            path = path[1:]
        if os.sep+"jp"+os.sep in path:
            path = path.replace(os.sep+"jp"+os.sep, os.sep+self.region+os.sep)
        if "ard" in path:
            if not "jp" in path and not self.region in path:
                path = path.replace("ard"+os.sep, "ard"+os.sep+self.region+os.sep)
        if "map" in path:
            # maps don't have region specifier for some reason, or they split it out into two files for some reason...
            path = path.split("map")[0]+"map"+os.sep+path.split(os.sep)[-1]
        if path.endswith(".a.fm"):
            path = path.replace(".a.fm", ".a.{}".format(self.region))
        return path

class BirthBySleepPatcher:
    def __init__(self, region):
        self.region = region
        self.name = "bbs"
        self.pkgs = ["bbs_first.pkg", "bbs_second.pkg", "bbs_third.pkg", "bbs_fourth.pkg"]
    def translate_path(self, path):
        if path.startswith(os.sep):
            path = path[1:]
        return path
class KingdomHearts3DPatcher:
    def __init__(self, region):
        self.region = region
        self.name = "kh3d"
        self.pkgs = self._translate_pkg_paths(["kh3d_first.pkg", "kh3d_second.pkg", "kh3d_third.pkg", "kh3d_fourth.pkg"])
    def _translate_pkg_paths(self, pkgs):
        t_pkgs = []
        for pkg in pkgs:
            t_pkgs.append(os.path.join("..", "..", "..", "KH_2.8", "Image", "en", pkg))
        return t_pkgs
    def translate_path(self, path):
        if path.startswith(os.sep):
            path = path[1:]
        return path

class RecomPatcher:
    def __init__(self, region):
        self.region = region
        self.name = "recom"
        self.pkgs = ["Recom.pkg"]
    def translate_path(self, path):
        if path.startswith(os.sep):
            path = path[1:]
        return path

games = {
    "kh1": KingdomHearts1Patcher,
    "kh2": KingdomHearts2Patcher,
    "bbs": BirthBySleepPatcher,
    "kh3d": KingdomHearts3DPatcher,
    "Recom": RecomPatcher
}
DEFAULTREGION = "us"
DEFAULTGAME = "kh2"

checksums = {'bbs_first.pkg': 'c7623c0459d0b9bb7ba77e966f9d26bc',
 'bbs_fourth.pkg': 'c61f61dd5954d795c03ae17174c15944',
 'bbs_second.pkg': 'a45d032ac2e39637d4cdf54c67b58d1b',
 'bbs_third.pkg': '1eb46d47c521b4b7f127e3e71428cfa0',
 'kh1_fifth.pkg': 'c5527403cf2b8340bf943e916a2971bc',
 'kh1_first.pkg': '188acf5c53948e0dbfaf4d3a1b3a88c4',
 'kh1_fourth.pkg': '00830acd3599236b378208132dbbd538',
 'kh1_second.pkg': '7eb1206e1568448924fd9d7785f618ea',
 'kh1_third.pkg': '2489bdf1e8dbaddd2177bd35d9a4eefd',
 'kh2_fifth.pkg': '94ac4ced450ca269e95cc8f2769131cd',
 'kh2_first.pkg': 'b977794bb340dc6c7fad486940af48a4',
 'kh2_fourth.pkg': 'd0b7b1417ffc4cc7cec75a878b115adb',
 'kh2_second.pkg': '832454c68a676022c106364c30601927',
 'kh2_sixth.pkg': 'b9c31aa7a3296b9b62d875787baf757f',
 'kh2_third.pkg': '55ce51115dd0587deb504f57b34d1c6e',
 'Recom.pkg': 'f05f21634ad3f14d1943abc16bb06183',
 'Theater.pkg': '1e08718a47d4aa0776931606e8fc9450'
}

import hashlib 

def validChecksum(path):
    pkgname = path.split(os.sep)[-1]
    if pkgname not in checksums:
        raise Exception("Error: PKG {} not found!".format(pkgname))
    checksum = hashlib.md5(open(path,'rb').read()).hexdigest()
    if not checksum == checksums[pkgname]:
        print("PKG {} has changed checksum!".format(pkgname))
        return False
    return True

@Gooey
def main_ui():
    main()

def main(cli_args: list = []):
    starttime = time.time()

    default_config = {
        "game": DEFAULTGAME,
        "openkh_path": "",
        "extracted_games_path": "",
        "khgame_path": "",
        "region": DEFAULTREGION
    }
    if os.path.exists("config.json"):
        default_config = json.load(open("config.json"))

    parser = GooeyParser()

    main_options = parser.add_argument_group(
        "Main options",
        "The main options around the mode and game to use. All required"
    )

    main_options.add_argument("-game", choices=list(games.keys()), default=default_config.get("game"), help="Which game to operate on", required=True)
    main_options.add_argument("-mode", choices=["patch", "extract"], default="patch", help="Which mode to run (patch patches the game, and extract just extracts the pkg files for the game, which must be done before running Mod Manager)", required=True)
    main_options.add_argument("-region", choices=["jp", "us", "uk", "it", "sp", "gr", "fr"], default=default_config.get("region", ""), help="defaults to 'us', needed to make sure the correct files are patched, as KH2FM PS2 mods use 'jp' as the region")


    main_options = parser.add_argument_group(
        "Setup",
        "Paths that must be configured to make sure the patcher works properly. patches_path is optional."
    )
    main_options.add_argument("-openkh_path", help="Path to openKH folder", default=default_config.get("openkh_path"), widget='DirChooser')
    main_options.add_argument("-extracted_games_path", help="Path to folder containing extracted games", default=default_config.get("extracted_games_path"), widget='DirChooser')
    main_options.add_argument("-khgame_path", help="Path to the kh_1.5_2.5 folder", default=default_config.get("khgame_path"), widget='DirChooser')
    main_options.add_argument("-patches_path", help="Path to directory containing other patches to apply. Will be applied in alphabetical order (with the mods manager 'mod' directory applied last). (optional)", default=default_config.get("patches_path"), widget='DirChooser')


    advanced_options = parser.add_argument_group(
        "Advanced Options",
        "Development options for the most part, if you don't know what these do then leave them alone."
    )
    advanced_options.add_argument("-keepkhbuild", action="store_true", default=False, help="Will keep the intermediate khbuild folder from being deleted after the patch is applied")
    advanced_options.add_argument("-ignorebadchecksum", action="store_true", default=False, help="If true, disabled backing up and restoring the original PKG files based on checksums (you probably don't want to check this option)")
    advanced_options.add_argument('-failonmissing', action="store_true", default=False, help="If true, fails when a file can't be patched to a PKG, rather than printing a warning")

    # Parse and print the results
    if cli_args:
        args = parser.parse_args(cli_args)

    config_to_write = {
        "game": args.game,
        "openkh_path": args.openkh_path,
        "extracted_games_path": args.extracted_games_path,
        "khgame_path": args.khgame_path,
        "region": args.region,
        "patches_path": args.patches_path
    }

    json.dump(config_to_write, open("config.json", "w"))

    MODDIR = os.path.join(args.openkh_path, "mod")
    PKGDIR = os.path.join(args.khgame_path, "Image", "en")
    IDXDIR =args.openkh_path
    IDXPATH = os.path.join(IDXDIR, "OpenKh.Command.IdxImg.exe")


    gamename = args.game
    if not args.game in games:
        raise Exception("Game not found, possible options: {}".format(list(games.keys())))
    if not os.path.exists(MODDIR):
        raise Exception("Mod dir not found")
    if not os.path.exists(PKGDIR):
        raise Exception("PKG dir not found")
    if not os.path.exists(IDXPATH):
        raise Exception("OpenKh.Command.IdxImg.exe not found")
    region = args.region
    game = games[gamename](region=region)
    mode = args.mode
    patch = True if mode == "patch" else False
    extract = True if mode == "extract" else False

    extra_patches_dir = args.patches_path or ''

    keepkhbuild = args.keepkhbuild
    validate_checksum = args.ignorebadchecksum
    ignoremissing = not args.failonmissing

    backup = True
    restore = True if patch else False

    pkgmap = json.load(open("pkgmap.json")).get(game.name)
    pkgmap_extras = json.load(open("pkgmap_extras.json")).get(game.name, {}) # predefined extras for patches that fail otherwise, such as GOA ROM
    pkgmap.update(pkgmap_extras)

    if extract:
        print("Extracting {}".format(game.name))
        if not os.path.exists(args.extracted_games_path):
            raise Exception("Path does not exist to extract games to! {}".format(args.extracted_games_path))
        pkglist = [os.path.join(PKGDIR,p) for p in os.listdir(PKGDIR) if game.name in p and p.endswith(".hed")]
        if os.path.exists("extractedout"):
            shutil.rmtree("extractedout")
        os.makedirs("extractedout")
        EXTRACTED_GAME_PATH = os.path.join(args.extracted_games_path, game.name)
        if os.path.exists(EXTRACTED_GAME_PATH):
            shutil.rmtree(EXTRACTED_GAME_PATH)
        for pkgfile in pkglist:
            if not validChecksum(pkgfile[:-4]+".pkg") and validate_checksum:
                raise Exception("Error: {} has an invalid checksum, please restore the original file!".format(pkgfile))
            idx_args = [IDXPATH, "hed", "extract", pkgfile, "-o", "extractedout"]
            print(IDXPATH, "hed", "extract", '"{}"'.format(pkgfile), "-o", '"{}"'.format("extractedout"))
            try:
                output = subprocess.check_output(idx_args, stderr=subprocess.STDOUT)
                print(output)
            except subprocess.CalledProcessError as err:
                output = err.output
                print(output.decode('utf-8'))
                raise Exception("Extract failed")
        original_path = os.path.join("extractedout", "original")
        remastered_path = os.path.join("extractedout", "remastered")
        shutil.move(remastered_path, os.path.join(original_path, "remastered"))
        shutil.move(original_path, args.extracted_games_path)
        os.rename(os.path.join(args.extracted_games_path, "original"), EXTRACTED_GAME_PATH)
    if backup:
        print("Backing up")
        if not os.path.exists("backup_pkgs"):
            os.makedirs("backup_pkgs")
        for pkg in game.pkgs:
            sourcefn = os.path.join(PKGDIR, pkg)
            newfn = os.path.join("backup_pkgs", pkg)
            if not os.path.exists(newfn):
                if not validChecksum(sourcefn) and validate_checksum :
                    raise Exception("Error: {} has an invalid checksum, please restore the original file and try again".format(sourcefn))
                shutil.copy(sourcefn, newfn)
                shutil.copy(sourcefn.split(".pkg")[0]+".hed", newfn.split(".pkg")[0]+".hed")
    if restore:
        print("Restoring from backup")
        if not os.path.exists("backup_pkgs"):
            raise Exception("Backup folder doesn't exist")
        for pkg in game.pkgs:
            newfn = os.path.join(PKGDIR, pkg)
            sourcefn = os.path.join("backup_pkgs", pkg)
            # The md5 takes too long to check so don't do it when restoring
            # if not validChecksum(sourcefn) and validate_checksum:
            #     raise Exception("Error: {} has an invalid checksum, please restore the original file and try again".format(sourcefn))
            shutil.copy(sourcefn, newfn)
            shutil.copy(sourcefn.split(".pkg")[0]+".hed", newfn.split(".pkg")[0]+".hed")
    if patch:
        print("Patching")
        if os.path.exists("khbuild"):
            shutil.rmtree("khbuild")
        os.makedirs("khbuild")
        for root, dirs, files in os.walk(MODDIR):
            path = root.split(os.sep)
            for file in files:
                fn = os.path.join(root, file)
                relfn = fn.replace(MODDIR, '')
                relfn_trans = game.translate_path(relfn)
                print("Translated Filename: {}".format(relfn_trans))
                pkgs = pkgmap.get(relfn_trans, "")
                if not pkgs:
                    print("WARNING: Could not find which pkg this path belongs: {} (original path {})".format(relfn_trans, relfn))
                    if not ignoremissing:
                        raise Exception("Exiting due to warning")
                    continue
                for pkg in pkgs:
                    newfn = os.path.join("khbuild", pkg, "original", relfn_trans)
                    new_basedir = os.path.dirname(newfn)
                    if not os.path.exists(new_basedir):
                        os.makedirs(new_basedir)
                    shutil.copy(fn, newfn)
        other_patches = []
        if extra_patches_dir and os.path.exists(extra_patches_dir):
            other_patches = [os.path.join(extra_patches_dir,p) for p in os.listdir(extra_patches_dir) if p.endswith(".kh2pcpatch")] #TODO double check extension
        zipped_files = {}
        for patch in sorted(other_patches):
            # Read the patch in as a zip, or extract it out to some temp dir
            # copy the files in based on the pkgmap
            input_zip=ZipFile(patch)
            for name in input_zip.namelist():
                zipped_files[name] = input_zip.read(name)
        for fn in zipped_files:
            if len(zipped_files[fn]) == 0:
                continue
            newfn = os.path.join("khbuild", fn)
            # mods manager needs to take priority
            if not os.path.exists(newfn): 
                new_basedir = os.path.dirname(newfn)
                if not os.path.exists(new_basedir):
                    os.makedirs(new_basedir)
                open(newfn, "wb").write(zipped_files[fn])
        for pkg in os.listdir("khbuild"):
            pkgfile = os.path.join(PKGDIR, pkg+".pkg")
            modfolder = os.path.join("khbuild", pkg)
            if not os.path.exists(os.path.join(modfolder, "remastered")):
                os.makedirs(os.path.join(modfolder, "remastered"))
            if os.path.exists("pkgoutput"):
                shutil.rmtree("pkgoutput")
            print("Patching: {}".format(pkg))
            args = [IDXPATH, "hed", "patch", pkgfile, modfolder, "-o", "pkgoutput"]
            #print(IDXPATH, "hed", "patch", '"{}"'.format(pkgfile), '"modfolder"', "-o", '"{}"'.format("pkgoutput"))
            try:
                print(args)
                output = subprocess.check_output(args, stderr=subprocess.STDOUT)
                print(output)
            except subprocess.CalledProcessError as err:
                output = err.output
                print(output.decode('utf-8'))
                raise Exception("Patch failed")
            shutil.copy(os.path.join("pkgoutput", pkg+".pkg"), os.path.join(PKGDIR, pkg+".pkg"))
            shutil.copy(os.path.join("pkgoutput", pkg+".hed"), os.path.join(PKGDIR, pkg+".hed"))
        if not keepkhbuild:
            shutil.rmtree("khbuild")
    print("All done! Took {}s".format(time.time()-starttime))

if __name__ == "__main__":
    main_ui()