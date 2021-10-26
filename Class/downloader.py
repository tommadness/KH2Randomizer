class Downloader():

    openKHDownload = {
        "name":"OpenKH Mods Manager",
        "url": "https://github.com/Xeeynamo/OpenKh/releases"
    }

    def __init__(self, url):
        self.url = url

    def downloadZip(self, path):
        print("Download {url} to {path}".format(url=self.url, path=path))