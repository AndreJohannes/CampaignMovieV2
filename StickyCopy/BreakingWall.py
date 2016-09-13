import copy
import pickle
import tkinter

from PIL import Image, ImageDraw

from Tools import Flicker2 as Flicker
from Tools.Articulated import Stickman, Flag, Brick


class Breaking(Flicker.Flicker):
    def __init__(self):
        super().__init__(self.key_callback)
        self.frame = 0
        self.objects = [Stickman(), Stickman(), Flag(), Flag(inverse=True)]
        for i in range(0, 9):
            self.objects.append(Brick((640, 581 - i * 40), large=True))
            self.objects.append(Brick((620, 561 - i * 40)))
            self.objects.append(Brick((660, 561 - i * 40)))
        self.shadows = [self.objects[0]]
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
            shadows = self.objects_for_frame.get(self.frame - 1)
            if shadows is not None:
                self.shadows = shadows
        elif keycode == 58:
            self.frame += 1
            objs = self.objects_for_frame.get(self.frame)
            if objs is not None:
                self.objects = objs
            else:
                self.objects = copy.deepcopy(self.objects)
                self.objects_for_frame[self.frame] = self.objects
            shadows = self.objects_for_frame.get(self.frame - 1)
            if shadows is not None:
                self.shadows = shadows
                # self.frame = max(self.frame, 0)
        self._paint()

    def _paint(self):
        # self.data[self.frame] = self.stickman.get_data()
        super()._paint()

    def save_sequence(self):
        for frame in self.objects_for_frame:
            image = Image.new("RGBA",(1280,720),"grey")
            img = Image.open("./sequences/ground.png")
            image.paste(img, (0,0), img)
            canvas = ImageDraw.Draw(image)
            for obj in self.objects_for_frame.get(frame):
                obj.draw(image)
            image.save("./frames/breakwall/frame{}.png".format(frame), "png")

    def _get_image(self) -> Image.Image:
        image = Image.open("./sequences/wall.png") if self.frame == 0 else Image.open("./sequences/ground.png")
        canvas = ImageDraw.Draw(image)
        canvas.text((10, 10), "Frame: {}".format(self.frame))
        return image

    def save(self):
        pickle.dump(self.objects_for_frame, open("./data/breaking.dat", "wb"))

    def load(self):
        self.objects_for_frame = pickle.load(open("./data/breaking.dat", "rb"))
        self.objects = self.objects_for_frame[self.frame]
        self._paint()

    def shift(self, frame):
        top = len(self.objects_for_frame)
        for i in range(top, frame, -1):
            self.objects_for_frame[i] = self.objects_for_frame[i-1]
        self.objects_for_frame[frame] = copy.deepcopy(self.objects_for_frame[frame - 1])

    def export(self):
        export_list = []
        for objs in self.objects_for_frame:
            export_dic = {}
            export_dic["stickman_1"] = self.objects_for_frame[objs][0].export()
            export_dic["stickman_2"] = self.objects_for_frame[objs][1].export()
            export_dic["flag_1"] = self.objects_for_frame[objs][2].export()
            export_dic["flag_2"] = self.objects_for_frame[objs][3].export()
            export_dic["bricks"] = []
            for i in range(4, len(self.objects_for_frame[objs])):
                export_dic["bricks"].append(self.objects_for_frame[objs][i].export())
            export_list.append(export_dic)
        pickle.dump(export_list, open("../StickmanScenes/data/breaking.dat", "wb"))


if __name__ == "__main__":
    flicker = Breaking()
