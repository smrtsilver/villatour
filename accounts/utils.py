from io import BytesIO  # basic input/output operation
from PIL import Image  # Imported to compress images
from django.core.files import File  # to store files


def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    # im = im.resize([500,500])
    im = im.convert("RGB")
    # resize = im.resize((240, 240), Image.ANTIALIAS)
    # w, h = image.size
    #
    # image = image.resize((w / 2, h / 2), Image.ANTIALIAS)

    im.save(im_io, 'JPEG', quality=35)
    # optimize=True REDUCE SIZE AS MUCH AZ POSSIBLE
    new_image = File(im_io, name=image.name)
    return new_image
