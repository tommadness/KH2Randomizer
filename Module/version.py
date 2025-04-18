import os

LOCAL_UI_VERSION = '3.1.1-beta'
EXTRACTED_DATA_UPDATE_VERSION = "3.0.1"  # shouldn't need to update this often


def debug_mode() -> bool:
    return os.environ.get("SEED_GEN_DEBUG") == "true"
