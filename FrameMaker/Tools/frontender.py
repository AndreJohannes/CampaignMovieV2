import Tkinter
import cairo
import datetime
from PIL import Image, ImageTk, ImageDraw


class Languages:
    ENGLISH = 1
    SPANISH = 2
    GERMAN = 3
    list_of_languages = [ENGLISH, SPANISH]


class evolve_base:
    def draw(self, frame, surface):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        for obj in self.list:
            obj.draw(frame, surface)


    def set_language(self, language):
        for element in self.list:
            if hasattr(element, "set_language"):
                element.set_language(language)


class _moduleList:
    def __init__(self):
        self.list = []
        self.frame_counter = 0;

    def append(self, module):
        print("load module \"{}\" at frame {}".format(module.__name__, self.frame_counter))
        evolver = module.evolve(self.frame_counter)
        self.list.append(evolver)
        self.frame_counter = evolver.stopTime

    def get_list(self):
        return self.list

    def print_list(self):

        for instance in self.list:
            print("module \"{}\" at frame {}".format(instance.__module__, instance.startTime))


class Flicker:
    def __init__(self, list_of_modules):
        app = Tkinter.Tk()
        app.title("PSYDEH")
        app.bind("<Key>", self.key_callback)
        self.canvas = Tkinter.Canvas(app, width=1280, height=720)
        self.canvas.pack()
        self.frame = 0
        self.save = False
        self.photo_image = None
        self.language = Languages.ENGLISH
        self.list = _moduleList()
        for module in list_of_modules:
            self.list.append(module)

    def key_callback(self, value):
        if (value.keycode == 113):
            self.frame -= 1
        elif (value.keycode == 114):
            self.frame += 1
        elif (value.keycode == 111):
            self.frame -= 10
        elif (value.keycode == 116):
            self.frame += 10
        elif (value.char == "s"):
            self.save = not self.save
        surface = self._get_white_surface()  # cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720)
        for obj in self.list.get_list():
            obj.draw(self.frame, surface)
        if self.save:
            print("saving frame: {}".format(self.frame))
            self._save_frame(surface, self.frame, self.language)
        image = Image.frombuffer("RGBA", (surface.get_width(), surface.get_height()), surface.get_data(), "raw", "BGRA",
                                 0, 1)
        d = ImageDraw.Draw(image)
        d.text((0, 0), "frame: {}".format(self.frame), "black")
        d.text((0, 8), "time: {}".format(datetime.timedelta(seconds=self.frame / 25)), "black")
        d.text((0, 16), "save: {}".format("on" if self.save else "off"), "black")
        self.currentImage = image
        self.photo_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(640, 360, image=self.photo_image)

    def save_frames(self, startFrame, stopFrame):
        for frame in range(startFrame, stopFrame + 1):
            image = self._get_white_surface()  # cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720)
            for obj in self.list.get_list():
                obj.draw(frame, image)
            print("saving frame: {}".format(frame))
            self._save_frame(image, frame, self.language)

    def set_language(self, language):
        self.language = language
        for obj in self.list.get_list():
            obj.set_language(language)

    def list_modules(self):
        self.list.print_list()

    def _save_frame(self, surface, frame, language):
        if language == Languages.ENGLISH:
            language_sting = "english"
        elif language == Languages.SPANISH:
            language_sting = "spanish"
        elif language == Languages.GERMAN:
            language_sting = "german"
        surface.write_to_png("./frames/{}/frame{}.png".format(language_sting, frame))

    def _get_white_surface(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720)
        context = cairo.Context(surface)
        context.rectangle(0, 0, 1280, 720)
        context.set_source_rgb(1, 1, 1)
        context.fill()
        return surface
