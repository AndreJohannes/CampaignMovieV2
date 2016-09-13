from PIL import Image

for i in range(0, 201):
    image_main = Image.open("./frames/side/frame{}.png".format(i))  # type: Image.Image
    image_sub = Image.open("./frames/bird/frame{}.png".format(i))  # type: Image.Image

    image_sub = image_sub.crop((174, 164, 1026, 780))
    image_sub = image_sub.resize((int(image_sub.size[0] / 2), int(image_sub.size[1] / 2)), resample=Image.ANTIALIAS)
    image_main.paste(image_sub, (0, 0))
    print("save image: {}".format(i))
    image_main.save("./frames/compound/frame{}.png".format(i), "png")
