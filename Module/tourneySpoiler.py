
from Module.resources import resource_path
from pathlib import Path
from PIL import Image
import io

class TourneySeedSaver():
    def __init__(self,path_to_save,tourney_name):
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


    def add_seed(self,seed_string,settings,spoilers):
        self.seed_strings.append(seed_string)

        hash_icon_path = Path(resource_path("static/seed-hash-icons"))
        icon_paths = [resource_path(hash_icon_path / (icon + '.png')) for icon in settings.seedHashIcons]

        # Adapted from https://stackoverflow.com/a/30228308
        images = [Image.open(x) for x in icon_paths]
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        stitched_image = Image.new('RGBA', (total_width, max_height))

        x_offset = 0
        for image in images:
            stitched_image.paste(image, (x_offset, 0))
            x_offset += image.size[0]

        image_file = io.BytesIO()
        stitched_image.save(image_file, 'PNG')
        seed_filename = f"seed{len(self.seed_strings)}"
        self.seed_names.append(seed_filename)
        with open(self.path_to_save / f"{seed_filename}.png","wb") as outfile:
            outfile.write(image_file.getvalue())
            
        with open(self.path_to_save / f"{seed_filename}.html","w") as outfile:
            outfile.write(spoilers)

        for image in images:
            image.close()
        image_file.close()
        stitched_image.close()
        self._add_seed_html()

    def _add_seed_html(self):
        self.seed_htmls.append(f"""
<h2>Seed {len(self.seed_strings)}</h2>
<h3>{self.seed_strings[-1]}</h3><br/>
<img src="{self.seed_names[-1]}.png"><br/>
<a href="{self.seed_names[-1]}.html">Spoiler Log</a><br/><br/>
""")