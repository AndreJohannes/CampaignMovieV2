from PIL import Image
from PIL import ImageDraw
import aggdraw
import math
import random

for i in range(0, 6):
    image = Image.open("./preps/image{:01d}.png".format(i))
    eyepatch = Image.open("../eyepatch.png")
    image.paste(eyepatch, (605, 254), eyepatch)
    image.save("image{}.png".format(i), "png")
