from typing import Callable, Any

from PySide6.QtWidgets import QLayout, QMessageBox, QPushButton


def button(text: str, onclick: Callable[[], Any]) -> QPushButton:
    widget = QPushButton(text=text)
    widget.clicked.connect(onclick)
    return widget


def show_alert(body: str, title: str = "KH2 Seed Generator"):
    message = QMessageBox(QMessageBox.NoIcon, title, body)
    message.exec()


def clear_layout(layout: QLayout):
    # Iterate in reverse to avoid issues with index changes during removal
    for i in reversed(range(layout.count())):
        layout_item = layout.itemAt(i)
        if layout_item.widget() is not None:
            widget_to_remove = layout_item.widget()
            layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)  # Remove the widget from its parent
            # Optionally, if the widget is no longer needed, schedule for deletion
            widget_to_remove.deleteLater()
