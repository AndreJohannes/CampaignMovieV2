from PIL import Image
from PIL import ImageDraw
import aggdraw
import math
import random

image = Image.open("./preps/base.png")
for i in range(0, 10):
    image.save("image{}.png".format(i), "png")
    image.save("image{}.png".format(i + 60), "png")

image = Image.open("./preps/pens.png")
for i in range(0, 50):
    image.save("image{}.png".format(i + 10), "png")
