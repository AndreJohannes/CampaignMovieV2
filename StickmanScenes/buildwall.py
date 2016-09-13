import math
import pickle

from vapory import *

from Tools import Flag, BuildWall, StickMan

sun = LightSource([1500, 2500, 2500], 'color', 1)

sky = Sphere([0, 0, 0], 1, 'hollow',
             Texture(Pigment('gradient', [0, 1, 0],
                             ColorMap([0, 'color', 'White'],
                                      [1, 'color', 'White']),
                             'quick_color', 'White'),
                     Finish('ambient', 1, 'diffuse', 0)),
             'scale', 10000)

ground = Box([-3.15, 0, -3.15], [3.15, -0.05, 3.15],
             Texture(Pigment('color', [1./255. * e for e in [24, 28, 207]])),
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
wall = BuildWall.BuildWall()
#data1 = pickle.load(open("./data/wall1.dat", "rb"))
#data2 = pickle.load(open("./data/wall2.dat", "rb"))
#data2.append(data2[len(data2) - 1].copy())
#for dat in data1:
#    dat["pos"] = [dat["pos"] - 1280 / 200., 1.]
#for dat in data2:
#    dat["pos"] = [dat["pos"] - 1280 / 200., 1.]

data = pickle.load(open("./data/wall.dat", "rb"))

for i in range(0, 20):
    objects_a = objects.copy()
    wall.add_objects(objects_a, i)
    flag.add_objects(objects_a, 0,
                     [e / 1. for e in (-0.145, -.05, -1.335)], False)
    flag.add_objects(objects_a, 0,
                     [e / 1. for e in (-0.145, -.05, 1.335)], True)

    stickman = StickMan.Stickman(data[i]["stickman_1"])
    stickman.add_objects(objects_a)
    stickman = StickMan.Stickman(data[i]["stickman_2"])
    stickman.add_objects(objects_a)

    #scene = Scene(camera_2, objects_a, included=['colors.inc', 'textures.inc'])
    #scene.render('./frames//wall/bird/frame{}.png'.format(i), width=1280, height=720, antialiasing=.0001)
    scene = Scene(camera_1, objects_a, included=['colors.inc', 'textures.inc'])
    scene.render('./frames/wall/side/frame{}.png'.format(i), width=1280, height=720, antialiasing=.0001,
                 transparency=True)
