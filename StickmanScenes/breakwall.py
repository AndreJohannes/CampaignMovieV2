import math
import pickle

from vapory import *

from Tools import Flag, StickMan, Block, Mortar

sun = LightSource([1500, 2500, 2500], 'color', 1)

sky = Sphere([0, 0, 0], 1, 'hollow',
             Texture(Pigment('gradient', [0, 1, 0],
                             ColorMap([0, 'color', 'White'],
                                      [1, 'color', 'White']),
                             'quick_color', 'White'),
                     Finish('ambient', 1, 'diffuse', 0)),
             'scale', 10000)

ground = Box([-3.15, 0, -3.15], [3.15, -0.05, 3.15],
             Texture(Pigment('color', [1. / 255. * e for e in [24, 28, 207]])),
             Finish('ambient', .2, 'diffuse', 0))

objects = [sun, ground]  # , sky, ground]

camera_1 = Camera('orthographic', 'angle', 2 * 180 / math.pi * math.atan2(6.4, 5),
                  'location', [5.0, 2.31, 0],
                  'look_at', [0.0, 2.31, 0.0])

camera_2 = Camera('orthographic', 'angle', 50,
                  'location', [10, 11, 10],
                  'look_at', [0.0, 1, 0.0])

camera_3 = Camera('orthographic', 'angle', 50,
                  'location', [0, 1.0, 5.0],
                  'look_at', [0.0, 1, 0.0])

flag = Flag.Flag(simple=True)
data = pickle.load(open("./data/breaking.dat", "rb"))

brick_small = Block.Block(0.15, 0.1, 0.2, .05)
brick_large = Block.Block(0.15, 0.1, 0.4, .05)
mortar_vertical = Mortar.Mortar(.125, .095, 0.05)
mortar_horizontal = Mortar.Mortar(.125, .05, 0.195)

bricks = {}
for i in range(0, 184):
    bricks[i] = []
for i in range(42, 184):
    bricks[i].append({"pos": (0, 0., 0.6), "type": "h"})
    bricks[i].append({"pos": (0, 0.1, 0.4), "type": "v"})
for i in range(47, 184):
    bricks[i].append({"pos": (0, 0., -0.6), "type": "h"})
    bricks[i].append({"pos": (0, 0.1, -0.4), "type": "v"})
for i in range(62, 184):
    bricks[i].append({"pos": (0, 0., 1.), "type": "h"})
    bricks[i].append({"pos": (0, 0., 1.4), "type": "h"})
    bricks[i].append({"pos": (0, 0.1, 0.8), "type": "v"})
for i in range(63, 184):
    bricks[i].append({"pos": (0, 0., -1.), "type": "h"})
    bricks[i].append({"pos": (0, 0.1, -0.8), "type": "v"})
for i in range(78, 184):
    bricks[i].append({"pos": (0, 0., 1.8), "type": "h"})
    bricks[i].append({"pos": (0, 0.1, 1.6), "type": "v"})
for i in range(79, 184):
    bricks[i].append({"pos": (0, 0., -1.8), "type": "h"})
    bricks[i].append({"pos": (0, 0., -1.4), "type": "h"})
    bricks[i].append({"pos": (0, 0.1, -1.2), "type": "v"})
for i in range(94, 184):
    bricks[i].append({"pos": (0, 0., 2.17), "type": "h"})
    bricks[i].append({"pos": (0, 0.1, 2.), "type": "v"})
for i in range(96, 184):
    bricks[i].append({"pos": (0, 0., -2.17), "type": "h"})
    bricks[i].append({"pos": (0, 0.1, -2.), "type": "v"})
for i in range(105, 184):
    bricks[i].append({"pos": (0, 0.2, 0.6), "type": "h"})
    bricks[i].append({"pos": (0, 0.2, 1), "type": "h"})
    bricks[i].append({"pos": (0, 0.3, 0.4), "type": "v"})
    bricks[i].append({"pos": (0, 0.2, -0.6), "type": "h"})
    bricks[i].append({"pos": (0, 0.3, -0.4), "type": "v"})
for i in range(114, 184):
    bricks[i].append({"pos": (0, 0.2, 1.4), "type": "h"})
    bricks[i].append({"pos": (0, 0.3, 1.2), "type": "v"})
for i in range(115, 184):
    bricks[i].append({"pos": (0, 0.2, -1.), "type": "h"})
    bricks[i].append({"pos": (0, 0.2, -1.4), "type": "h"})
    bricks[i].append({"pos": (0, 0.3, -.8), "type": "v"})
