import random

from vapory import vapory as vp


class Block:
    def __init__(self, x, y, z, r):
        self.block = self._get_block(x, y, z, r)

    def get_block(self):
        return self.block

    def _get_block(self, x, y, z, radius):
        color = (240 + random.randint(-5, 5), 180 + random.randint(-5, 5), 75 + random.randint(-5, 5))
        color = [0.25 * e for e in color]
        # radius = 0.01
        x -= radius
        y -= radius
        z -= radius
        points = []
        points.append([x, y, z])
        points.append([x, y, -z])
        points.append([x, -y, z])
        points.append([x, -y, -z])
        points.append([-x, y, z])
        points.append([-x, y, -z])
        points.append([-x, -y, z])
        points.append([-x, -y, -z])
        links = []
        links.append([points[0], points[1]])
        links.append([points[0], points[2]])
        links.append([points[0], points[4]])
        links.append([points[1], points[3]])
        links.append([points[1], points[5]])
        links.append([points[2], points[3]])
        links.append([points[2], points[6]])
        links.append([points[3], points[7]])
        links.append([points[4], points[5]])
        links.append([points[4], points[6]])
        links.append([points[5], points[7]])
        links.append([points[6], points[7]])
        parts = []
        for point in points:
            parts.append(self._get_sphere(point, radius, color))
        for link in links:
            parts.append(self._get_cylinder(link[0], link[1], radius, color))
        for i in range(0, 3):
            p1 = [-x, -y, -z]
            p2 = [x, y, z]
            p1[i] -= radius
            p2[i] += radius
            parts.append(self._get_box(p1, p2, color))

        union = vp.Union()
        union.args = parts
        return union

    def _get_sphere(self, point, radius, color) -> vp.Sphere:
        return vp.Sphere(point, radius, vp.Texture(vp.Pigment('color', [1 / 255. * e for e in color])),
                         vp.Finish("ambient", 1.0, "diffuse", 0.0))

    def _get_cylinder(self, p1, p2, radius, color) -> vp.Cylinder:
        return vp.Cylinder(p1, p2, radius, vp.Texture(vp.Pigment('color', [1. / 255. * e for e in color])),
                           vp.Finish("ambient", 1.0, "diffuse", 0.0))

    def _get_box(self, p1, p2, color) -> vp.Box:
        return vp.Box(p1, p2, vp.Texture(vp.Pigment('color', [1. / 255. * e for e in color])),
                      vp.Finish("ambient", 1.0, "diffuse", 0.0))


if __name__ == "__main__":
    camera = vp.Camera('orthographic', 'angle', 50,
                       'location', [5.0, .5, -0.0],
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
    block = Block(.5, .4, .3, .05)
    objects.append(block.get_block())
    scene = vp.Scene(camera, objects,
                     included=['colors.inc', 'textures.inc'])
    scene.render('../images/block.png', width=1280, height=720, antialiasing=.0001)
