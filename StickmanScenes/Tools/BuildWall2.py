from  Tools.Block import Block
from numpy import random

class BuildWall:
    def __init__(self):
        self.layer = []
        for j in range(0, 9):
            blocks = []
            for i in range(1, 6):
                dy1 = random.normal(0,.005)
                dy2 = random.normal(0, .005)
                dz1 = random.normal(0, .005)
                dz2 = random.normal(0, .005)

                blocks.append(
                    self._get_block().add_args(["translate", [-2.4 + i * .8, j * 0.4 + .2 + dy1, -0.2 + dz1]]))
                blocks.append(self._get_block().add_args(["translate", [-2.4 + i * .8, j * 0.4 + .2 + dy2, 0.2 + dz2]]))
            self.layer.append(blocks)

    def _get_block(self):
        return Block(0.4, .2, .2, .05).get_block()

    def add_objects(self, list, limit=1000):
        for blocks in self.layer:
            for block in blocks:
                list.append(block)
                # list.append(self.mortar[i])
