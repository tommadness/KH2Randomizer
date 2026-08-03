from pathlib import Path

from UI.GithubInfo import releaseInfo


def _release(assets):
    return {
        "body": "notes",
        "prerelease": False,
        "draft": False,
        "tag_name": "v9.0.0",
        "assets": assets,
    }


def _asset(name, url="https://example.invalid/download"):
    return {"name": name, "browser_download_url": url, "updated_at": "now"}


def test_linux_release_selects_only_exact_appimage(monkeypatch):
    monkeypatch.setattr(releaseInfo.platformutils, "is_windows", lambda: False)
    info = releaseInfo.GithubReleaseInfo(_release([
        _asset("other.AppImage", "wrong"),
        _asset(releaseInfo.LINUX_ASSET_NAME, "correct"),
    ]))

    assert info.download_link == "correct"


def test_duplicate_platform_assets_are_rejected(monkeypatch):
    monkeypatch.setattr(releaseInfo.platformutils, "is_windows", lambda: False)
    info = releaseInfo.GithubReleaseInfo(_release([
        _asset(releaseInfo.LINUX_ASSET_NAME, "first"),
        _asset(releaseInfo.LINUX_ASSET_NAME, "second"),
    ]))

    assert info.download_link is None


class _Progress:
    def __init__(self, *args, **kwargs):
        self.closed = False

    def setWindowTitle(self, title):
        pass

    def setModal(self, modal):
        pass

    def show(self):
        pass

    def setValue(self, value):
        pass

    def close(self):
        self.closed = True


class _Message:
    def __init__(self, *args, **kwargs):
        pass

    def setWindowTitle(self, title):
        pass

    def exec(self):
        pass


class _Response:
    headers = {"Content-Length": "10"}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def raise_for_status(self):
        pass

    def iter_content(self, chunk_size):
        yield b"short"


def test_truncated_download_does_not_replace_target(monkeypatch, tmp_path):
    target = tmp_path / releaseInfo.LINUX_ASSET_NAME
    target.write_bytes(b"original")
    monkeypatch.setattr(releaseInfo, "update_install_target", lambda: target)
    monkeypatch.setattr(releaseInfo, "QProgressDialog", _Progress)
    monkeypatch.setattr(releaseInfo, "QMessageBox", _Message)
    monkeypatch.setattr(releaseInfo.requests, "get", lambda *args, **kwargs: _Response())
    monkeypatch.setattr(releaseInfo.platformutils, "is_windows", lambda: False)
    info = releaseInfo.GithubReleaseInfo(_release([_asset(releaseInfo.LINUX_ASSET_NAME)]))

    assert info.download_release() is False
    assert target.read_bytes() == b"original"
    assert not Path(str(target) + ".tmp").exists()
