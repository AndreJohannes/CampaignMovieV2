import random

import vapory.vapory as vp


class Water:
    def __init__(self, lim, off):
        segments = []
        for i in range(3*off, min(3 * max(lim, 0), 10)):
            def add(i0_n, dx):
                i0 = -random.gauss(i0_n, .4)
                x0 = -i0 / 12.
                y0 = -x0 * x0 * 1. + dx
                x1 = -(i + i0) / 12. - x0
                y1 = -(i + i0) * (i + i0) / 100. - y0
                x2 = -(i + 1 + i0) / 12. - x0
                y2 = -(i + 1 + i0) * (i + 1 + i0) / 100. - y0
                segments.append(self._get_cylinder([0, y1, x1], [0, y2, x2], 0.014))

            add(0, 0)
            add(-1.5, 0.05)
            add(2, -0.05)

        self.body = vp.Union()
        self.body.args = segments

    def _get_cylinder(self, start, end, radius):
        color = (0, 125/255., 255/255.)
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
            [-2, 0, -2], [2, 2, 2]
        )))
