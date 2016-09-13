import pickle
import tkinter
import math
from PIL import Image, ImageDraw

from Tools import Flicker
from Tools.Stickman import Part


class Final(Flicker.Flicker):
    def __init__(self):
        super().__init__()
        self.frame = 0
        self.data = {}  # pickle.load(open("./data/walkin.dat", "rb"))
        for i in self.data:
            if self.data.get(i).get(Part.HEAD) is None:
                self.data.get(i)[Part.HEAD] = 0
        if self.data.get(0) is not None:
            self.stickman.set_data(self.data[0])

    def key_callback(self, value: tkinter.Event):
        keycode = value.keycode
        if keycode == 57:
            self.frame -= 1
            self.frame = max(self.frame, 0)
            data = self.data.get(self.frame)
            if data is not None:
                self.stickman.set_data(data)
        elif keycode == 58:
            self.frame += 1
            self.frame = self.frame if self.frame <= 6 else 6
            data = self.data.get(self.frame)
            if data is not None:
                self.stickman.set_data(data)
        super().key_callback(value)

    def _paint(self):
        self.data[self.frame] = self.stickman.get_data()
        image = self._get_image()
        image = image.convert("RGBA")
        canvas = ImageDraw.Draw(image)
        canvas.text((10, 10), "{} - {}: {:0.2f}".format(0, "Figure", self.frame),
                    "black")
        super()._paint(image=image)

    def _get_image(self) -> Image.Image:
        return Image.open("./sequences/finalScene.png".format(self.frame))

    def export(self):
        pickle.dump(self._export(), open("../StickmanScenes/data/final.dat", "wb"))

    def _export(self):
        retList = []
        for i in self.data:
            data = self.data[i]
            dic = {"thigh_1": 180 - 180. / math.pi * data[Part.UPPER_LEG_1],
                   "shin_1": 180 - 180. / math.pi * data[Part.LOWER_LEG_1],
                   "thigh_2": 180 - 180. / math.pi * data[Part.UPPER_LEG_2],
                   "shin_2": 180 - 180. / math.pi * data[Part.LOWER_LEG_2],
                   "upper_arm1": 180 - 180. / math.pi * data[Part.UPPER_ARM_1],
                   "lower_arm1": 180 - 180. / math.pi * data[Part.LOWER_ARM_1],
                   "upper_arm2": 180 - 180. / math.pi * data[Part.UPPER_ARM_2],
                   "lower_arm2": 180 - 180. / math.pi * data[Part.LOWER_ARM_2],
                   "torso": 180 - 180. / math.pi * data[Part.TORSO],
                   "head": 180 - 180. / math.pi * data[Part.HEAD],
                   "pos": (data[Part.POSITION][0] / 100.,data[Part.POSITION][1] / 100.)
                   }
            retList.append(dic)
        return retList

if __name__ == "__main__":
    flicker = Final()
