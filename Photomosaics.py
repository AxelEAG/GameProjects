from PIL import Image as img
import numpy as np
import pandas as pd


def average_color(pixels, x_init, x_final, y_init, y_final):
    summ = [0, 0, 0]
    for a in range(x_init, x_final): # column
        for b in range(y_init, y_final): # row
            summ += pixels[b][a] # row x column
    total = (x_final - x_init)*(y_final - y_init)

    avg = np.array([int(summ[0]/total), int(summ[1]/total), int(summ[2]/total)])
    return avg


# def average_color(pixels, x_init, x_final, y_init, y_final):
#     summ = [0, 0, 0]
#     for a in range(x_init, x_final): # column
#         summ += sum(pixels[a]) # row x column
#     total = (x_final - x_init)*(y_final - y_init)
#
#     avg = np.array([int(summ[0]/total), int(summ[1]/total), int(summ[2]/total)])
#     return avg


def pixelate(pixels, x_step, y_step):
    pixelated = np.zeros_like(pixels)
    width = len(pixels[0])
    height = len(pixels)

    for i in range(0, len(pixels[0]), x_step):
        for j in range(0, len(pixels), y_step):
            x_final = i + x_step
            y_final = j + y_step
            if width <= x_final:
                x_final = width
            if height <= y_final:
                y_final = height

            pixel = average_color(pixels, i, x_final, j, y_final)
            for k in range(x_final - i):
                for m in range(y_final - j):
                    pixelated[j+m][i+k] = pixel

    return pixelated


def photomosaic(pixels, x_step, y_step):
    pixelated = np.zeros_like(pixels)
    width = len(pixels[0])
    height = len(pixels)

    for i in range(0, len(pixels[0]), x_step):
        for j in range(0, len(pixels), y_step):
            x_final = i + x_step
            y_final = j + y_step
            if width <= x_final:
                x_final = width
            if height <= y_final:
                y_final = height

            avg_color = average_color(pixels, i, x_final, j, y_final)
            index_image = find_closest_image(flowers, avg_color)
            flower = img.open(f"images\\flower{index_image}.jpg")
            flower = flower.resize((x_step, y_step))
            flower_arr = np.asarray(flower)

            for k in range(x_final - i):
                for m in range(y_final - j):
                    pixelated[j+m][i+k] = flower_arr[m][k]

    return pixelated


def calculate_distance(R1, G1, B1, R2, G2, B2):
    distance = ((R2-R1)**2 + (G2-G1)**2 + (B2-B1)**2)**0.5
    return distance


def find_closest_image(flowers, avg_color):
    R1, G1, B1 = avg_color
    smallest = 100000
    index_img = 0
    for i in range(len(flowers.index)):
        index, R2, G2, B2 = flowers.loc[i]
        distance = calculate_distance(R1, G1, B1, R2, G2, B2)
        if distance < smallest:
            smallest = distance
            index_img = index
    return index_img


def read_csv(csv):
    data = pd.read_csv(csv)
    return data


flowers = read_csv("flowers2.csv")

# image = img.open("DOG.jpg")
image = img.open("CuteDog.jpg")
image = image.resize((800, 800))
width, height = image.size
image.show()

initial = np.asarray(image)
# initial = np.array([[[250, 210, 0], [20, 10, 4]], [[20, 20, 10], [2, 4, 5]]])

final = photomosaic(initial, 10, 10)
image2 = img.fromarray(final)
image2.show()

# final = pixelate(initial, 20, 20)
# image2 = img.fromarray(final)
# image2.show()

