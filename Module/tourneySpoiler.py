import shutil

from Module import hashimage
from Module.resources import resource_path


class TourneySeedSaver:

    def __init__(self, path_to_save, tourney_name):
        self.start_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<title>KH2FM Tourney Seed List - {tourney_name}</title>
<style>
    @font-face {{
        font-family: KHMenu;
        src: url("misc/KHMenu.otf") format("opentype");
    }}
    body {{
        font-family: KHMenu, sans-serif;
        background-color: #31363b;
        color: #ffffff;
        display: grid;
        place-items: center;
    }}
    .tourney-seed {{
        background-color: #001e3c;
        margin-top: 4px;
        margin-bottom: 4px;
        padding-left: 32px;
        padding-right: 32px;
        padding-bottom: 16px;
    }}
    .tourney-seed img {{
        vertical-align: middle;
    }}
    .tourney-seed a {{
        background-color: #31363b;
        color: #4dd0e1;
        margin-left: 32px;
        padding: 8px 12px;
        text-decoration: none;
        vertical-align: middle;
    }}
</style>
</head>
<body>
"""
        self.end_html = f"""
</body>
</html>
"""
        self.seed_strings = []
        self.seed_names = []
        self.path_to_save = path_to_save
        self.tourney_name = tourney_name

        self.seed_htmls = []

    def save(self):
        with open(self.path_to_save / f"{self.tourney_name}.html", "w") as outfile:
            outfile.write(self.start_html)
            for h in self.seed_htmls:
                outfile.write(h)
            outfile.write(self.end_html)

        misc_dir = self.path_to_save / "misc"
        misc_dir.mkdir()
        shutil.copy(resource_path("static/KHMenu.otf"), misc_dir)

    def add_seed(self, seed_string, settings, spoilers):
        self.seed_strings.append(seed_string)

        seed_filename = f"seed{len(self.seed_strings)}"
        self.seed_names.append(seed_filename)

        image_data = hashimage.generate_seed_hash_image(settings.seedHashIcons, use_bitmap=False)
        with open(self.path_to_save / f"{seed_filename}.png", "wb") as outfile:
            outfile.write(image_data)

        with open(self.path_to_save / f"{seed_filename}.html", "w") as outfile:
            outfile.write(spoilers)

        self._add_seed_html(seed_string=seed_string, seed_filename=seed_filename)

    def _add_seed_html(self, seed_string: str, seed_filename: str):
        self.seed_htmls.append(f"""
<div class="tourney-seed">
    <h2>Seed {len(self.seed_strings)}</h2>
    <h3>{seed_string}</h3>
    <img src="{seed_filename}.png">
    <a href="{seed_filename}.html">Spoiler Log</a>
</div>
""")
