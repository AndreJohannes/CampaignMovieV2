import math
import tkinter

from PIL import Image, ImageTk, ImageDraw

from Tools.Articulated import Root


class Flicker:
    def __init__(self, callback=None):
        app = tkinter.Tk()
        app.title("StickyCopy")
        app.bind("<Button-1>", self.mouse_callback)
        app.bind("<ButtonRelease-1>", self.button_release_callback)
        app.bind("<B1-Motion>", self.motion_callback)
        if callback is not None:
            app.bind("<Key>", callback)
        self.canvas = tkinter.Canvas(app, width=1280, height=720)
        self.canvas.pack()
        self.status = None  # Part.POSITION  # type: Part

    def mouse_callback(self, event):
        self.status = None
        for obj in self.objects:
            for node in obj.root.get_nodes():
                if self._get_distance_sqr(event.x, event.y, node.get_position()) < 10:
                    self.status = node

    def button_release_callback(self, event):
        self.status = None

    def motion_callback(self, event):
        if self.status is None:
            return
        if isinstance(self.status, Root):
            self.status.set_position((event.x, event.y))
        else:
            pos = self.status.parent.position
            self.status.set_angle(180. / math.pi * math.atan2(-pos[0] + event.x, pos[1] - event.y))
        self._paint()

    def _paint(self, image=None):
        image = self._get_image() if image is None else image
        image = image.convert("RGBA")
        canvas = ImageDraw.Draw(image)
        for obj in self.shadows:
            obj.draw(image, shadow=True)
        for obj in self.objects:
            obj.draw(image)
        self.photo_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(640, 360, image=self.photo_image)

    def _get_image(self) -> Image.Image:
        return Image.new("RGBA", (1280, 720))

    def _get_distance_sqr(self, x, y, position):
        return (position[0] - x) ** 2 + (position[1] - y) ** 2
