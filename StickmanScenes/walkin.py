import math
import pickle

from vapory import *

from Tools import StickMan, Flag

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

objects = [sun]  # , ground]

data1 = pickle.load(open("./data/walkin.dat", "rb"))
data1[7]["upper_arm1"] = -12
data1[9]["upper_arm1"] = -13
data1[10]["upper_arm1"] = -13
data1[11]["upper_arm1"] = -14

data2 = []

for data in data1:
    # print(data["upper_arm1"])
    data["pos"] = [-data["pos"] + 6.86319163032431, 1]
    data_mirror = data.copy()
    for key in data_mirror:
        if key == "pos":
            data["pos"] = [-data["pos"][0], 1]
        else:
            data_mirror[key] = - data[key]
    data2.append(data_mirror)

camera_1 = Camera('orthographic', 'angle', 2 * 180 / math.pi * math.atan2(6.4, 5),
                  'location', [5.0, 2.31, 0],
                  'look_at', [0.0, 2.31, 0.0])

camera_2 = Camera('orthographic', 'angle', 50,
                  'location', [10, 11, 10],
                  'look_at', [0.0, 1, 0.0])

camera_3 = Camera('orthographic', 'angle', 50,
                  'location', [0, 1.0, 5.0],
                  'look_at', [0.0, 1, 0.0])

flag = Flag.Flag(lift=-1, simple=True)

# MakeTree.scene(0, objects)
i = 0
rad_old = 0
for data in data1:
    print("saving frame: {}".format(i))
    objects_a = objects.copy()


    def addStickman(data, objects, inverse=False):
        pos = -2 * 3 / 5.
        # print(data)
        stickman = StickMan.Stickman(data)
        stickman.add_objects(objects)
        rad = (math.atan2(-stickman.left_hand[2] + stickman.left_shoulder[2],
                          -stickman.left_hand[1] + stickman.left_shoulder[1]) if i < 31 else
               math.atan2(-stickman.left_hand[2] + stickman.right_hand[2],
                          -stickman.left_hand[1] + stickman.right_hand[1]))
        if i >= 35:
            flag.add_objects(objects_a, 0,
                             [e / 1. for e in (-0.14500000000000002, .95, -1.335 if not inverse else 1.335)], inverse)
        else:
            tr = [stickman.left_hand[0], stickman.left_hand[1] + data["pos"][1], stickman.left_hand[2] + data["pos"][0]]
            flag.add_objects(objects_a, rad, tr, inverse)


    addStickman(data, objects_a)
    addStickman(data2[i], objects_a, True)
    #scene = Scene(camera_2, objects_a, included=['colors.inc', 'textures.inc'])
    #scene.render('./frames//walkin/bird/frame{}.png'.format(i), width=1280, height=720, antialiasing=.0001,
    #             transparency=True)
    scene = Scene(camera_1, objects_a, included=['colors.inc', 'textures.inc'])
    scene.render('./frames/walkin/side/frame{}.png'.format(i), width=1280, height=720, antialiasing=.0001,
                 transparency=True, quality=0)
    # scene = Scene(camera_3, objects_a, included=['colors.inc', 'textures.inc'])
    # scene.render('./frames/walkin/front/frame{}.png'.format(i), width=1280, height=720, antialiasing=.0001)
    i += 1
