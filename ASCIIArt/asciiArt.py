from PIL import Image as img

image = img.open("ascii-pineapple.jpg")
width, height = image.size
print("Successfully loaded image!")
print(f"Image size: {width} x {height}")
image.resize((int(width*0.6), int(height*0.6)))
image.show()
width, height = image.size

scale = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
print(len(scale))
pixels = list(image.getdata())
new_pixels = []
ascii_img = []
line = []

for n in range(len(pixels)):
    brightness = sum(pixels[n])/3
    new_pixels.append(brightness)

    num = int(65*brightness/255)
    ascii_eq = scale[num]
    line.append(ascii_eq*3)
    if (n + 1) % width == 0:
        ascii_img.append(line)
        line = []

print(len(ascii_img[0]))
for i in range(len(ascii_img)):
    print(*ascii_img[i], sep="")


# red, green, blue = image.split()
# zeroed_band = red.point(lambda _: 0)
#
# red_merge = img.merge("RGB", (red, zeroed_band, zeroed_band))
# red_merge.show()





