from PIL import Image
from PIL import ImageDraw
import aggdraw
import math
import random

image = Image.open("./preps/image8.png")
eyepatch = Image.open("../eyepatch.png")
image.paste(eyepatch, (605, 254), eyepatch)
for i in range(9, 39):
    image.save("image{}.png".format(i), "png")

for i in range(0, 9):
    image = Image.open("./preps/image{:01d}.png".format(i))
    eyepatch = Image.open("../eyepatch.png")
    image.paste(eyepatch, (605, 254), eyepatch)
    image.save("image{}.png".format(i), "png")
    image.save("image{}.png".format(47 - i), "png")
