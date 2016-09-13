import tkinter
import pickle
from PIL import Image
from Tools import Flicker
from Tools.Stickman import Part

class Seeding(Flicker.Flicker):
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
            data = self.data.get(self.frame)
            if data is not None:
                self.stickman.set_data(data)
                # self.frame = max(self.frame, 0)
        super().key_callback(value)

    def _paint(self):
        self.data[self.frame] = self.stickman.get_data()
        super()._paint()

    def _get_image(self) -> Image.Image:
        return Image.open("./sequences/seeding/image{}.png".format(self.frame))

    def export(self):
        pickle.dump(self._export(), open("../StickmanScenes/data/seeding.dat", "wb"))

if __name__ == "__main__":
    flicker = Seeding()