import vapory.vapory as vp


class Parable:
    def __init__(self):

        def drange(start, stop, step):
            r = start
            while r < stop:
                yield r
                r += step

        def func(x):
            return 1-0.5*(x-1.1)**2

        step = 0.05
        segments = []
        for x in drange(-6.4, 6.4, step):
            y = x + step
            cylinder = self._get_cylinder([0, func(x), x], [0, func(y), y], 0.02)
            segments.append(cylinder)

        self.body = vp.Union()
        self.body.args = segments

    def _get_cylinder(self, start, end, radius):
        texture = vp.Texture(vp.Pigment('color', [1 / 255. * e for e in (0, 125, 255)]))
        c1 = vp.Sphere(start, radius, texture)
        c2 = vp.Sphere(end, radius, texture)
        c3 = vp.Cylinder(start, end, radius, texture)
        return vp.Union(c1, c2, c3)

    def add_object(self, list):
        list.append(self.body)
