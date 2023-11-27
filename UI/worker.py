import io
import subprocess
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtWidgets import QProgressDialog, QFileDialog, QWidget, QMessageBox

from Class.exceptions import RandomizerExceptions
from Class.seedSettings import SeedSettings, ExtraConfigurationData
from Module import appconfig
from Module.RandomizerSettings import RandomizerSettings
from Module.generate import generateSeed, generateMultiWorldSeed
from Module.zipper import BossEnemyOnlyZip, CosmeticsOnlyZip, SeedZipResult


def _run_custom_cosmetics_executables(extra_data: ExtraConfigurationData):
    for custom_executable in extra_data.custom_cosmetics_executables:
        custom_file_path = Path(custom_executable)
        if custom_file_path.is_file():
            custom_cwd = custom_file_path.parent
            subprocess.call(custom_file_path, cwd=custom_cwd)


def _wrap_in_last_seed_folder_if_possible(last_seed_folder_txt: Path, output_file_name: str) -> str:
    if last_seed_folder_txt.is_file():
        last_seed_folder = Path(last_seed_folder_txt.read_text().strip())
        if last_seed_folder.is_dir():
            output_file_name = str(last_seed_folder / output_file_name)
    return output_file_name


def _download_seed(parent: QWidget, seed_zip_result: SeedZipResult):
    zip_file, _, _ = seed_zip_result

    last_seed_folder_txt = appconfig.auto_save_folder() / 'last_seed_folder.txt'
    output_file_name = _wrap_in_last_seed_folder_if_possible(last_seed_folder_txt, 'randoseed.zip')

    save_widget = QFileDialog()
    filter_name = "KH2 Randomizer Seed (*.zip)"
    save_widget.setNameFilters([filter_name])
    outfile_name, _ = save_widget.getSaveFileName(parent, "Save Seed", output_file_name, filter_name)
    if outfile_name != "":
        if not outfile_name.endswith(".zip"):
            outfile_name += ".zip"
        with open(outfile_name, "wb") as out_zip:
            out_zip.write(zip_file.getbuffer())

        last_seed_folder_txt.write_text(str(Path(outfile_name).parent))


class GenerateSeedThread(QThread):
    finished = Signal(object)
    failed = Signal(Exception)

    def __init__(self, rando_settings: RandomizerSettings, extra_data: ExtraConfigurationData):
        super().__init__()
        self.rando_settings = rando_settings
        self.extra_data = extra_data

    def run(self):
        try:
            extra_data = self.extra_data
            seed_zip_result = generateSeed(self.rando_settings, extra_data)

            _run_custom_cosmetics_executables(extra_data)

            self.finished.emit(seed_zip_result)
        except Exception as e:
            self.failed.emit(e)


class GenerateSeedWorker:

    def __init__(self, parent: QWidget, rando_settings: RandomizerSettings, extra_data: ExtraConfigurationData):
        self.parent = parent
        self.rando_settings = rando_settings
        self.extra_data = extra_data
        self.progress: Optional[QProgressDialog] = None
        self.thread: Optional[GenerateCosmeticsZipThread] = None

    def generate_seed(self):
        rando_settings = self.rando_settings
        displayed_seed_name = rando_settings.random_seed
        self.progress = QProgressDialog(f"Creating seed with name {displayed_seed_name}", "Cancel", 0, 0, None)
        self.progress.setWindowTitle("Making your Seed, please wait...")
        # self.progress.setCancelButton(None)
        self.progress.setModal(True)
        self.progress.show()

        self.thread = GenerateSeedThread(rando_settings, self.extra_data)
        self.thread.finished.connect(self._handle_result)
        self.thread.failed.connect(self._handle_failure)
        self.progress.canceled.connect(lambda: self.thread.terminate())
        self.thread.start()

    def _handle_result(self, seed_zip_result: SeedZipResult):
        self.progress.close()
        self.progress = None
        zip_file, spoiler_log_output, enemy_log_output = seed_zip_result
        spoiler_log_output = spoiler_log_output if spoiler_log_output else "<html>No spoiler log generated</html>"
        _download_seed(self.parent, (zip_file, spoiler_log_output, enemy_log_output))
        self.thread = None

    def _handle_failure(self, failure: Exception):
        if self.progress is not None:
            self.progress.close()
        self.progress = None
        message = QMessageBox(text=str(repr(failure)))
        message.setTextInteractionFlags(Qt.TextSelectableByMouse)
        message.setWindowTitle("Seed Generation Error")
        message.exec()
        self.thread = None
        if not isinstance(failure, RandomizerExceptions):
            raise failure


