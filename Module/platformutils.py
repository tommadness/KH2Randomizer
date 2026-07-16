"""
Helpers for code that needs to behave differently across operating systems.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from Class.exceptions import GeneratorException


def is_windows() -> bool:
    return sys.platform == "win32"


def is_linux() -> bool:
    return sys.platform.startswith("linux")


def running_as_bundle() -> bool:
    """True when running from a PyInstaller bundle rather than from source."""
    return hasattr(sys, "_MEIPASS")


def appimage_path() -> Optional[Path]:
    """Path of the running AppImage (Linux only; set by the AppImage runtime)."""
    path = os.environ.get("APPIMAGE")
    return Path(path) if path else None


def no_window_flags() -> int:
    """subprocess creation flags that suppress a console window on Windows."""
    return subprocess.CREATE_NO_WINDOW if is_windows() else 0


def open_folder(path):
    """Opens a folder in the OS file manager."""
    from PySide6.QtCore import QUrl
    from PySide6.QtGui import QDesktopServices
    QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))


def prepare_qt_environment():
    """
    Call before creating the QApplication. On Linux, pick a platform theme (unless the
    user configured one) so file dialogs use the desktop's native file picker instead
    of Qt's built-in one, which inherits the app stylesheet. GTK-based desktops get the
    gtk3 theme, which talks to GTK directly and doesn't need the xdg-desktop-portal
    daemon; everything else goes through the portal.
    """
    if not is_linux() or os.environ.get("QT_QPA_PLATFORMTHEME"):
        return

    desktop = ":".join([
        os.environ.get("XDG_CURRENT_DESKTOP", ""),
        os.environ.get("DESKTOP_SESSION", ""),
    ]).lower()
    gtk_desktops = ("gnome", "cinnamon", "mate", "xfce", "unity", "budgie", "lxde")
    if any(name in desktop for name in gtk_desktops):
        os.environ["QT_QPA_PLATFORMTHEME"] = "gtk3"
    else:
        os.environ["QT_QPA_PLATFORMTHEME"] = "xdgdesktopportal"


def wine_available() -> bool:
    return shutil.which("wine") is not None


def ensure_windows_exe_runnable():
    """Raises a GeneratorException if Windows executables can't run on this system."""
    if not is_windows() and not wine_available():
        raise GeneratorException(
            "Running Windows tools (such as the OpenKH tools) on this system requires"
            " Wine, which was not found. Install wine using your distribution's package"
            " manager and try again."
        )


def windows_exe_command(exe_path, args: list) -> list:
    """
    Command list that runs a Windows executable on the current platform (natively on
    Windows, through wine elsewhere). Wine exposes absolute Unix paths via its Z:
    drive, so path arguments need no translation.
    """
    command = [str(exe_path)] + [str(arg) for arg in args]
    if is_windows():
        return command
    ensure_windows_exe_runnable()
    return ["wine"] + command


def fs_relative(data_path: str) -> Path:
    """Converts a backslash-separated archive-internal path to a relative Path."""
    return Path(data_path.replace("\\", "/"))
