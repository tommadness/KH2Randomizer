import io
from pathlib import Path

from PIL import Image

from Module.resources import resource_path


def seed_hash_icon_path(icon_name: str, use_bitmap: bool = False) -> Path:
    icon_dir = Path(resource_path("static/icons/seed-hash-icons")).absolute()
    if use_bitmap:
        return icon_dir / f"{icon_name}.bmp"
    else:
        return icon_dir / f"{icon_name}.png"


def generate_seed_hash_image(icon_names: list[str], use_bitmap: bool) -> bytes:
    """
    Generates an image of the seed hash given a list of seed hash icon names. If use_bitmap is True, the image will
    have a black background and be returned as a bitmap. If use_bitmap is False, the image will have a transparent
    background and be returned as a PNG.
    """

    icon_paths: list[Path] = [seed_hash_icon_path(icon_name, use_bitmap) for icon_name in icon_names]

    # Adapted from https://stackoverflow.com/a/30228308
    images = [Image.open(x) for x in icon_paths]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    if use_bitmap:
        stitched_image = Image.new('RGB', (total_width, max_height))
    else:
        stitched_image = Image.new('RGBA', (total_width, max_height))

    x_offset = 0
    for image in images:
        stitched_image.paste(image, (x_offset, 0))
        x_offset += image.size[0]

    image_file = io.BytesIO()
    if use_bitmap:
        stitched_image.save(image_file, 'BMP')
    else:
        stitched_image.save(image_file, 'PNG')

    image_data = image_file.getvalue()

    for image in images:
        image.close()
    image_file.close()
    stitched_image.close()

    return image_data
