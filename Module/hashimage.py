import io
from pathlib import Path

from PIL import Image

from Module.resources import resource_path


def generate_seed_hash_image(icon_names: list[str], use_bitmap: bool = False) -> bytes:
    """
    Generates an image of the seed hash given a list of seed hash icon names. If use_bitmap is True, the image will
    have a black background and be returned as a bitmap. If use_bitmap is False, the image will have a transparent
    background and be returned as a PNG.
    """

    hash_icon_path = Path(resource_path("static/seed-hash-icons")).absolute()

    icon_paths: list[Path] = []
    if use_bitmap:
        for icon_name in icon_names:
            icon_paths.append(hash_icon_path / '{}.bmp'.format(icon_name))
    else:
        for icon_name in icon_names:
            icon_paths.append(hash_icon_path / '{}.png'.format(icon_name))

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
