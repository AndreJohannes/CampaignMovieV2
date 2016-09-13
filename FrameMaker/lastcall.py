import cairo
import math

from Tools.phrases import TextTRenderer
from Tools.frontender import Languages, evolve_base
import Tools.transitions as Transitions

class still:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 230
        self.image = cairo.ImageSurface.create_from_png("./sequences/pensombre/base.png")

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        context = cairo.Context(image)
        context.set_source_surface(self.image)
        context.paint()


class bubble:
    def __init__(self, startTime):
        self.startTime = startTime

    def draw(self, frame, im):
        if frame < self.startTime:
            return
        # idx = frame - self.startTime
        radius_x = 600
        radius_y = 320
        pos_x = 640
        pos_y = 360
        context = cairo.Context(im)
        context.set_source_rgb(0., 0., 0.)
        context.set_line_width(3)
        for grad in range(0, 360):
            dr = 20 * math.pow(math.sin(2 * grad / 180. * math.pi), 2)
            x = (dr + radius_x) * math.sin(grad / 180. * math.pi)
            y = (dr + radius_y) * math.cos(grad / 180. * math.pi)
            if grad == 0:
                context.move_to(pos_x + x, pos_y + y)
            else:
                context.line_to(pos_x + x, pos_y + y)

        context.close_path()
        context.stroke_preserve()
        context.set_source_rgba(1, 1, 180 / 255., 230 / 255.)
        context.fill()


class text:
    def __init__(self, start, duration, fading, phrases):
        self.startTime = start
        self.stopTime = start + duration + fading
        self.duration = duration
        self.fading = fading
        self.phrases = phrases
        self.phrase = phrases[Languages.ENGLISH]

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        if idx > self.duration:
            alpha = (1. - (idx - self.duration) / (self.fading - 1.))
            # textMask = self.phrase(idx)
            # textMask2 = Image.new("L", textMask.size, "black")
            # textMask2.paste((color), (0, 0), textMask)
            # image.paste("black", (620 - textMask2.size[0] / 2, int(165 - 0 * idx)), textMask2)
        else:
            alpha = 1
            # textMask = self.phrase(idx)
            # image.paste("black", (620 - textMask.size[0] / 2, int(165 - 0 * idx)), textMask)

        context = cairo.Context(image)
        context.translate(620 - self.phrase(idx).get_width() / 2, int(205 - 0 * idx))
        context.set_source_surface(self.phrase(idx))
        context.paint_with_alpha(alpha)

    def set_language(self, language):
        ':type language: languages'
        if language == Languages.ENGLISH:
            self.phrase = self.phrases[Languages.ENGLISH]
        elif language == Languages.SPANISH:
            self.phrase = self.phrases[Languages.SPANISH]


class smile:
    def __init__(self):
        pass

    def draw(self, frame, image):
        context = cairo.Context(image)
        context.rectangle(620, 435, 810 - 620, 485 - 435)
        context.clip()
        im = cairo.ImageSurface.create_from_png("./images/smile.png")
        context.set_source_surface(im)
        context.paint()


class evolve(evolve_base):
    renderer = TextTRenderer()
    font = "Calibri"
    text_english = [u"Invest in indigeneous women in Mexico.", "             ",
                    u"Support these three outcomes.", "             ",
                    u"Create opportunities for all!"]
    text_spanish = [u"Acomp\u00e1\u00f1anos a derribar las paredes.", "             ",
                    u"Apoya estos tres proyectos.", "             ",
                    u"Ay\u00fadanos a que nuestro \u00e1rbol crezca.", "         ",
                    u"    \u00a1Los ciudadanos del mundo prosperan en colaboraci\u00f3n!"]

    phrase1 = {Languages.ENGLISH: renderer.makeImage_centered_runnable(text_english, font, 35, 60),
               Languages.SPANISH: renderer.makeImage_centered_runnable(text_spanish, font, 35, 60)}

    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 230
        self.list = []
        self.list.append(still(start))
        # self.list.append(bezier.evlove(start))
        self.list.append(smile())
        self.list.append(bubble(start))
        self.list.append(text(start, 180, 50, self.phrase1))
        self.list.append(Transitions.blender(None, cairo.ImageSurface.create_from_png("./images/final.png"), start + 210, 20))