class GenerateMultiWorldSeedThread(QThread):
    finished = Signal(object)
    failed = Signal(Exception)

    def __init__(self, rando_settings: list[RandomizerSettings], extra_data: ExtraConfigurationData):
        super().__init__()
        self.rando_settings = rando_settings
        self.extra_data = extra_data

    def run(self):
        try:
            extra_data = self.extra_data
            all_output = generateMultiWorldSeed(self.rando_settings, extra_data)

            _run_custom_cosmetics_executables(extra_data)

            self.finished.emit(all_output)
        except Exception as e:
            self.failed.emit(e)


class GenerateMultiWorldSeedWorker:

    def __init__(self, parent: QWidget, rando_settings: list[RandomizerSettings], extra_data: ExtraConfigurationData):
        self.parent = parent
        self.rando_settings = rando_settings
        self.extra_data = extra_data
        self.progress: Optional[QProgressDialog] = None
        self.thread: Optional[GenerateMultiWorldSeedThread] = None

    def generate_seed(self):
        rando_settings = self.rando_settings
        displayed_seed_name = rando_settings[0].random_seed
        self.progress = QProgressDialog(f"Creating seed with name {displayed_seed_name}", "Cancel", 0, 0, None)
        self.progress.setWindowTitle("Making your Seed, please wait...")
        # self.progress.setCancelButton(None)
        self.progress.setModal(True)
        self.progress.show()

        self.thread = GenerateMultiWorldSeedThread(rando_settings, self.extra_data)
        self.thread.finished.connect(self._handle_result)
        self.thread.failed.connect(self._handle_failure)
        self.progress.canceled.connect(lambda: self.thread.terminate())
        self.thread.start()

    def _handle_result(self, seed_zip_result: SeedZipResult):
        self.progress.close()
        self.progress = None
        for zip_file, spoiler_log_output, enemy_log_output in seed_zip_result:
            spoiler_log_output = spoiler_log_output if spoiler_log_output else "<html>No spoiler log generated</html>"
            _download_seed(self.parent, (zip_file, spoiler_log_output, enemy_log_output))
        self.thread = None

    def _handle_failure(self, failure: Exception):
        if self.progress is not None:
            self.progress.close()
        self.progress = None
        message = QMessageBox(text=str(repr(failure)))
        message.setTextInteractionFlags(Qt.TextSelectableByMouse)
        message.setWindowTitle("Seed Generation Error")
        message.exec()
        self.thread = None
        if not isinstance(failure, RandomizerExceptions):
            raise failure


class GenerateCosmeticsZipThread(QThread):
    finished = Signal(object)
    failed = Signal(Exception)

    def __init__(self, ui_settings: SeedSettings, extra_data: ExtraConfigurationData):
        super().__init__()
        self.ui_settings = ui_settings
        self.extra_data = extra_data

    def run(self):
        try:
            extra_data = self.extra_data
            zipper = CosmeticsOnlyZip(self.ui_settings, extra_data)
            zip_file = zipper.create_zip()

            _run_custom_cosmetics_executables(extra_data)

            self.finished.emit(zip_file)
        except Exception as e:
            self.failed.emit(e)