for i in range(122, 184):
    bricks[i].append({"pos": (0, 0.2, 1.8), "type": "h"})
    bricks[i].append({"pos": (0, 0.3, 1.6), "type": "v"})
for i in range(123, 184):
    bricks[i].append({"pos": (0, 0.2, -1.8), "type": "h"})
    bricks[i].append({"pos": (0, 0.3, -1.6), "type": "v"})
for i in range(129, 184):
    bricks[i].append({"pos": (0, 0.2, 2.17), "type": "h"})
    bricks[i].append({"pos": (0, 0.3, 2.), "type": "v"})
    bricks[i].append({"pos": (0, 0.4, -0.6), "type": "h"})
    bricks[i].append({"pos": (0, 0.4, -1.), "type": "h"})
    bricks[i].append({"pos": (0, 0.5, -0.4), "type": "v"})
for i in range(135, 184):
    bricks[i].append({"pos": (0, 0.4, 0.6), "type": "h"})
    bricks[i].append({"pos": (0, 0.4, 1.), "type": "h"})
    bricks[i].append({"pos": (0, 0.5, 0.4), "type": "v"})
for i in range(136, 184):
    bricks[i].append({"pos": (0, 0.2, -2.17), "type": "h"})
    bricks[i].append({"pos": (0, 0.3, -2.), "type": "v"})
for i in range(142, 184):
    bricks[i].append({"pos": (0, 0.4, 1.4), "type": "h"})
    bricks[i].append({"pos": (0, 0.5, 1.2), "type": "v"})
for i in range(144, 184):
    bricks[i].append({"pos": (0, 0.4, -1.4), "type": "h"})
    bricks[i].append({"pos": (0, 0.5, -1.2), "type": "v"})
for i in range(148, 184):
    bricks[i].append({"pos": (0, 0.4, 1.8), "type": "h"})
    bricks[i].append({"pos": (0, 0.4, 2.17), "type": "h"})
    bricks[i].append({"pos": (0, 0.5, 1.6), "type": "v"})
for i in range(150, 184):
    bricks[i].append({"pos": (0, 0.4, -1.8), "type": "h"})
    bricks[i].append({"pos": (0, 0.5, -1.6), "type": "v"})

for i in range(0, 184):
    bricks[i].append({"pos": (0, 0.3, 0), "type": "v"})
    bricks[i].append({"pos": (0, 0., .2), "type": "h"})
    bricks[i].append({"pos": (0, 0., -.2), "type": "h"})
    bricks[i].append({"pos": (0, 0.2, .2), "type": "h"})
    bricks[i].append({"pos": (0, 0.4, .2), "type": "h"})
    bricks[i].append({"pos": (0, 0.4, -.2), "type": "h"})
    bricks[i].append({"pos": (0, 0.2, -.2), "type": "h"})

for i in range(0, 152):
    bricks[i].append({"pos": (0, 0.6, .2), "type": "h"})
for i in range(0, 147):
    bricks[i].append({"pos": (0, 0.6, -.2), "type": "h"})
    bricks[i].append({"pos": (0, 0.7, 0), "type": "v"})
for i in range(0, 146):
    bricks[i].append({"pos": (0, 0.8, .2), "type": "h"})
    bricks[i].append({"pos": (0, 0.8, -.2), "type": "h"})
for i in range(0, 142):
    bricks[i].append({"pos": (0, 1.0, -.2), "type": "h"})
for i in range(0, 139):
    bricks[i].append({"pos": (0, 1.0, .2), "type": "h"})
    bricks[i].append({"pos": (0, 1.1, 0), "type": "v"})
for i in range(0, 133):
    bricks[i].append({"pos": (0, 1.2, .2), "type": "h"})
    bricks[i].append({"pos": (0, 1.2, -.2), "type": "h"})
    bricks[i].append({"pos": (0, 1.4, -.2), "type": "h"})
for i in range(0, 126):
    bricks[i].append({"pos": (0, 1.4, .2), "type": "h"})
    bricks[i].append({"pos": (0, 1.5, 0), "type": "v"})
    bricks[i].append({"pos": (0, 1.6, .2), "type": "h"})
    bricks[i].append({"pos": (0, 1.6, -.2), "type": "h"})
for i in range(0, 120):
    bricks[i].append({"pos": (0, 1.8, -.2), "type": "h"})
