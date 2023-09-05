from Photomosaic import Photomosaics as ph
from PIL import Image as img
import numpy as np
import csv
import glob

names = glob.glob("images2\\flower*.jpg")
count = 0

with open("flowers3.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["index", "R", "G", "B"])

    for name in names:
        image = img.open(name)
        width, height = image.size
        pixels = np.asarray(image)
        R, G, B = ph.average_color(pixels, 0, width - 1, 0, height - 1)
        writer.writerow([count, R, G, B])
        count += 1
        print(count)