class CosmeticsZipWorker:

    def __init__(self, parent: QWidget, ui_settings: SeedSettings, extra_data: ExtraConfigurationData):
        self.parent = parent
        self.ui_settings = ui_settings
        self.extra_data = extra_data
        self.progress: Optional[QProgressDialog] = None
        self.thread: Optional[GenerateCosmeticsZipThread] = None

    def generate_mod(self):
        self.progress = QProgressDialog("Creating cosmetics-only mod", "Cancel", 0, 0, None)
        self.progress.setWindowTitle("Please wait...")
        self.progress.setModal(True)
        self.progress.show()

        self.thread = GenerateCosmeticsZipThread(self.ui_settings, self.extra_data)
        self.thread.finished.connect(self._handle_result)
        self.thread.failed.connect(self._handle_failure)
        self.progress.canceled.connect(lambda: self.thread.terminate())
        self.thread.start()

    def _handle_result(self, zip_file: io.BytesIO):
        self.progress.close()
        self.progress = None
        self._download_zip(zip_file)
        self.thread = None

    def _handle_failure(self, failure: Exception):
        if self.progress is not None:
            self.progress.close()
        self.progress = None

        message = QMessageBox(text=str(repr(failure)))
        message.setTextInteractionFlags(Qt.TextSelectableByMouse)
        message.setWindowTitle("Cosmetics Generation Error")
        message.exec()

        self.thread = None

    def _download_zip(self, zip_file: io.BytesIO):
        last_seed_folder_txt = appconfig.auto_save_folder() / 'last_seed_folder.txt'
        output_file_name = _wrap_in_last_seed_folder_if_possible(last_seed_folder_txt, 'randomized-cosmetics.zip')

        save_widget = QFileDialog()
        filter_name = "OpenKH Mod (*.zip)"
        save_widget.setNameFilters([filter_name])
        outfile_name, _ = save_widget.getSaveFileName(self.parent, "Save Cosmetics Mod", output_file_name, filter_name)
        if outfile_name != "":
            if not outfile_name.endswith(".zip"):
                outfile_name += ".zip"
            with open(outfile_name, "wb") as out_zip:
                out_zip.write(zip_file.getbuffer())


class GenerateBossEnemyZipThread(QThread):
    finished = Signal(object)
    failed = Signal(Exception)

    def __init__(self, seed_name: str, ui_settings: SeedSettings, platform: str):
        super().__init__()
        self.ui_settings = ui_settings
        self.platform = platform
        self.seed_name = seed_name

    def run(self):
        try:
            platform = self.platform
            zipper = BossEnemyOnlyZip(self.seed_name, self.ui_settings, platform)
            zip_file = zipper.create_zip()
            self.finished.emit(zip_file)
        except Exception as e:
            self.failed.emit(e)


class BossEnemyZipWorker:

    def __init__(self, parent: QWidget, seed_name: str, ui_settings: SeedSettings, platform: str):
        self.parent = parent
        self.ui_settings = ui_settings
        self.platform = platform
        self.seed_name = seed_name
        self.progress: Optional[QProgressDialog] = None
        self.thread: Optional[GenerateBossEnemyZipThread] = None

    def generate_mod(self):
        self.progress = QProgressDialog("Creating boss/enemy-only mod", "Cancel", 0, 0, None)
        self.progress.setWindowTitle("Please wait...")
        self.progress.setModal(True)
        self.progress.show()

        self.thread = GenerateBossEnemyZipThread(self.seed_name, self.ui_settings, self.platform)
        self.thread.finished.connect(self._handle_result)
        self.thread.failed.connect(self._handle_failure)
        self.progress.canceled.connect(lambda: self.thread.terminate())
        self.thread.start()

    def _handle_result(self, zip_file: io.BytesIO):
        self.progress.close()
        self.progress = None
        self._download_zip(zip_file)
        self.thread = None

    def _handle_failure(self, failure: Exception):
        if self.progress is not None:
            self.progress.close()
        self.progress = None

        message = QMessageBox(text=str(repr(failure)))
        message.setTextInteractionFlags(Qt.TextSelectableByMouse)
        message.setWindowTitle("Boss/Enemy Generation Error")
        message.exec()

        self.thread = None

    def _download_zip(self, zip_file: io.BytesIO):
        last_seed_folder_txt = appconfig.auto_save_folder() / 'last_seed_folder.txt'
        output_file_name = _wrap_in_last_seed_folder_if_possible(last_seed_folder_txt, 'randomized-bosses-enemies.zip')

        save_widget = QFileDialog()
        filter_name = "OpenKH Mod (*.zip)"
        save_widget.setNameFilters([filter_name])
        outfile_name, _ = save_widget.getSaveFileName(self.parent, "Save boss/enemy mod", output_file_name, filter_name)
        if outfile_name != "":
            if not outfile_name.endswith(".zip"):
                outfile_name += ".zip"
            with open(outfile_name, "wb") as out_zip:
                out_zip.write(zip_file.getbuffer())