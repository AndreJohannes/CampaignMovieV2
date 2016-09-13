import numpy
import vapory.vapory as vp


class Soil:
    def __init__(self, scale):
        segments = []
        texture = vp.Texture(vp.Pigment('color', [1 / 255. * e for e in (40, 40, 40)]))
        for i in range(1, 1000):
            rands = numpy.random.normal(0, .03 * scale, 3)
            sphere = vp.Sphere(rands, 0.01, texture)
            segments.append(sphere)
        self.body = vp.Union()
        self.body.args = segments

    def add_object(self, list, translate):
        list.append(self.body.add_args(["translate", translate]))
