import math
import pickle

from vapory import *

from Tools import Foundation, StickMan, MakeTree, WateringCan

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

Foundation.Foundation().add_objects(objects)
data1 = pickle.load(open("./data/seeding.dat", "rb")).pop()
data2 = pickle.load(open("./data/watering.dat", "rb")).pop()
data1["pos"] = (data1["pos"] - (6.86319163032431 + 0.2), 1.6)
data1["thigh_1"] *= 0.5
data1["thigh_2"] *= 0.5
data2["pos"] = (data2["pos"] - (6.86319163032431 - 0.43), 1.6)
stickman = StickMan.Stickman(data1)
stickman.add_objects(objects)
stickman = StickMan.Stickman(data2)
stickman.add_objects(objects)
can = WateringCan.WateringCan()
can.set_orientation(0, (
    stickman.left_hand[0], stickman.left_hand[1] + data2["pos"][1], stickman.left_hand[2] + data2["pos"][0]))
can.add_object(objects)

camera_1 = Camera('orthographic', 'angle', 2 * 180 / math.pi * math.atan2(6.4, 5),
                  'location', [5.0, 2.31, 0],
                  'look_at', [0.0, 2.31, 0.0])

camera_2 = Camera('orthographic', 'angle', 50,
                  'location', [10, 11, 10],
                  'look_at', [0.0, 1, 0.0])

for i in range(200, 54, -1):
    print("saving frame: {}".format(i))
    objects_a = objects.copy()
    MakeTree.scene(200 - (i if i != 0 else 1), objects_a)
    pickle.dump(objects_a, open("./data/tree/tree{}.dat".format(i), "wb"))
    scene = Scene(camera_2, objects_a, included=['colors.inc', 'textures.inc'])
    scene.render('./frames/tree/bird/frame{}.png'.format(i), width=1280, height=720, antialiasing=.0001)
    scene = Scene(camera_1, objects_a, included=['colors.inc', 'textures.inc'])
    scene.render('./frames/tree/side/frame{}.png'.format(i), width=1280, height=720, antialiasing=.0001)

# passing 'ipython' as argument at the end of an IPython Notebook cell will display the picture in the IPython notebook.
# scene.render('ipython', width=300, height=200)



# passing no 'file' arguments returns the rendered image as a RGB numpy array
# image = scene.render(width=300, height=500)
