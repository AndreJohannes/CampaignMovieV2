import random

import vapory.vapory as vp

from Tools import Vector3D


def make_tree(iters: int):
    random.seed(7)#5)
    return [[0, 0],
            _make_tree(iters, 40, 0),
            _make_tree(iters, 30, 95),
            _make_tree(iters, 45, 170),
            _make_tree(iters, 40, 271),
            _make_tree(iters, 0, 0)]


def _make_tree(iter: int, a: float, b: float) -> list:
    if iter <= 0:
        return [[a, b]]
    ret_array = [[a, b]]
    ret_array.append(_make_tree(iter - 1, a + 20 + random.randint(-15, 35), b + random.randint(-15, 15)))
    ret_array.append(_make_tree(iter - 1, a - 20 + random.randint(-15, 35), b + random.randint(-15, 15)))
    ret_array.append(_make_tree(iter - 1, a + random.randint(-15, 35), b + 50 + random.randint(-15, 15)))
    ret_array.append(_make_tree(iter - 1, a + random.randint(-15, 35), b - 50 + random.randint(-15, 15)))
    return ret_array


def get_tree(tree, fac, fac2):
    return _get_tree(0, tree, (0, 0, 0), fac, fac, fac2)


def _get_tree(iter, branch, pos: tuple, l, fac, fac2):
    vec = Vector3D.fromAngles(branch[0][0], branch[0][1], l)
    vec = (vec[0] * 0.8, 0.8 * vec[1], 1.2 * vec[2])
    pos = Vector3D.add(pos, vec)
    pos = pos + (fac2 * (0.045 - 0.005 * iter if iter > 0 else 0.055),)
    ret_array = [pos]
    for branch in branch[1:]:
        ret_array.append(_get_tree(iter + 1, branch, pos, l * fac, fac, fac2))

    return ret_array


def trav(start, branch, r, objects, t, iter):
    end = branch[0]
    # print(end[3])
    # print(start, end)
    cylinder = vp.Cone([start[0], start[2], start[1]], end[3], [end[0], end[2], end[1]], end[3],
                       vp.Texture(vp.Pigment('color', [0.7 / 255. * e for e in [98, 78, 44]])),
                       vp.Finish('ambient', [0.7 / 255. * e for e in [98, 78, 44]], "diffuse", 0.1))
    top = vp.Sphere([end[0], end[2], end[1]], end[3],
                    vp.Texture(vp.Pigment('color', [.7 / 255. * e for e in [98, 78, 44]])),
                    vp.Finish('ambient', [0.7 / 255. * e for e in [98, 78, 44]], "diffuse", 0.1))
    for i in range(0, int(t * 450)):
        (dx, dy, dz) = Vector3D.fromAngles(random.randint(0, 180), random.randint(0, 360),
                                           t * random.randint(0, 5) / (5. * (iter + 2) if iter != 0 else 1000))
        # dx = random.randint(-5, 5) / 30.
        # dy = random.randint(-5, 5) / 30.
        # dz = random.randint(-5, 5) / 30.
        dr = random.randint(-5, 5) / 30.
        dg = random.randint(-5, 5) / 30.
        db = random.randint(-5, 5) / 30.
        ddx = random.randint(1, 10) / 10000.
        ddy = random.randint(0, 10) / 10000.
        ddz = random.randint(0, 10) / 10000.
        color = (random.randint(40, 180), random.randint(120, 250), random.randint(0, 50))
        leave = vp.Cylinder([end[0] + dx, end[2] + dy, end[1] + dz],
                            [end[0] + dx + ddx, end[2] + dy + ddy, end[1] + dz + ddz],
                            .01 + random.randint(0, 10) / 1000.,
                            vp.Texture(vp.Pigment('color', [2 / 255. * e for e in color])),
                            vp.Finish('phong', 1))
        objects.append(leave.add_args(["scale", [2, 2, 2], "translate", [0, 0.58, 0]]))

    for i in range(0, int(random.randint(0, 10) / 5)):
        (dx, dy, dz) = Vector3D.fromAngles(random.randint(90, 180), random.randint(0, 360),
                                           t * random.randint(4, 4) / (5 * (iter + 2) if iter != 0 else 1000))

        color = (random.randint(190, 250), random.randint(40, 80), random.randint(40, 80))
        fruit = vp.Sphere([end[0] + dx, end[2] + dz, end[1] + dy], 0.04,
                          vp.Texture(vp.Pigment('color', [2 / 255. * e for e in color])))
        #objects.append(fruit.add_args(["scale", [2, 2, 2], "translate", [0, 0.58, 0]]))

    objects.append(cylinder.add_args(["scale", [2, 2, 2], "translate", [0, 0.58, 0]]))
    objects.append(top.add_args(["scale", [2, 2, 2], "translate", [0, 0.58, 0]]))

    for branch in branch[1:]:
        trav(end, branch, r - (0.005 if r != 0.05 else 0.02), objects, t, iter + 1)


def scene(t, objects):
    print("make scene")
    # sun = LightSource([1500 , 2500,
    tree = get_tree(make_tree(3), 0.7 - t / 500., 1 - t / 210.)
    random.seed()
    # print("make tree object")
    tree_list = []
    trav((0, 0, 0, 0.07), tree, .05 - (t / 5000.), tree_list, 1 - t / 200., 0)
    tree = vp.Union()
    tree.args = tree_list
    objects.append(tree)
    # pos = 2
