import random

from vapory import vapory

from  Tools.Block import Block


class BuildWall:
    def __init__(self):
        self.mortar = []
        self.layer = []
        for j in range(0, 15):
            blocks = []
            for i in range(1, 6):
                blocks.append(self._get_block().add_args(["translate", [-2.4 + i * .8, j * 0.4 + .1, -0.2]]))
                blocks.append(self._get_block().add_args(["translate", [-2.4 + i * .8, j * 0.4 + .1, 0.2]]))
            blocks.append(
                self._get_block().add_args(["rotate", [0, 90, 0],
                                            "translate", [2.2, j * 0.4 + .1, 0.0]]))
            self.layer.append(blocks)
            color = (0.40, 0.45, 0.85)
            self.mortar.append(vapory.Box([-1.8, j * .4 - .01, -.385], [2.38, j * .4 + .185, .385],
                                          vapory.Texture(
                                              vapory.Pigment('color', [0.5 / 255. * e for e in (92, 71, 0)])),
                                          vapory.Finish("ambient", [.15 / 255. * e for e in color], "diffuse",
                                                        0.6)))
            blocks = []
            blocks.append(
                self._get_block().add_args(["rotate", [0, 90, 0],
                                            "translate", [-1.8, j * 0.4 + .3, 0.0]]))
            for i in range(1, 6):
                blocks.append(self._get_block().add_args(["translate", [-2.0 + i * .8, j * 0.4 + .3, -0.2]]))
                blocks.append(self._get_block().add_args(["translate", [-2.0 + i * .8, j * 0.4 + .3, 0.2]]))
            self.layer.append(blocks)
            color = (0.40, 0.45, 0.85)
            self.mortar.append(vapory.Box([-1.8, .19 + j * .4, -.385], [2.38, j * .4 + .385, .385],
                                          vapory.Texture(
                                              vapory.Pigment('color', [0.5 / 255. * e for e in (92, 71, 0)])),
                                          vapory.Finish("ambient", [.15 / 255. * e for e in color], "diffuse",
                                                        0.6)))

    def _get_block(self):
        return Block(0.4, .1, .2, .05).get_block()
        # return vapory.Box([-0.39, 0, -0.19], [.39, 0.19, 0.19],
        #                  vapory.Texture(vapory.Pigment('color', [1. / 255. * e for e in color])),
        #                  vapory.Finish("ambient", [.5 / 255. * e for e in color], "diffuse", 0.6))

    def _get_sphere(self, point, radius, color) -> vapory.Sphere:
        return vapory.Sphere(point, radius, vapory.Texture(vapory.Pigment('color', [1. / 255. * e for e in color])),
                             vapory.Finish("ambient", 0.1, "diffuse", 0.6))

    def _get_cylinder(self, p1, p2, radius, color) -> vapory.Cylinder:
        return vapory.Sphere(p1, p2, radius, vapory.Texture(vapory.Pigment('color', [1. / 255. * e for e in color])),
                             vapory.Finish("ambient", 0.1, "diffuse", 0.6))

    def add_objects(self, list, limit=1000):
        # pass
        # list.append(self.foundation)
        random.seed(5)
        limit_n = 0
        for i in range(0, limit):
            limit_n += random.randint(0, 3)
        i = 0
        for blocks in self.layer:
            if i >= limit_n:
                break
            for block in blocks:
                list.append(block)
                list.append(self.mortar[i])
            i += 1
