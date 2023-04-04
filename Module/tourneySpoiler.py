from Module import hashimage


class TourneySeedSaver:

    def __init__(self, path_to_save, tourney_name):
        self.start_html = f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>KH2FM Tourney Seed List - {tourney_name}</title>
    <script>
    </script>
</head>
<style>
<style>
    @font-face {{
        font-family: KHMenu;
        src: url("KHMenu.otf") format("opentype");
    }}
    :root {{
        --background: #1f2123;
    }}
    *,*::before,*::after {{
        box-sizing: border-box;
    }}
    body{{
        background-color: #31363b;
        color: #ffffff;
    }}
</style>
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

    def add_seed(self, seed_string, settings, spoilers):
        self.seed_strings.append(seed_string)

        seed_filename = f"seed{len(self.seed_strings)}"
        self.seed_names.append(seed_filename)

        image_data = hashimage.generate_seed_hash_image(settings.seedHashIcons, use_bitmap=False)
        with open(self.path_to_save / f"{seed_filename}.png", "wb") as outfile:
            outfile.write(image_data)

        with open(self.path_to_save / f"{seed_filename}.html", "w") as outfile:
            outfile.write(spoilers)

        self._add_seed_html()

    def _add_seed_html(self):
        self.seed_htmls.append(f"""
<h2>Seed {len(self.seed_strings)}</h2>
<h3>{self.seed_strings[-1]}</h3><br/>
<img src="{self.seed_names[-1]}.png"><br/>
<a href="{self.seed_names[-1]}.html">Spoiler Log</a><hr/><br/><br/>
""")
