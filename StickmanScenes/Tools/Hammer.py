import vapory.vapory as vp


class Parametric(vp.POVRayElement):
    """ Paremteric() """


class Hammer:
    def __init__(self):
        cylinder1 = self._get_cylinder([0, 0, 0], [0, .45, 0], 0.02)
        cylinder2 = self._get_cylinder([0, .45, +0.015], [0, .45, -0.015], 0.04)
        self.body = vp.Union(cylinder1, cylinder2)

    def set_orientation(self, orientation, position):
        self.position = position
        self.orientation = orientation

    def _get_cylinder(self, start, end, radius):
        c1 = vp.Sphere(start, radius, vp.Texture("Brass_Metal"))
        c2 = vp.Sphere(end, radius, vp.Texture("Brass_Metal"))
        c3 = vp.Cylinder(start, end, radius, vp.Texture("Brass_Metal"))
        return vp.Union(c1, c2, c3)

    def add_object(self, list, turn=False):
        list.append(
            self.body.add_args(
                ["rotate", [0, 0 if not turn else 180, 0], "rotate", [self.orientation, 0, 0], "translate",
                 self.position]))