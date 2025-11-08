import os
import shutil
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import QProgressDialog

from Module.cosmeticsmods.keyblademod import KeybladeMod, Kh1KeybladePack, BirthBySleepKeybladePack, \
    VanillaKeybladePack, PackagedKeyblade
from UI.qtlib import show_alert
from UI.workers import BaseWorkerThread, BaseWorker


class ExtractVanillaKeybladesThread(BaseWorkerThread):

    def do_work(self) -> Path:
        return VanillaKeybladePack.extract_vanilla_keyblades()


class ExtractVanillaKeybladesWorker(BaseWorker):

    def create_worker_thread(self) -> BaseWorkerThread:
        return ExtractVanillaKeybladesThread()

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog("Extracting vanilla keyblades")

    def handle_result(self, result: Path):
        show_alert(f"Extracted keyblades to [{str(result.absolute())}]", title="Keyblade Extraction")


class ImportCustomKeybladesThread(BaseWorkerThread):

    def __init__(self, keyblade_file_paths: list[Path]):
        super().__init__()
        self.keyblade_file_paths = keyblade_file_paths

    def do_work(self) -> int:
        count = len(self.keyblade_file_paths)
        if count > 0:
            for keyblade_file_path in self.keyblade_file_paths:
                PackagedKeyblade.import_keyblade(keyblade_file_path)
        return count


class ImportCustomKeybladesWorker(BaseWorker):

    def __init__(self, keyblade_file_paths: list[Path]):
        super().__init__()
        self.keyblade_file_paths = keyblade_file_paths

    def create_worker_thread(self) -> BaseWorkerThread:
        return ImportCustomKeybladesThread(self.keyblade_file_paths)

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog("Importing keyblade(s)")

    def handle_result(self, result: int):
        show_alert(f"Imported {result} keyblade(s).", title="Keyblade Import")


class ImportKh1KeybladePackThread(BaseWorkerThread):

    def do_work(self) -> Path:
        base_path = Path("cache", "kh1-keyblade-pack")
        Kh1KeybladePack.download_keyblade_pack(base_path)

        children = os.listdir(base_path)
        if len(children) == 1:
            pack_path = base_path / children[0]
        else:
            pack_path = base_path

        result = Kh1KeybladePack.import_keyblades(pack_path)
        shutil.rmtree(base_path)
        return result


class ImportKh1KeybladePackWorker(BaseWorker):

    def create_worker_thread(self) -> BaseWorkerThread:
        return ImportKh1KeybladePackThread()

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog("Importing keyblades")

    def handle_result(self, result: Path):
        show_alert(f"Imported keyblades to [{str(result.absolute())}]", title="Keyblade Import")


class ImportBirthBySleepKeybladePackThread(BaseWorkerThread):

    def do_work(self) -> Path:
        base_path = Path("cache", "birth-by-sleep-keyblade-pack")
        BirthBySleepKeybladePack.download_keyblade_pack(base_path)

        children = os.listdir(base_path)
        if len(children) == 1:
            pack_path = base_path / children[0]
        else:
            pack_path = base_path

        result = BirthBySleepKeybladePack.import_keyblades(pack_path)
        shutil.rmtree(base_path)
        return result


class ImportBirthBySleepKeybladePackWorker(BaseWorker):

    def create_worker_thread(self) -> BaseWorkerThread:
        return ImportBirthBySleepKeybladePackThread()

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog("Importing keyblades")

    def handle_result(self, result: Path):
        show_alert(f"Imported keyblades to [{str(result.absolute())}]", title="Keyblade Import")


class ImportModKeybladesThread(BaseWorkerThread):

    def __init__(self, mod: KeybladeMod):
        super().__init__()
        self.mod = mod

    def do_work(self) -> Path:
        return self.mod.import_keyblades()


class ImportModKeybladesWorker(BaseWorker):

    def __init__(self, mod: KeybladeMod):
        super().__init__()
        self.mod = mod

    def create_worker_thread(self) -> BaseWorkerThread:
        return ImportModKeybladesThread(self.mod)

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog("Importing keyblade(s)")

    def handle_result(self, result: Path):
        show_alert(f"Imported keyblade(s) to [{str(result.absolute())}]", title="Keyblade Import")
