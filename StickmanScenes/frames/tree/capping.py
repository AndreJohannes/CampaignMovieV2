from PIL import Image

image_cap = Image.open("cap.png")
for i in range(0, 201):
    image = Image.open("./side/frame{}.png".format(i))  # type: Image.Image
    image.paste(image_cap, (0, 0), image_cap)
    print("save image: {}".format(i))
    image.save("./side/frame{}.png".format(i), "png")