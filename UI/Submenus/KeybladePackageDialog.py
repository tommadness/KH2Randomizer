import os
import shutil
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QFileDialog, QHBoxLayout, \
    QWidget

from Class.seedSettings import SeedSettings
from Module.cosmeticsmods.keyblade import KeybladeRandomizer
from UI.Submenus.SubMenu import KH2Submenu
from UI.qtlib import button, show_alert


class PackageKeybladeMenu(KH2Submenu):

    def _browse(self, field: QLineEdit, file_filter: str, directory: bool = False):
        file_dialog = QFileDialog(self)
        if directory:
            chosen_dir = file_dialog.getExistingDirectory()
            if chosen_dir is not None and chosen_dir != "":
                field.setText(chosen_dir)
        else:
            outfile_name, _ = file_dialog.getOpenFileName(self, filter=file_filter)
            if outfile_name is not None and outfile_name != "":
                field.setText(outfile_name)

    def _add_browseable(
            self,
            label_text: str,
            field: QLineEdit,
            tooltip: str,
            file_filter: str = "",
            directory: bool = False,
    ):
        hbox = QHBoxLayout()
        field.setFixedWidth(600)
        hbox.addWidget(field)
        hbox.addWidget(button("Browse", lambda: self._browse(field, file_filter, directory)))
        wrapper = QWidget()
        wrapper.setLayout(hbox)
        self.add_labeled_widget(wrapper, label_text, tooltip)

    def __init__(self, settings: SeedSettings):
        super().__init__("Package", settings)

        key_name = QLineEdit("")
        key_name.setFixedWidth(600)
        self.key_name = key_name

        author = QLineEdit("")
        author.setFixedWidth(600)
        self.author = author

        source = QLineEdit("")
        source.setFixedWidth(600)
        self.source = source

        remastered_itempic = QLineEdit()
        self.remastered_itempic = remastered_itempic
        original_itempic = QLineEdit()
        self.original_itempic = original_itempic

        self.mdlx_fields = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.remastered_texture_fields = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.fx_fields = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.remastered_fx_fields = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        self.sound_fields = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]

        self.start_column()

        self.start_group()
        self.add_labeled_widget(key_name, "Keyblade Name*", tooltip="Name of the keyblade (required).")
        self.add_labeled_widget(author, "Author", tooltip="Author/designer for attribution (included in metadata).")
        self.add_labeled_widget(source, "Source", tooltip="Link to the source for the keyblade assets, if any.")
        self.end_group("Basic")

        self.start_group()
        self._add_browseable(
            "Remastered (.dds)*",
            remastered_itempic,
            tooltip="Location of the image to use as the keyblade's remastered item picture (in .dds format).",
            file_filter="Remastered (*.dds)"
        )
        self._add_browseable(
            "Original (.imd)",
            original_itempic,
            tooltip="""
            Location of the image to use as the keyblade's non-remastered item picture (in .imd format).
            
            (The non-remastered itempic is ignored for PC/remastered, but these are allowed to be packaged in the
            keyblade format.)
            """,
            file_filter="Itempic (*.imd)"
        )
        self.end_group("Item Picture")

        self.start_group()
        self._add_browseable(
            "Base*",
            self.mdlx_fields[0],
            tooltip=".mdlx file containing the default model and texture (required).",
            file_filter="MDLX (*.mdlx)"
        )
        self._add_browseable(
            "Halloween Town (_NM)",
            self.mdlx_fields[1],
            tooltip="Optional .mdlx file containing the Halloween Town specific model and texture (if any).",
            file_filter="MDLX (*.mdlx)"
        )
        self._add_browseable(
            "Space Paranoids (_TR)",
            self.mdlx_fields[2],
            tooltip="Optional .mdlx file containing the Space Paranoids specific model and texture (if any).",
            file_filter="MDLX (*.mdlx)"
        )
        self._add_browseable(
            "Timeless River (_WI)",
            self.mdlx_fields[3],
            tooltip="Optional .mdlx file containing the Timeless River specific model and texture (if any).",
            file_filter="MDLX (*.mdlx)"
        )
        self.end_group("Models (.mdlx)")

        self.start_group()
        self._add_browseable(
            "Base*",
            self.remastered_texture_fields[0],
            tooltip="Folder containing the default remastered textures in .dds format (required).",
            directory=True
        )
        self._add_browseable(
            "Halloween Town (_NM)",
            self.remastered_texture_fields[1],
            tooltip="Folder containing the Halloween Town specific remastered textures in .dds format (if any).",
            directory=True
        )
        self._add_browseable(
            "Space Paranoids (_TR)",
            self.remastered_texture_fields[2],
            tooltip="Folder containing the Space Paranoids specific remastered textures in .dds format (if any).",
            directory=True
        )
        self._add_browseable(
            "Timeless River (_WI)",
            self.remastered_texture_fields[3],
            tooltip="Folder containing the Timeless River specific remastered textures in .dds format (if any).",
            directory=True
        )
        self.end_group("Remastered Texture Folders (.mdlx)")

        self.start_group()
        self._add_browseable(
            "Base",
            self.fx_fields[0],
            tooltip=".a.us file containing the default keyblade effects.",
            file_filter="Effects (*.us)"
        )
        self._add_browseable(
            "Halloween Town (_NM)",
            self.fx_fields[1],
            tooltip=".a.us file containing the Halloween Town specific keyblade effects (if any).",
            file_filter="Effects (*.us)"
        )
        self._add_browseable(
            "Space Paranoids (_TR)",
            self.fx_fields[2],
            tooltip=".a.us file containing the Space Paranoids specific keyblade effects (if any).",
            file_filter="Effects (*.us)"
        )
        self._add_browseable(
            "Timeless River (_WI)",
            self.fx_fields[3],
            tooltip=".a.us file containing the Timeless River specific keyblade effects (if any).",
            file_filter="Effects (*.us)"
        )
        self.end_group("Effects (.a.us) (Optional)")

        self.start_group()
        self._add_browseable(
            "Base",
            self.remastered_fx_fields[0],
            tooltip="Folder containing the default remastered effects in .dds format.",
            directory=True
        )
        self._add_browseable(
            "Halloween Town (_NM)",
            self.remastered_fx_fields[1],
            tooltip="Folder containing the Halloween Town specific remastered effects in .dds format (if any).",
            directory=True
        )
        self._add_browseable(
            "Space Paranoids (_TR)",
            self.remastered_fx_fields[2],
            tooltip="Folder containing the Space Paranoids specific remastered effects in .dds format (if any).",
            directory=True
        )
        self._add_browseable(
            "Timeless River (_WI)",
            self.remastered_fx_fields[3],
            tooltip="Folder containing the Timeless River specific remastered effects in .dds format (if any).",
            directory=True
        )
        self.end_group("Remastered Effects Folders (.a.us) (Optional)")

        self.start_group()
        self._add_browseable(
            "Base",
            self.sound_fields[0],
            tooltip="The default sound effect file (usually named something like se503)."
        )
        self._add_browseable(
            "Halloween Town (_NM)",
            self.sound_fields[1],
            tooltip="The Halloween Town specific sound effect file (if any) (usually named something like se503)."
        )
        self._add_browseable(
            "Space Paranoids (_TR)",
            self.sound_fields[2],
            tooltip="The Space Paranoids specific sound effect file (if any) (usually named something like se503)."
        )
        self._add_browseable(
            "Timeless River (_WI)",
            self.sound_fields[3],
            tooltip="The Timeless River specific sound effect file (if any) (usually named something like se503)."
        )
        self.end_group("Remastered Sounds (se###) (Optional)")

        self.start_group()
        self.pending_group.addWidget(button("Package Keyblade", self._package_keyblade))
        self.end_group()

        self.end_column()

        self.finalizeMenu()

    def _validate(self) -> Optional[str]:
        if self.key_name.text() == "":
            return "Keyblade name is required"
        if self.remastered_itempic.text() == "":
            return "Remastered item picture is required"
        if self.mdlx_fields[0].text() == "":
            return "Base model is required"
        if self.remastered_texture_fields[0].text() == "":
            return "Base remastered textures folder is required"
        return None

    def _package_keyblade(self):
        validation = self._validate()
        if validation is not None:
            show_alert(validation, title="Package Keyblade")
            return

        key_name = self.key_name.text()

        staging_path = Path(f"cache/staging-keyblades").absolute()
        staging_path.mkdir(parents=True, exist_ok=True)

        try:
            KeybladeRandomizer.extract_keyblade(
                keyblade_name=key_name,
                author=self.author.text(),
                source=self.source.text(),
                output_path=staging_path,
                original_itempic=Path(self.original_itempic.text()),
                remastered_itempic=Path(self.remastered_itempic.text()),
                mdlx_files=[Path(field.text()) for field in self.mdlx_fields],
                remastered_mdlx_folders=[Path(field.text()) for field in self.remastered_texture_fields],
                fx_files=[Path(field.text()) for field in self.fx_fields],
                remastered_fx_folders=[Path(field.text()) for field in self.remastered_fx_fields],
                remastered_sound_files=[Path(field.text()) for field in self.sound_fields],
            )
        except Exception as error:
            show_alert(str(repr(error)), title="Package Keyblade")
            return

        packaged_path = Path(f"cache/packaged-keyblades").absolute()
        packaged_path.mkdir(parents=True, exist_ok=True)

        zip_path = packaged_path / key_name
        packaged_file = f"{zip_path}.kh2randokb"
        archive = shutil.make_archive(str(zip_path), "zip", staging_path / key_name)
        os.rename(archive, packaged_file)
        shutil.rmtree(staging_path)

        show_alert(f"Created [{packaged_file}].", title="Package Keyblade")


class KeybladePackageDialog(QDialog):

    def __init__(self, parent: QWidget, settings: SeedSettings):
        super().__init__(parent)
        self.setWindowTitle("Package External Keyblade")

        vbox = QVBoxLayout()
        vbox.addWidget(PackageKeybladeMenu(settings))

        self.setLayout(vbox)
        self.setMinimumWidth(1200)
        self.setMinimumHeight(800)
