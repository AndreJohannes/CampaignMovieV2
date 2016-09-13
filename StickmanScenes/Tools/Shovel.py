import vapory.vapory as vp


class Parametric(vp.POVRayElement):
    """ Paremteric() """


class Shovel:
    def __init__(self):
        texture = vp.Texture(vp.Pigment('color', [0.15 * e for e in [0.50, 0.50, 0.10]]),
                             vp.Finish("ambient", 1., "diffuse", 0))
        cylinder1 = self._get_cylinder([0, 0, 0], [0, -1.15, 0], 0.02, texture)
        cylinder2 = self._get_cylinder([0, -1.15, 0], [0, -1.2, -0.015], 0.02, texture)
        #texture = vp.Texture(vp.Pigment('color', [0.15 * e for e in [0.50, 0.50, 0.10]]),
        #                     vp.Finish("phong", 0.9, "metallic", 10))
        #texture = vp.Texture("Polished_Brass")
        shovel = Parametric(self._get_parametric_body(), texture, "scale", [0.5, 0.5, 0.5],
                            "rotate", [0, 0, 90], "translate", [0.25, -1.2, -.045])
        self.position = [0, 0, 0]
        self.orientation = 0
        self.body = vp.Union(cylinder1, cylinder2, shovel)

    def set_orientation(self, orientation, position):
        self.position = position
        self.orientation = orientation

    def _get_parametric_body(self):
        string_list = ["function {-0.7*u-0.3*u*sqrt(1-3*(0.5-v)*(0.5-v))}"]
        string_list.append("function{v}")
        string_list.append("function{-(2-u)*(sqrt(1-.4*(0.5-v)*(0.5-v))-1)+0.1*u*u*u}")
        string_list.append("<0,0>, <1,1> ")
        string_list.append("contained_by {sphere{0, 10}} ")
        return "".join(string_list)

    def _get_cylinder(self, start, end, radius, texture):
        c1 = vp.Sphere(start, radius, texture)
        c2 = vp.Sphere(end, radius, texture)
        c3 = vp.Cylinder(start, end, radius, texture)
        return vp.Union(c1, c2, c3)

    def add_object(self, list, turn=False):
        list.append(
            self.body.add_args(
                ["rotate", [0, 0 if not turn else 180, 0], "rotate", [self.orientation, 0, 0], "translate",
                 self.position]))
