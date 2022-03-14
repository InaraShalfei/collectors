import string
import random

from PIL import Image

from collectors.settings import MEDIA_ROOT


def watermark_image(file):
    image = Image.open(file)
    watermarked_image = Image.open(MEDIA_ROOT + '/watermark.jpg')
    watermarked_image = watermarked_image.resize(image.size, Image.NEAREST)
    my_img = Image.blend(image, watermarked_image, 0.5)
    filename_prefix = ''.join(random.choices(string.ascii_uppercase, k=16))
    new_filename = f'{file.name}'
    my_img.save(MEDIA_ROOT + '/' + new_filename)

    return new_filename
