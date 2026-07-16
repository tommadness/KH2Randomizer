import subprocess
from pathlib import Path

from Class.exceptions import GeneratorException
from Module import appconfig, platformutils


class BinaryArchiver:
    """
    Can pack and unpack KH2 binary archive files using OpenKH tools. See https://openkh.dev/kh2/file/type/bar.html.
    """

    def __init__(self):
        super().__init__()

        openkh_path = appconfig.read_openkh_path()
        if openkh_path is None:
            raise GeneratorException("No OpenKH path configured.")

        bar_exe = openkh_path / "OpenKh.Command.Bar.exe"
        if not bar_exe.is_file():
            raise GeneratorException("No OpenKh.Command.Bar.exe found.")

        platformutils.ensure_windows_exe_runnable()

        self.bar_exe = bar_exe

    def extract_bar(self, bar_file: Path, destination: Path):
        """
        Unpacks the contents of bar_file to the destination directory. Creates the destination directory if needed
        """
        destination.mkdir(parents=True, exist_ok=True)
        # -o specifies the output location
        args = platformutils.windows_exe_command(self.bar_exe, ["unpack", "-o", destination, bar_file])
        subprocess.call(args, creationflags=platformutils.no_window_flags())

    def create_bar(self, bar_json_file: Path, destination: Path):
        """Packs a BAR file to the destination file from a JSON "project file"."""
        # -o specifies the output location
        args = platformutils.windows_exe_command(self.bar_exe, ["pack", "-o", destination, bar_json_file])
        subprocess.call(args, creationflags=platformutils.no_window_flags())
