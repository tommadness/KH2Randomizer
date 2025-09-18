import subprocess
from io import BytesIO
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QProgressDialog, QFileDialog, QWidget, QMessageBox

from Class.exceptions import RandomizerExceptions
from Class.seedSettings import SeedSettings, ExtraConfigurationData
from Module import appconfig
from Module.RandomizerSettings import RandomizerSettings
from Module.cosmeticsmods.keyblade import KeybladeRandomizer
from Module.generate import generateSeed, generateMultiWorldSeed
from Module.zipper import BossEnemyOnlyZip, CosmeticsOnlyZip, SeedZipResult
from UI.workers import BaseWorkerThread, BaseWorker


class GenerateModWorker(BaseWorker):

    def __init__(self, parent: QWidget):
        super().__init__()
        self.parent = parent

    @staticmethod
    def run_custom_cosmetics_executables(extra_data: ExtraConfigurationData):
        for custom_executable in extra_data.custom_cosmetics_executables:
            custom_file_path = Path(custom_executable)
            if custom_file_path.is_file():
                custom_cwd = custom_file_path.parent
                subprocess.call(custom_file_path, cwd=custom_cwd)

    def download_mod(self, zip_data: BytesIO, output_file_name: str, title: str):
        last_save_path = appconfig.read_last_save_path()
        if last_save_path is not None:
            output_file_name = str(last_save_path / output_file_name)

        save_widget = QFileDialog()
        filter_name = f"{title} (*.zip)"
        save_widget.setNameFilters([filter_name])
        outfile_name, _ = save_widget.getSaveFileName(self.parent, f"Save {title}", output_file_name, filter_name)
        if outfile_name != "":
            if not outfile_name.endswith(".zip"):
                outfile_name += ".zip"
            with open(outfile_name, "wb") as out_zip:
                out_zip.write(zip_data.getbuffer())
            appconfig.write_last_save_path(str(Path(outfile_name).parent))

    @staticmethod
    def display_emu_warnings(rando_settings: RandomizerSettings, extra_data: ExtraConfigurationData):
        if not extra_data.disable_emu_warning and rando_settings.keyblades_unlock_chests and extra_data.platform == "PCSX2":
            from UI import theme
            explainer_text = f'''You've generated a seed for PCSX2 with the setting for locking chests with keyblades. <br><br>
    This requires running the lua file included in the seed zip. This means, either move the lua file from the zip 
    (randoseed-mod-files/keyblade_locking/keyblade.lua) manually to your scripts folder, or reconfigure PCSX2 to use the folder made by the mod manager.<br><br>
    A tutorial to do so can be found here: <a href="LINK_HERE" style="color: {theme.LinkColor}">Tutorial</a><br><br>
    '''
            message = QMessageBox(text=explainer_text)
            message.setTextFormat(Qt.RichText)
            message.setWindowTitle("KH2 Seed Generator")
            message.exec()


class GenerateSeedThread(BaseWorkerThread):

    def __init__(self, rando_settings: RandomizerSettings, extra_data: ExtraConfigurationData):
        super().__init__()
        self.rando_settings = rando_settings
        self.extra_data = extra_data

    def do_work(self) -> SeedZipResult:
        extra_data = self.extra_data
        seed_zip_result = generateSeed(self.rando_settings, extra_data)
        GenerateModWorker.run_custom_cosmetics_executables(extra_data)
        return seed_zip_result


class GenerateSeedWorker(GenerateModWorker):

    def __init__(self, parent: QWidget, rando_settings: RandomizerSettings, extra_data: ExtraConfigurationData):
        super().__init__(parent)
        self.rando_settings = rando_settings
        self.extra_data = extra_data

    def create_worker_thread(self) -> BaseWorkerThread:
        return GenerateSeedThread(self.rando_settings, self.extra_data)

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog(
            label_text=f"Creating seed with name {self.rando_settings.random_seed}",
            title_text="Making your Seed, please wait...",
        )

    def handle_result(self, result: SeedZipResult):
        zip_data, _, _ = result
        self.download_mod(zip_data, output_file_name="randoseed.zip", title="Randomizer Seed")
        self.display_emu_warnings(self.rando_settings, self.extra_data)

    def handle_failure(self, failure: Exception):
        super().handle_failure(failure)
        if not isinstance(failure, RandomizerExceptions):
            raise failure


class GenerateMultiWorldSeedThread(BaseWorkerThread):

    def __init__(self, rando_settings: list[RandomizerSettings], extra_data: ExtraConfigurationData):
        super().__init__()
        self.rando_settings = rando_settings
        self.extra_data = extra_data

    def do_work(self) -> list[SeedZipResult]:
        extra_data = self.extra_data
        all_output = generateMultiWorldSeed(self.rando_settings, extra_data)
        GenerateModWorker.run_custom_cosmetics_executables(extra_data)
        return all_output


