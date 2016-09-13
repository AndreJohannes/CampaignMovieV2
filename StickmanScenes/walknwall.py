from PIL import Image

i = 0

for j in range(0, 38):
    image = Image.open("./frames/walkin/side/frame{}.png".format(j))
    image.save("./frames/walknwall/side/frame{}.png".format(i), "png")
    i += 1

for j in range(0, 20):
    image = Image.open("./frames/wall/side/frame{}.png".format(j))
    image.save("./frames/walknwall/side/frame{}.png".format(i), "png")
    i += 1
