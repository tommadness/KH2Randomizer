from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget

from Module.resources import resource_path


class LuaBackendSetupDialog(QDialog):

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)

        self.setMinimumHeight(160)
        self.setWindowTitle("LuaBackend Hook Setup")
        self.setWindowIcon(QIcon(resource_path("Module/icon.png")))

        information_text = f"""
        LuaBackend Hook setup has moved to the OpenKH Mods Manager setup wizard.<br>
        See the setup guide on the randomizer website for more information.
        """
        message = QLabel(information_text)
        message.setTextFormat(Qt.RichText)

        layout = QVBoxLayout()
        layout.addWidget(message)
        self.setLayout(layout)
