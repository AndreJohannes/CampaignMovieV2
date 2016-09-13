import math
import pickle

import vapory.vapory as vp

from Tools import StickMan, MakeTree

sun = vp.LightSource([1500, 2500, 2500], 'color', 1)

sky = vp.Sphere([0, 0, 0], 1, 'hollow',
                vp.Texture(vp.Pigment('gradient', [0, 1, 0],
                                      vp.ColorMap([0, 'color', 'White'],
                                                  [1, 'color', 'White']),
                                      'quick_color', 'White'),
                           vp.Finish('ambient', 1, 'diffuse', 0)),
                'scale', 10000)

ground = vp.Box([-4.36, 0, -4.36], [4.36, -0.05, 4.36],
                vp.Texture(vp.Pigment('color', [1.1 * e for e in [0.40, 0.45, 0.85]])),
                vp.Finish('phong', 0.1))

objects = [sun, ground, sky]

camera_1 = vp.Camera('orthographic', 'angle', 2 * 180 / math.pi * math.atan2(6.4, 5),
                     'location', [5.0, 2.31, 0],
                     'look_at', [0.0, 2.31, 0.0])

camera_2 = vp.Camera('orthographic', 'angle', 50,
                     'location', [10, 11, 10],
                     'look_at', [0.0, 1, 0.0])

data = pickle.load(open("./data/dream.dat", "rb")).pop()

data["stickman_1"]["pos"]=  (data["stickman_1"]["pos"][0], data["stickman_1"]["pos"][1]+0.325)
data["stickman_2"]["pos"]=  (data["stickman_2"]["pos"][0], data["stickman_2"]["pos"][1]+0.325)
data["stickman_3"]["pos"]=  (data["stickman_3"]["pos"][0], data["stickman_3"]["pos"][1]+0.325)

objects_a = objects.copy()
MakeTree.scene(0, objects_a)
tree = objects_a.pop()
# pickle.dump(tree, open("./data/tree/tree.dat","wb"))
# tree = pickle.load(open("./data/tree/tree.dat", "rb"))
objects_a.append(tree.add_args(["translate", [0, -.6, -1.2]]))

stickman = StickMan.Stickman(data["stickman_1"])
stickman.add_objects(objects_a)
stickman = StickMan.Stickman(data["stickman_2"])
stickman.add_objects(objects_a)
stickman = StickMan.Stickman(data["stickman_3"])
stickman.add_objects(objects_a)

scene = vp.Scene(camera_2, objects_a, included=['colors.inc', 'textures.inc'])
scene.render('./frames/dreaming_bird.png', width=1280, height=720, antialiasing=.0001)
scene = vp.Scene(camera_1, objects_a, included=['colors.inc', 'textures.inc'])
scene.render('./images/dreaming.png', width=1280, height=720, antialiasing=.0001)

# passing 'ipython' as argument at the end of an IPython Notebook cell will display the picture in the IPython notebook.
# scene.render('ipython', width=300, height=200)



# passing no 'file' arguments returns the rendered image as a RGB numpy array
# image = scene.render(width=300, height=500)