class GenerateMultiWorldSeedWorker(GenerateModWorker):

    def __init__(self, parent: QWidget, rando_settings: list[RandomizerSettings], extra_data: ExtraConfigurationData):
        super().__init__(parent)
        self.rando_settings = rando_settings
        self.extra_data = extra_data

    def create_worker_thread(self) -> BaseWorkerThread:
        return GenerateMultiWorldSeedThread(self.rando_settings, self.extra_data)

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog(
            label_text=f"Creating seed with name {self.rando_settings[0].random_seed}",
            title_text="Making your Seed, please wait...",
        )

    def handle_result(self, result: list[SeedZipResult]):
        for zip_data, _, _ in result:
            self.download_mod(zip_data, output_file_name="randoseed.zip", title="Randomizer Seed")

    def handle_failure(self, failure: Exception):
        super().handle_failure(failure)
        if not isinstance(failure, RandomizerExceptions):
            raise failure


class GenerateCosmeticsZipThread(BaseWorkerThread):

    def __init__(self, ui_settings: SeedSettings, extra_data: ExtraConfigurationData):
        super().__init__()
        self.ui_settings = ui_settings
        self.extra_data = extra_data

    def do_work(self) -> BytesIO:
        extra_data = self.extra_data
        zipper = CosmeticsOnlyZip(self.ui_settings)
        zip_data = zipper.create_zip()
        GenerateModWorker.run_custom_cosmetics_executables(extra_data)
        return zip_data


class CosmeticsZipWorker(GenerateModWorker):

    def __init__(self, parent: QWidget, ui_settings: SeedSettings, extra_data: ExtraConfigurationData):
        super().__init__(parent)
        self.ui_settings = ui_settings
        self.extra_data = extra_data

    def create_worker_thread(self) -> BaseWorkerThread:
        return GenerateCosmeticsZipThread(self.ui_settings, self.extra_data)

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog("Creating cosmetics-only mod")

    def handle_result(self, result: BytesIO):
        self.download_mod(result, output_file_name="randomized-cosmetics.zip", title="Cosmetics Mod")


class GenerateBossEnemyZipThread(BaseWorkerThread):

    def __init__(self, seed_name: str, ui_settings: SeedSettings, platform: str):
        super().__init__()
        self.ui_settings = ui_settings
        self.platform = platform
        self.seed_name = seed_name

    def do_work(self) -> BytesIO:
        platform = self.platform
        zipper = BossEnemyOnlyZip(self.seed_name, self.ui_settings, platform)
        zip_data = zipper.create_zip()
        return zip_data


class BossEnemyZipWorker(GenerateModWorker):

    def __init__(self, parent: QWidget, seed_name: str, ui_settings: SeedSettings, platform: str):
        super().__init__(parent)
        self.ui_settings = ui_settings
        self.platform = platform
        self.seed_name = seed_name

    def create_worker_thread(self) -> BaseWorkerThread:
        return GenerateBossEnemyZipThread(self.seed_name, self.ui_settings, self.platform)

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog("Creating boss/enemy-only mod")

    def handle_result(self, result: BytesIO):
        self.download_mod(result, output_file_name="randomized-bosses-enemies.zip", title="Boss/Enemy Mod")


class ExtractVanillaKeybladesThread(BaseWorkerThread):

    def do_work(self) -> Path:
        return KeybladeRandomizer.extract_game_models()


class ExtractVanillaKeybladesWorker(BaseWorker):

    def create_worker_thread(self) -> BaseWorkerThread:
        return ExtractVanillaKeybladesThread()

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog("Extracting vanilla keyblades")

    def handle_result(self, result: Path):
        message = QMessageBox(text=f"Extracted keyblades to [{str(result.absolute())}]")
        message.setWindowTitle("Keyblade Extraction")
        message.exec()


class ImportCustomKeybladesThread(BaseWorkerThread):

    def __init__(self, keyblade_file_paths: list[str]):
        super().__init__()
        self.keyblade_file_paths = keyblade_file_paths

    def do_work(self) -> int:
        count = len(self.keyblade_file_paths)
        if count > 0:
            for keyblade_file_path in self.keyblade_file_paths:
                KeybladeRandomizer.import_keyblade(keyblade_file_path)
        return count


class ImportCustomKeybladesWorker(BaseWorker):

    def __init__(self, keyblade_file_paths: list[str]):
        super().__init__()
        self.keyblade_file_paths = keyblade_file_paths

    def create_worker_thread(self) -> BaseWorkerThread:
        return ImportCustomKeybladesThread(self.keyblade_file_paths)

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog("Importing keyblade(s)")

    def handle_result(self, result: int):
        message = QMessageBox(text=f"Imported {result} keyblade(s).")
        message.setWindowTitle("Keyblade Import")
        message.exec()
