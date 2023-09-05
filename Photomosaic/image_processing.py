from PIL import Image as img
import glob
import os


def crop_image(image):
    width, height = image.size
    if width < height:
        box = (0, int((height-width)/2), width, height - int((height-width)/2))
    else:
        box = (int((width-height)/2), 0, width - int((width-height)/2), height)

    return image.crop(box)

#
# def save_image(image, filename):
#     file =


# flowers = ["astilbe", "bellflower", "black_eyed_susan", "calendula", "california_poppy", "carnation", "common_daisy",
#            "coreopsis", "daffodil", "dandelion", "iris", "magnolia", "rose", "sunflower", "tulip", "water_lily"]
file = os.getcwd()

count = 0
file_name = file + "\\archive (1)\\flower_images\\flower_images"
names = glob.glob(file_name + "\\*.png")
for name in names:
    imag = img.open(name)
    imag = imag.convert('RGB')
    cropped = crop_image(imag)
    cropped.save(f"images2\\flower{count}.jpg")
    count += 1
