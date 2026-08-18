import sys
from typing import Optional, IO


class Logger:

    def __init__(self, orig_stream: Optional[IO[str]]):
        self.filename = "log.txt"
        self.orig_stream = orig_stream

    def write(self, data):
        data_str = str(data)

        with open(self.filename, "a") as f:
            f.write(data_str)

        stream = self.orig_stream
        if stream is not None:
            stream.write(data_str)

    def flush(self):
        stream = self.orig_stream
        if stream is not None:
            stream.flush()


def initialize_logging():
    logger = Logger(sys.stdout)
    sys.stdout = logger
    sys.stderr = logger
