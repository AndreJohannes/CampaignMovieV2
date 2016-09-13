import tkinter
import pickle
from PIL import Image
from Tools import Flicker2 as Flicker
from Tools.Articulated import Stickman

class Dream(Flicker.Flicker):
    def __init__(self):
        super().__init__()
        self.objects = [Stickman(), Stickman(), Stickman()]
        self.shadows = []
        self._paint()

    def key_callback(self, value: tkinter.Event):
        super().key_callback(value)

    def _paint(self):
        super()._paint()

    def _get_image(self) -> Image.Image:
        return Image.open("./sequences/dreaming.png")

    def save(self):
        pickle.dump(self.objects, open("./data/dreaming.dat", "wb"))

    def load(self):
        self.objects = pickle.load(open("./data/dreaming.dat", "rb"))
        self._paint()

    def export(self):
        export_list = []
        export_dic = {}
        export_dic["stickman_1"] = self.objects[0].export()
        export_dic["stickman_2"] = self.objects[1].export()
        export_dic["stickman_3"] = self.objects[2].export()
        export_list.append(export_dic)
        pickle.dump(export_list, open("../StickmanScenes/data/dream.dat", "wb"))


if __name__ == "__main__":
    flicker = Dream()