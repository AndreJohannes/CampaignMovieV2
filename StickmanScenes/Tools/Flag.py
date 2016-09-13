import math
import random

import vapory.vapory as vp


class Parametric(vp.POVRayElement):
    """ Paremteric() """


class Flag:
    def __init__(self, filename=None, ratio=2., lift=0, simple=False):
        texture = vp.Texture(vp.Pigment('color', [0.1 * e for e in [0.20, 0.20, 0.20]]),
                             vp.Finish("ambient", 1.0, "diffuse", 0.0))
        cylinder = vp.Cylinder([0, 0, 0], [0, 2.5, 0], 0.02, texture)
        texture = vp.Texture("" if simple else "uv_mapping", vp.Pigment(vp.ImageMap('png', filename, 'once')),
                             vp.Finish("ambient", 1.0)) if filename is not None else vp.Texture(
            vp.Pigment('color', [0.9 * e for e in [1.0, 1.00, 1.00]]),
            vp.Finish("ambient", 1.0, "diffuse", 0.0))

        sheet = vp.Polygon(5, [0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0], [0, 0, 0], texture,
                           "scale", [ratio * 0.5, 0.5, 0], "translate", [0, 2, 0]) if simple else Parametric(
            self._get_parametric_body(), texture,
            "scale", [ratio * 0.5, 0.5, 0], "translate", [0, 2, 0])  #

        self.flag = vp.Union(cylinder, sheet)
        self.flag = self.flag.add_args(["rotate", [0, 90, 0], "translate", [0, lift, 0]])

    def add_objects(self, list: list, rad, translate, inverse=False):
        list.append(
            self.flag.add_args(
                ["rotate", [0, 180 if inverse else 0, 0], "rotate", [180. / math.pi * rad, 0, 0], "translate",
                 translate]))

    def _get_parametric_body(self):
        a = random.randint(0, 30) / 10.
        b = random.randint(0, 30) / 10.
        string_list = ["function {}u + 0.05*u * sin(6*v+{}){} ".format("{", a + b, "}")]
        string_list.append(
            "function {}v*(1-0.1*u) + sin(min(4*u,3.14159/2))*(0.025 * sin(10 * u + {})+0.025*sin(19 * u + {})+0.0015*sin(39*u) -(1-cos(0.4*u))){} ".format(
                "{", a, b, "}"))
        string_list.append(
            "function {}0.02 * sin(10 * u)+0.02*sin(19*u)+0.25* u *  sin(6*v+{}){} ".format("{", a + b, "}"))
        string_list.append("<0,0>, <1,1> ")
        string_list.append("contained_by {sphere{0, 10}} ")
        return "".join(string_list)


if __name__ == "__main__":
    camera = vp.Camera('orthographic', 'angle', 50,
                       'location', [1.4 * 5.0, 1.0, 0 * 5.0],
                       'look_at', [0.0, 1.0, 0.0])

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
    Flag().add_objects(objects)
    scene = vp.Scene(camera, objects,
                     included=['colors.inc', 'textures.inc'])
    scene.render('./images/flag.png', width=1200, height=720, antialiasing=.0001)
