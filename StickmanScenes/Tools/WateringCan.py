import math

import vapory.vapory as vp


class WateringCan:
    def __init__(self):
        color = (80/255., 80/255., 80/255.)
        texture = vp.Texture(vp.Pigment('color', color),
                             vp.Finish('ambient', color, 'diffuse', 0))
        self.body = vp.Union(self._get_body(texture), self._get_trunk(texture), self._get_Handle(texture))
        cos = math.cos(math.pi / 180 * 15)
        sin = math.sin(math.pi / 180 * 15)
        self.origin = [0, -(0.14 * cos + .24), -(.2 + 0.14 * sin)]
        self.body = self.body.add_args(["translate", self.origin])
        self.position = [0, 0, 0]
        self.orientation = 0

    def get_tip(self):
        sin = math.sin(math.pi / 180. * self.orientation)
        cos = math.cos(math.pi / 180. * self.orientation)
        tip = [0, .066 + math.sqrt(2) / 2. * 0.48, -.180 - math.sqrt(2) / 2. * 0.48]
        return [self.position[0] + self.origin[0],
                self.position[1] + cos * (self.origin[1] + tip[1]) - sin * (self.origin[2] + tip[2]),
                self.position[2] + cos * (self.origin[2] + tip[2]) + sin * (self.origin[1] + tip[1])]

    def set_orientation(self, orientation, position):
        self.position = position
        self.orientation = orientation

    def _get_body(self, texture):
        return vp.Cylinder([0, 0, 0], [0, .2, 0], .1, texture, "scale", [1, 2, 2])

    def _get_trunk(self, texture):
        c1 = vp.Cone([0, 0, 0], 0.024, [0, .4, 0], 0.014, texture)
        c2 = vp.Cone([0, .4, 0], 0.014, [0, .48, 0], 0.1, texture)
        return vp.Union(c1, c2, "rotate", [-45, 0, 0], "translate", [0, .066, -.180])

    def _get_Handle(self, texture):
        d_deg = 10
        elems = []
        for i in range(0, 180, d_deg):
            sin = math.sin(math.pi / 180. * i)
            cos = math.cos(math.pi / 180. * i)
            start = [0, 0.14 * cos + .24, +.2 + 0.14 * sin]
            sin = math.sin(math.pi / 180. * (i + d_deg))
            cos = math.cos(math.pi / 180. * (i + d_deg))
            end = [0, 0.14 * cos + .24, +.2 + 0.14 * sin]
            elems.append(self._get_cylinder(start, end, 0.007, texture))
        union = vp.Union()
        union.args = elems
        return union

    def _get_cylinder(self, start, end, radius, texture):
        c1 = vp.Sphere(start, radius, texture)
        c2 = vp.Sphere(end, radius, texture)
        c3 = vp.Cylinder(start, end, radius, texture)
        return vp.Union(c1, c2, c3)

    def add_object(self, list):
        list.append(self.body.add_args(["rotate", [self.orientation, 0, 0], "translate", self.position]))


if __name__ == "__main__":
    camera = vp.Camera('orthographic', 'angle', 50,
                       'location', [3.0, .5, -0.0],
                       'look_at', [0.0, .5, 0.0])

    sun = vp.LightSource([1500, 2500, 2500], 'color', 1)

    sky = vp.Sphere([0, 0, 0], 1, 'hollow',
                    vp.Texture(vp.Pigment('gradient', [0, 1, 0],
                                          vp.ColorMap([0, 'color', 'White'],
                                                      [1, 'color', 'White']),
                                          'quick_color', 'White'),
                               vp.Finish('ambient', 1, 'diffuse', 0)),
                    'scale', 10000)

    ground = vp.Box([-2, 0, -2], [2, -0.05, 2],
                    vp.Texture(vp.Pigment('color', [1.1 * e for e in [0.40, 0.45, 0.85]])),
                    vp.Finish('phong', 0.1))

    objects = [sun, sky, ground]
    WateringCan().add_object(objects)
    scene = vp.Scene(camera, objects,
                     included=['colors.inc', 'textures.inc'])
    scene.render('../images/can.png', width=1200, height=800, antialiasing=.0001)
