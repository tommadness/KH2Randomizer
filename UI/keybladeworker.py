from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import QProgressDialog

from Module.cosmeticsmods.keyblade import KeybladeRandomizer
from UI.qtlib import show_alert
from UI.workers import BaseWorkerThread, BaseWorker


class ExtractVanillaKeybladesThread(BaseWorkerThread):

    def do_work(self) -> Path:
        return KeybladeRandomizer.extract_game_models()


class ExtractVanillaKeybladesWorker(BaseWorker):

    def create_worker_thread(self) -> BaseWorkerThread:
        return ExtractVanillaKeybladesThread()

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return self.basic_wait_dialog("Extracting vanilla keyblades")

    def handle_result(self, result: Path):
        show_alert(f"Extracted keyblades to [{str(result.absolute())}]", title="Keyblade Extraction")


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
        show_alert(f"Imported {result} keyblade(s).", title="Keyblade Import")
