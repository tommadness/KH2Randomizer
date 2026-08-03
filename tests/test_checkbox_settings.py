from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from UI.Submenus.SubMenu import KH2Submenu


class _Settings:
    def __init__(self):
        self.value = True

    def get(self, name):
        return self.value

    def set(self, name, value):
        self.value = value


def test_checkbox_uses_boolean_toggle_value():
    app = QApplication.instance() or QApplication([])
    settings = _Settings()

    checkbox = KH2Submenu.make_check_box_for_settings(settings, "example")
    assert checkbox.checkState() == Qt.Checked
    assert settings.value is True

    checkbox.setChecked(False)
    assert settings.value is False
    assert isinstance(settings.value, bool)
    app.processEvents()
