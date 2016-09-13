import random

import vapory.vapory as vp


class Seeds:
    def __init__(self, i):
        segments = []
        i = i * 2

        def add(i0_n, x):
            i0 = -random.gauss(i0_n, .2)
            x0 = i0 / (11. * x) + 1
            y0 = -i0 * i0 / 100.
            x1 = (i + i0) / (11. * x) - x0
            y1 = -(i + i0) * (i + i0) / 100. - y0
            x2 = (i + 1 + i0) / (11. * x) - x0
            y2 = -(i + 1 + i0) * (i + 1 + i0) / 100. - y0
            segments.append(self._get_cylinder([0, y1, x1], [0, y2, x2], 0.02))

        add(0, 1)
        add(0, 1.1)
        add(0, .9)

        self.body = vp.Union()
        self.body.args = segments

    def _get_cylinder(self, start, end, radius):
        color = (40 / 255., 40 / 255., 40 / 255.)
        texture = vp.Texture(vp.Pigment('color', color),
                             vp.Finish("ambient", color, "diffuse",
                                       0.0)
                             )
        c1 = vp.Sphere(start, radius, texture)
        c2 = vp.Sphere(end, radius, texture)
        c3 = vp.Cylinder(start, end, radius, texture)
        return vp.Union(c1, c2, c3)

    def add_object(self, list, translate):
        list.append(vp.Intersection(self.body.add_args(["translate", translate]), vp.Box(
            [-20, 0, -20], [20, 20, 20]
        )))
