from vapory import vapory as vp


class Mortar:
    def __init__(self, x, y, z):
        self.block = self._get_block(x, y, z)

    def get_block(self):
        return self.block

    def _get_block(self, x, y, z):
        p1 = [-x, -y, -z]
        p2 = [x, y, z]
        color = (75, 71, 0)
        return vp.Box(p1, p2, vp.Texture(vp.Pigment('color', [0.8/255. * e for e in color])),
                      vp.Finish("ambient", [1/255. * e for e in color], "diffuse",
                                0.0))
