import math
import pickle

from vapory import *

from Tools import StickMan, Flag, WateringCan, Water, Foundation, Seeds

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

data1 = pickle.load(open("./data/seeding.dat", "rb"))

data2 = pickle.load(open("./data/watering.dat", "rb"))

data3 = pickle.load(open("./data/can.dat", "rb"))

for data in data1:
    data["pos"] = [data["pos"] - (6.86319163032431 + 0.2), 1.6]
    data["thigh_1"] *= 0.5
    data["thigh_2"] *= 0.5

for data in data2:
    data["pos"] = [data["pos"] - (6.86319163032431 - 0.43), 1.6]

camera_1 = Camera('orthographic', 'angle', 2 * 180 / math.pi * math.atan2(6.4, 5),
                  'location', [5.0, 2.31, 0],
                  'look_at', [0.0, 2.31, 0.0])

camera_2 = Camera('orthographic', 'angle', 50,
                  'location', [10, 11, 10],
                  'look_at', [0.0, 1, 0.0])

camera_3 = Camera('orthographic', 'angle', 50,
                  'location', [0, 1.0, 5.0],
                  'look_at', [0.0, 1, 0.0])

flag = Flag.Flag()
Foundation.Foundation().add_objects(objects)
can = WateringCan.WateringCan()

# MakeTree.scene(0, objects)
rad_old = 0
for i in range(0, 73):
    j = max(i - 30, 0)
    print("saving frame: {}".format(i))
    objects_a = objects.copy()
    stickman = StickMan.Stickman(data1[min(i, 37)])
    stickman.add_objects(objects_a)
    stickman = StickMan.Stickman(data2[j])
    stickman.add_objects(objects_a)
    can.set_orientation(data3[max(j, 0)], [stickman.left_hand[0], stickman.left_hand[1] + data2[j]["pos"][1],
                                           stickman.left_hand[2] + data2[j]["pos"][0]])
    can.add_object(objects_a)  # stickman.left_hand, data3[i]
    water = Water.Water(j - 17, max(0, j - 32))
    water.add_object(objects_a, can.get_tip())
    if (i >= 8 and i <= 14):
        seeds = Seeds.Seeds(i - 8)
        seeds.add_object(objects_a, [0, 1.6, 0])
    if (i >= 25 and i <= 31):
        seeds = Seeds.Seeds(i - 25)
        seeds.add_object(objects_a, [0, 1.6, 0])

    scene = Scene(camera_2, objects_a, included=['colors.inc', 'textures.inc'])
    #scene.render('./frames//seednwater/bird/frame{}.png'.format(i), width=1280, height=720, antialiasing=.0001,
    #             transparency=True, quality=0)
    scene = Scene(camera_1, objects_a, included=['colors.inc', 'textures.inc'])
    scene.render('./frames/seednwater/side/frame{}.png'.format(i), width=1280, height=720, antialiasing=.0001,
                 transparency=False)
    # scene = Scene(camera_3, objects_a, included=['colors.inc', 'textures.inc'])
    # scene.render('./frames/walkin/front/frame{}.png'.format(i), width=1280, height=720, antialiasing=.0001)
