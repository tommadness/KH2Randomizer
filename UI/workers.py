from typing import Any, Optional

from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QProgressDialog, QMessageBox


class BaseWorkerThread(QThread):
    """Base class for worker threads. Override do_work() to specify the work to perform."""
    finished = Signal(object)
    failed = Signal(Exception)

    def run(self):
        try:
            result = self.do_work()
            self.finished.emit(result)
        except Exception as e:
            self.failed.emit(e)

    def do_work(self) -> Any:
        raise Exception("do_work() not implemented")


class BaseWorker(QObject):
    """
    Base class for worker objects. Override create_worker_thread() to create a worker thread. There are other methods
    that can optionally be overridden to further customize behavior.
    """
    finished = Signal(object)
    failed = Signal(Exception)

    def __init__(self):
        super().__init__()
        self.progress: Optional[QProgressDialog] = None
        self.thread: Optional[BaseWorkerThread] = None

    def start(self):
        """Creates and starts the worker thread, displaying a progress dialog if configured to do so."""
        progress = self.create_progress_dialog()
        self.progress = progress
        if progress is not None:
            progress.setModal(True)
            progress.show()

        thread = self.create_worker_thread()
        self.thread = thread
        thread.finished.connect(self._internal_handle_result)
        thread.failed.connect(self._internal_handle_failure)

        if progress is not None:
            # Not sure why, but a lambda seems to be needed here instead of just a reference
            progress.canceled.connect(lambda: self._internal_handle_cancel())

        thread.start()

    def create_worker_thread(self) -> BaseWorkerThread:
        raise Exception("create_worker_thread() not implemented")

    def create_progress_dialog(self) -> Optional[QProgressDialog]:
        return None

    def handle_result(self, result: Any):
        pass

    def handle_failure(self, failure: Exception):
        message = QMessageBox(text=str(repr(failure)))
        message.setTextInteractionFlags(Qt.TextSelectableByMouse)
        message.setWindowTitle("Error")
        message.exec()

    def _internal_handle_result(self, result: Any):
        self.thread = None

        if self.progress is not None:
            self.progress.close()
            self.progress = None

        try:
            self.handle_result(result)
        finally:
            self.finished.emit(result)

    def _internal_handle_failure(self, failure: Exception):
        self.thread = None

        if self.progress is not None:
            self.progress.close()
            self.progress = None

        try:
            self.handle_failure(failure)
        finally:
            self.failed.emit(failure)

    def _internal_handle_cancel(self):
        thread = self.thread
        if thread is not None:
            thread.terminate()

    @staticmethod
    def basic_wait_dialog(
            label_text: str,
            title_text: str = "Please wait...",
            cancel_text: str = "Cancel",
    ) -> QProgressDialog:
        """Creates a basic progress dialog with some reasonable defaults."""
        progress = QProgressDialog(label_text, cancel_text, 0, 0, None)
        progress.setWindowTitle(title_text)
        return progress
