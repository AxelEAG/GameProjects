from PIL import Image as img

image = img.open("ascii-pineapple.jpg")
width, height = image.size
image = image.resize((int(width*0.5), int(height*0.5)))
width, height = image.size

scale = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
pixels = list(image.getdata())
new_pixels = []
ascii_img = []
line = []

for n in range(len(pixels)):
    # brightness = sum(pixels[n])/3
    # new_pixels.append(brightness)
    # num = int(65*brightness/255)

    # R, G, B = pixels[n]
    # lightness = (max(R, G, B) + min(R, G, B))/2
    # num = int(65 * lightness / 255) - 1

    R, G, B = pixels[n]
    lumosity = 0.21*R + 0.72*G + 0.07*B
    num = int(65*lumosity/255) - 1
    
    ascii_eq = scale[num]
    line.append(ascii_eq*3)
    if (n + 1) % width == 0:
        ascii_img.append(line)
        line = []

for i in range(len(ascii_img)):
    print(*ascii_img[i], sep="")





