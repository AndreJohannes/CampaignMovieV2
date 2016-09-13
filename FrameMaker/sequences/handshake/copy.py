import cairo

for i in range(0,16):
    image = cairo.ImageSurface.create_from_png("../pullWall2/frame{}.png".format(i+160))
    image.write_to_png("./frame{}.png".format(i))