for i in range(0, 119):
    bricks[i].append({"pos": (0, 1.8, .2), "type": "h"})
    bricks[i].append({"pos": (0, 1.9, 0), "type": "v"})
for i in range(0, 110):
    bricks[i].append({"pos": (0, 2.0, .2), "type": "h"})
    bricks[i].append({"pos": (0, 2.0, -.2), "type": "h"})
for i in range(0, 109):
    bricks[i].append({"pos": (0, 2.2, .2), "type": "h"})
for i in range(0, 101):
    bricks[i].append({"pos": (0, 2.2, -.2), "type": "h"})
    bricks[i].append({"pos": (0, 2.3, 0), "type": "v"})
    bricks[i].append({"pos": (0, 2.4, .2), "type": "h"})
    bricks[i].append({"pos": (0, 2.4, -.2), "type": "h"})
for i in range(0, 89):
    bricks[i].append({"pos": (0, 2.6, -.2), "type": "h"})
for i in range(0, 88):
    bricks[i].append({"pos": (0, 2.6, .2), "type": "h"})
    bricks[i].append({"pos": (0, 2.7, 0), "type": "v"})
for i in range(0, 70):
    bricks[i].append({"pos": (0, 2.8, .2), "type": "h"})
    bricks[i].append({"pos": (0, 2.8, -.2), "type": "h"})
for i in range(0, 68):
    bricks[i].append({"pos": (0, 3.0, .2), "type": "h"})
for i in range(0, 56):
    bricks[i].append({"pos": (0, 3.0, -.2), "type": "h"})
    bricks[i].append({"pos": (0, 3.1, 0), "type": "v"})
for i in range(0, 52):
    bricks[i].append({"pos": (0, 3.2, .2), "type": "h"})
    bricks[i].append({"pos": (0, 3.2, -.2), "type": "h"})
for i in range(0, 36):
    bricks[i].append({"pos": (0, 3.4, -.2), "type": "h"})
for i in range(0, 32):
    bricks[i].append({"pos": (0, 3.4, .2), "type": "h"})
    bricks[i].append({"pos": (0, 3.5, 0), "type": "v"})



i = 0
for datum in data:
    if i < 0:
        i += 1
        continue

    objects_a = objects.copy()
    flag.add_objects(objects_a, math.pi / 180 * (180 - datum["flag_1"]["pole"]),
                     (-0.145, datum["flag_1"]["pos"][1], datum["flag_1"]["pos"][0]), False)
    flag.add_objects(objects_a, math.pi / 180 * (180 - datum["flag_2"]["pole"]),
                     (-0.145, datum["flag_2"]["pos"][1], datum["flag_2"]["pos"][0]), True)

    stickman = StickMan.Stickman(datum["stickman_1"])
    stickman.add_objects(objects_a)
    stickman = StickMan.Stickman(datum["stickman_2"])
    stickman.add_objects(objects_a)

    for brick in datum["bricks"]:
        if brick["large"]:
            block = brick_large.get_block()
        else:
            block = brick_small.get_block()
        objects_a.append(block.add_args(["translate", (0, brick["pos"][1], brick["pos"][0])]))

    for brick in bricks[i]:
        if brick["type"] == "h":
            objects_a.append(mortar_horizontal.get_block().add_args(["translate", brick["pos"]]))
        if brick["type"] == "v":
            objects_a.append(mortar_vertical.get_block().add_args(["translate", brick["pos"]]))

    # for mortar in get_mortar():
    #    if mortar["type"] == "v":
    #        objects_a.append(mortar_vertical.get_block().add_args(["translate", mortar["pos"]]))
    #    else:
    #        objects_a.append(mortar_horizontal.get_block().add_args(["translate", mortar["pos"]]))
    # objects_a.append(mortar_horizontal.get_block().add_args(["translate", (0, 0.2, -0.20)]))
    # objects_a.append(mortar_horizontal.get_block().add_args(["translate", (0, 0.4, 0.20)]))
    # objects_a.append(mortar_horizontal.get_block().add_args(["translate", (0, 0.4, -0.20)]))
    print("render frame: {}".format(i))
    # scene = Scene(camera_2, objects_a, included=['colors.inc', 'textures.inc'])
    # scene.render('./frames/break/bird/frame{}.png'.format(i), width=1280, height=720, antialiasing=.0001)
    scene = Scene(camera_1, objects_a, included=['colors.inc', 'textures.inc'])
    scene.render('./frames/break/side/frame{}.png'.format(i), width=1280, height=720, antialiasing=.0001,
                 transparency=True)
    i += 1
