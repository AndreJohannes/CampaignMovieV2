import random

from vapory import vapory

from Tools.Block import Block


class Foundation:
    def __init__(self):
        self.blocks = []
        for i in range(-1, 2):
            block = self._get_block().add_args(["translate", [i * .4, .0, .7]])
            self.blocks.append(block)
            block = self._get_block().add_args(["translate", [i * .4, .0, -.7]])
            self.blocks.append(block)
            block = self._get_block().add_args(["translate", [i * .4, .2, .7]])
            self.blocks.append(block)
            block = self._get_block().add_args(["translate", [i * .4, .2, -.7]])
            self.blocks.append(block)
            block = self._get_block().add_args(["rotate", [0, 90, 0], "translate", [.7, 0.1, 0.4 * i]])
            self.blocks.append(block)
            block = self._get_block().add_args(["rotate", [0, 90, 0], "translate", [-.7, 0.1, 0.4 * i]])
            self.blocks.append(block)
        for i in range(-2, 2):
            block = self._get_block().add_args(["rotate", [0, 90, 0], "translate", [.7, 0, 0.4 * i + .2]])
            self.blocks.append(block)
            block = self._get_block().add_args(["rotate", [0, 90, 0], "translate", [-.7, 0, 0.4 * i + .2]])
            self.blocks.append(block)
            block = self._get_block().add_args(["rotate", [0, 90, 0], "translate", [.7, 0.2, 0.4 * i + .2]])
            self.blocks.append(block)
            block = self._get_block().add_args(["rotate", [0, 90, 0], "translate", [-.7, 0.2, 0.4 * i + .2]])
            self.blocks.append(block)
            block = self._get_block().add_args(["translate", [0.4 * i + .2, 0.1, 0.7]])
            self.blocks.append(block)
            block = self._get_block().add_args(["translate", [0.4 * i + .2, 0.1, -0.7]])
            self.blocks.append(block)

        color = (75, 71, 0)
        self.blocks.append(vapory.Box([-.79, 0, -0.79], [.79, 0.29, 0.79],
                                      vapory.Texture(vapory.Pigment('color', [0.8/255. * e for e in color])),
                                      vapory.Finish("ambient", [1/255. * e for e in color], "diffuse",
                                0.0)))

        self.foundation = vapory.Union()
        self.foundation.args = self.blocks
        self.foundation = self.foundation.add_args(["scale", [2, 2, 2]])

    def _get_block(self):
        return Block(.2, .05, .1, 0.025).get_block().add_args(["translate", [0, 0.05, 0]])

        color = (240 + random.randint(-5, 5), 180 + random.randint(-5, 5), 75 + random.randint(-5, 5))
        return vapory.Box([-0.195, 0, -0.095], [.195, 0.095, 0.095],
                          vapory.Texture(vapory.Pigment('color', [0.5*1. / 255. * e for e in color])),
                          vapory.Finish("ambient", 0.1, "diffuse", 0.6))

    def add_objects(self, list):
        # pass
        list.append(self.foundation)
        # for block in self.blocks:
        #    list.append(block)


if __name__ == "__main__":
    camera = vapory.Camera('orthographic', 'angle', 50,
                           'location', [5.0, 6.0, 5.0],
                           'look_at', [0.0, 1.0, 0.0])

    sun = vapory.LightSource([1500, 2500, 2500], 'color', 1)

    sky = vapory.Sphere([0, 0, 0], 1, 'hollow',
                        vapory.Texture(vapory.Pigment('gradient', [0, 1, 0],
                                                      vapory.ColorMap([0, 'color', 'White'],
                                                                      [1, 'color', 'White']),
                                                      'quick_color', 'White'),
                                       vapory.Finish('ambient', 1, 'diffuse', 0)),
                        'scale', 10000)

    ground = vapory.Box([-2, 0, -2], [2, -0.05, 2],
                        vapory.Texture(vapory.Pigment('color', [1.1 * e for e in [0.40, 0.45, 0.85]])),
                        vapory.Finish('phong', 0.1))

    objects = [sun, sky, ground]
    Foundation().add_objects(objects)
    scene = vapory.Scene(camera, objects,
                         included=['colors.inc', 'textures.inc'])
    scene.render('./images/foundation.png', width=1200, height=800, antialiasing=.0001)
