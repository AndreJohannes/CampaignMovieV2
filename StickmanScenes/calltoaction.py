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

objects = [sun]  # , sky, ground]

camera_1 = Camera('orthographic', 'angle', 2 * 180 / math.pi * math.atan2(6.4, 5),
                  'location', [5.0, 2.31, 0],
                  'look_at', [0.0, 2.31, 0.0])

camera_2 = Camera('orthographic', 'angle', 50,
                  'location', [10, 11, 10],
                  'look_at', [0.0, 1, 0.0])

camera_3 = Camera('orthographic', 'angle', 50,
                  'location', [0, 1.0, 5.0],
                  'look_at', [0.0, 1, 0.0])

data = pickle.load(open("./data/call.dat", "rb"))

i=0
for dato in data:
    objects_a = objects.copy()

    stickman = StickMan.Stickman(dato["stickman_1"], falda=True)
    stickman.add_objects(objects_a)

    #scene = Scene(camera_2, objects_a, included=['colors.inc', 'textures.inc'])
    #scene.render('./frames//wall/bird/frame{}.png'.format(i), width=1280, height=720, antialiasing=.0001)
    scene = Scene(camera_1, objects_a, included=['colors.inc', 'textures.inc'])
    scene.render('./frames/call/frame{}.png'.format(i), width=1280, height=720, antialiasing=.0001,
                 transparency=True)
    i += 1