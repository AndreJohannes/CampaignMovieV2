import copy
import pickle
import tkinter

from PIL import Image

from Tools import Flicker2 as Flicker
from Tools.Articulated import Stickman, Stick


class Working(Flicker.Flicker):
    def __init__(self):
        super().__init__(self.key_callback)
        self.frame = 0
        self.objects = [Stickman(), Stick(150)]
        self.objects_for_frame = {self.frame: self.objects}
        self._paint()

    def key_callback(self, value: tkinter.Event):
        keycode = value.keycode
        if keycode == 57:
            self.frame -= 1
            self.frame = max(self.frame, 0)
            objs = self.objects_for_frame.get(self.frame)
            if objs is not None:
                self.objects = objs
            else:
                self.objects = copy.deepcopy(self.objects)
                self.objects_for_frame[self.frame] = self.objects
        elif keycode == 58:
            self.frame += 1
            objs = self.objects_for_frame.get(self.frame)
            if objs is not None:
                self.objects = objs
            else:
                self.objects = copy.deepcopy(self.objects)
                self.objects_for_frame[self.frame] = self.objects
                # self.frame = max(self.frame, 0)
        self._paint()

    def _paint(self):
        # self.data[self.frame] = self.stickman.get_data()
        super()._paint()

    def _get_image(self) -> Image.Image:
        return Image.open("./sequences/stillworkin/image{}.png".format(self.frame))

    def save(self):
        pickle.dump(self.objects_for_frame, open("./data/working.dat", "wb"))

    def load(self):
        self.objects_for_frame = pickle.load(open("./data/working.dat", "rb"))
        self.objects = self.objects_for_frame[self.frame]
        self._paint()

    def export(self):
        export_list = []
        for objs in self.objects_for_frame:
            export_dic = {}
            export_dic["stickman"] = self.objects_for_frame[objs][0].export()
            export_dic["stick"] = self.objects_for_frame[objs][1].export()
            export_list.append(export_dic)
        pickle.dump(export_list, open("../StickmanScenes/data/working.dat", "wb"))


if __name__ == "__main__":
    flicker = Working()
