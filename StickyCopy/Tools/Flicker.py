import math
import tkinter

from PIL import Image, ImageTk, ImageDraw

from Tools.Stickman import Stickman, Part


class Flicker:
    def __init__(self):
        app = tkinter.Tk()
        app.title("StickyCopy")
        app.bind("<Key>", self.key_callback)
        app.bind("<Button-1>", self.mouse_callback)
        app.bind("<ButtonRelease-1>", self.button_release_callback)
        app.bind("<B1-Motion>", self.motion_callback)
        self.canvas = tkinter.Canvas(app, width=1280, height=720)
        self.canvas.pack()
        self.status = None #Part.POSITION  # type: Part
        self.stickman = Stickman()

    def key_callback(self, value: tkinter.Event):
        keycode = value.keycode
        # print(keycode)
        if keycode >= 10 and keycode <= 20:
            for part in Part:
                if part.value + 9 == keycode:
                    self.status = part
        elif keycode == 113:
            if self.status == Part.POSITION:
                self.stickman.inc_position(-1, 0)
            else:
                self.stickman.inc_angle(self.status, -math.pi / 180.)
        elif keycode == 114:
            if self.status == Part.POSITION:
                self.stickman.inc_position(1, 0)
            else:
                self.stickman.inc_angle(self.status, math.pi / 180.)
        elif keycode == 111:
            self.stickman.inc_position(0, -1)
        elif keycode == 116:
            self.stickman.inc_position(0, 1)
        self._paint()

    def mouse_callback(self, event):
        self.status = None
        for part in Part:
            if self._get_distance_sqr(event.x, event.y, self.stickman.get_position(part)) < 10:
                self.status = part

    def button_release_callback(self, event):
        self.status = None

    def motion_callback(self, event):
        if self.status == Part.POSITION:
            self.stickman.set_position(event.x, event.y)
        elif self.status == Part.TORSO:
            pos = self.stickman.get_position(Part.POSITION)
            self.stickman.set_angle(Part.TORSO, math.atan2(-pos[0]+event.x, pos[1]-event.y))
        elif self.status == Part.UPPER_LEG_1:
            pos = self.stickman.get_position(Part.POSITION)
            self.stickman.set_angle(Part.UPPER_LEG_1, math.atan2(-pos[0] + event.x, pos[1] - event.y))
        elif self.status == Part.LOWER_LEG_1:
            pos = self.stickman.get_position(Part.UPPER_LEG_1)
            self.stickman.set_angle(Part.LOWER_LEG_1, math.atan2(-pos[0] + event.x, pos[1] - event.y))
        elif self.status == Part.UPPER_LEG_2:
            pos = self.stickman.get_position(Part.POSITION)
            self.stickman.set_angle(Part.UPPER_LEG_2, math.atan2(-pos[0] + event.x, pos[1] - event.y))
        elif self.status == Part.LOWER_LEG_2:
            pos = self.stickman.get_position(Part.UPPER_LEG_2)
            self.stickman.set_angle(Part.LOWER_LEG_2, math.atan2(-pos[0] + event.x, pos[1] - event.y))
        elif self.status == Part.UPPER_ARM_1:
            pos = self.stickman.get_position(Part.TORSO)
            self.stickman.set_angle(Part.UPPER_ARM_1, math.atan2(-pos[0]+event.x, pos[1]-event.y))
        elif self.status == Part.LOWER_ARM_1:
            pos = self.stickman.get_position(Part.UPPER_ARM_1)
            self.stickman.set_angle(Part.LOWER_ARM_1, math.atan2(-pos[0] + event.x, pos[1] - event.y))
        elif self.status == Part.UPPER_ARM_2:
            pos = self.stickman.get_position(Part.TORSO)
            self.stickman.set_angle(Part.UPPER_ARM_2, math.atan2(-pos[0] + event.x, pos[1] - event.y))
        elif self.status == Part.LOWER_ARM_2:
            pos = self.stickman.get_position(Part.UPPER_ARM_2)
            self.stickman.set_angle(Part.LOWER_ARM_2, math.atan2(-pos[0] + event.x, pos[1] - event.y))
        elif self.status == Part.HEAD:
            pos = self.stickman.get_position(Part.TORSO)
            self.stickman.set_angle(Part.HEAD, math.atan2(-pos[0] + event.x, pos[1] - event.y))
        self._paint()

    def _paint(self, image=None):
        image = self._get_image() if image is None else image
        image = image.convert("RGBA")
        canvas = ImageDraw.Draw(image)
        for part in Part:
            if part is not Part.POSITION:
                value = 180. / math.pi * self.stickman.get_angle(part)
                canvas.text((10, part.value * 10), "{} - {}: {:0.2f}".format(part.value, part.name, value),
                            "black" if part is not self.status else "red")
        self.stickman.draw(image)
        self.photo_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(640, 360, image=self.photo_image)

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
                   "pos": data[Part.POSITION][0] / 100.
                   }
            retList.append(dic)
        return retList

    def _get_image(self) -> Image.Image:
        return Image.new("RGBA", (1280, 720))

    def _get_distance_sqr(self, x, y, position):
        return (position[0]-x)**2 + (position[1]-y)**2