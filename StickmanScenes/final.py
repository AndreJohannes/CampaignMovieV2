import math
import pickle

import vapory.vapory as vp

from Tools import StickMan, Flag, MakeTree

sun = vp.LightSource([1500, 2500, 2500], 'color', 1)

sky = vp.Sphere([0, 0, 0], 1, 'hollow',
                vp.Texture(vp.Pigment('gradient', [0, 1, 0],
                                      vp.ColorMap([0, 'color', 'White'],
                                                  [1, 'color', 'White']),
                                      'quick_color', 'White'),
                           vp.Finish('ambient', 1, 'diffuse', 0)),
                'scale', 10000)

ground = vp.Box([-4.36, 0, -6.1], [4.36, -0.05, 3.85],
                vp.Texture(vp.Pigment('color', [1.1 * e for e in [0.40, 0.45, 0.85]])),
                vp.Finish('phong', 0.1))

objects = [sun, ground, sky]

camera_1 = vp.Camera('orthographic', 'angle', 2 * 180 / math.pi * math.atan2(6.4, 5),
                     'location', [5.0, 2.31, 0 * 5],
                     'look_at', [0.0, 2.31, 0.0])

camera_2 = vp.Camera('orthographic', 'angle', 50,
                     'location', [10, 11, 10],
                     'look_at', [0.0, 1, 0.0])

datas = pickle.load(open("./data/final.dat", "rb"))

box = vp.Box([-10, 0, -10], [10, 10, 10])

for data in datas:
    vert = 4.85 - data["pos"][1]
    data["pos"] = data["pos"][0] - 6.4
    stickman = StickMan.Stickman(data)
    stickman.add_objects(objects)
    stickman = objects.pop()
    objects.append(vp.Intersection(stickman.add_args(["translate", [0, vert, 0]]), box))

flag = Flag.Flag(filename='"./flags/america.png"', ratio=1.8, simple=False)
flag.add_objects(objects, 0, [-.3, -.2, 1.5 - 6.4])
flag = objects.pop()
objects.append(vp.Intersection(flag, box))
flag = Flag.Flag(filename='"./flags/japan.png"', ratio=1.75, simple=False)
flag.add_objects(objects, 0, [-.3, -.81, 2.45 - 6.4])
flag = objects.pop()
objects.append(vp.Intersection(flag, box))
flag = Flag.Flag(filename='"./flags/mexican.png"', ratio=1.7, simple=False)
flag.add_objects(objects, 0, [-.3, -.95, 3.55 - 6.4])
flag = objects.pop()
objects.append(vp.Intersection(flag, box))
flag = Flag.Flag(filename='"./flags/german.png"', ratio=1.65, simple=False)
flag.add_objects(objects, 0, [-.3, -.79, 5.32 - 6.4], inverse=True)
flag = objects.pop()
objects.append(vp.Intersection(flag, box))
flag = Flag.Flag(filename='"./flags/brazil.png"', ratio=1.7, simple=False)
flag.add_objects(objects, 0, [-.3, -.71, 6.69 - 6.4], inverse=True)
flag = objects.pop()
objects.append(vp.Intersection(flag, box))
flag = Flag.Flag(filename='"./flags/argentina.png"', ratio=1.65, simple=False)
flag.add_objects(objects, 0, [-.3, -.62, 7.75 - 6.4], inverse=True)
flag = objects.pop()
objects.append(vp.Intersection(flag, box))
flag = Flag.Flag(filename='"./flags/spanish.png"', ratio=1.7, simple=False)
flag.add_objects(objects, 0, [-.3, -.12, 8.7 - 6.4], inverse=True)
flag = objects.pop()
objects.append(vp.Intersection(flag, box))

objects_a = objects.copy()
MakeTree.scene(0, objects_a)
tree = objects_a.pop()
# pickle.dump(tree, open("./data/tree/tree.dat","wb"))
#tree = pickle.load(open("./data/tree/tree.dat", "rb"))
objects_a.append(tree.add_args(["translate", [0, -.6, -1.87]]))
scene = vp.Scene(camera_1, objects_a, included=['colors.inc', 'textures.inc'])
scene.render('./images/final.png', width=1280, height=720, antialiasing=.0001)
scene = vp.Scene(camera_2, objects_a, included=['colors.inc', 'textures.inc'])
# scene.render('./frames/final_bird.png', width=1280, height=720, antialiasing=.0001)
