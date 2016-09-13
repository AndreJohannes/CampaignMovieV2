import math
import pickle

from PIL import Image
from vapory import *

from Tools import Foundation, StickMan, Shovel, Soil, MakeTree

sun = LightSource([1500, 2500, 2500], 'color', 1)

sky = Sphere([0, 0, 0], 1, 'hollow',
             Texture(Pigment('gradient', [0, 1, 0],
                             ColorMap([0, 'color', 'White'],
                                      [1, 'color', 'White']),
                             'quick_color', 'White'),
                     Finish('ambient', 1, 'diffuse', 0)),
             'scale', 10000)

ground = Box([-3.15, 0, -3.15], [3.15, -0.05, 3.15],
             Texture(Pigment('color', [1.1 * e for e in [0.40, 0.45, 0.85]])),
             Finish('phong', 0.1))

objects = [sun, ground, sky]

#tree = pickle.load(open("./data/tree/tree.dat", "rb"))
#objects.append(tree.add_args(["translate", [0, 0, 0]]))
Foundation.Foundation().add_objects(objects)
MakeTree.scene(0, objects)
# Parable.Parable().add_object(objects)
shovel = Shovel.Shovel()
data = pickle.load(open("./data/working.dat", "rb"))

camera_1 = Camera('orthographic', 'angle', 2 * 180 / math.pi * math.atan2(6.4, 5),
                  'location', [5.0, 2.31, 0],
                  'look_at', [0.0, 2.31, 0.0])

camera_2 = Camera('orthographic', 'angle', 50,
                  'location', [10, 11, 10],
                  'look_at', [0.0, 1, 0.0])

for i in range(33, 200, 1):
    print("saving frame: {}".format(i))
    if i > 32:
        idx = ((i - 3) % 30) + 3
        im = Image.open('./frames/working/side/frame{}.png'.format(idx))
        im.save('./frames/working/side/frame{}.png'.format(i), "png")
        continue
    idx = i if i < 30 else i - 30
    stickman = StickMan.Stickman(data[idx]["stickman"])
    objects_a = objects.copy()
    shovel.set_orientation(-data[idx]["stick"]["end"],
                           [0.07 + 0.04, data[idx]["stick"]["pos"][1],
                            data[idx]["stick"]["pos"][0]])
    shovel.add_object(objects_a, turn=True if idx >= 12 else False)
    stickman.add_objects(objects_a)
    if i > 21:
        x = 1.7 - 0.3 * int((i - 22) / 2)
        scale = 1 + ((i - 22) / 10)
        Soil.Soil(scale).add_object(objects_a, [0, 1 - 0.5 * (x - 1.1) ** 2, x])
    #scene = Scene(camera_2, objects_a, included=['colors.inc', 'textures.inc'])
    #scene.render('./frames/working/bird/frame{}.png'.format(i), width=1280, height=720)
    scene = Scene(camera_1, objects_a, included=['colors.inc', 'textures.inc'])
    scene.render('./frames/working/side/frame{}.png'.format(i), width=1280, height=720, antialiasing=0.0001)
