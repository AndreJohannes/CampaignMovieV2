import cairo
from Tools.phrases import TextTRenderer
import Tools.helpers as Helpers
from Tools.frontender import Languages, evolve_base

class labour:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 100

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        im = cairo.ImageSurface.create_from_png("./sequences/stillworkin/frame{}.png".format(idx))
        context = cairo.Context(image)
        context.set_source_surface(im)
        context.paint()


class slider:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 100

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        base = cairo.ImageSurface.create_from_png("./sequences/stillworkin/frame{}.png".format(idx + 100))
        im = cairo.ImageSurface.create_from_png("./sequences/pensombre/slider/image{:02d}.png".format(25 - idx))
        context = cairo.Context(image)
        context.set_source_surface(im)
        context.paint()
        dic = {10: 1221, 11: 1196, 12: 1153, 13: 1096, 14: 1022, 15: 952, 16: 874, 17: 797, 18: 724, 19: 646, 20: 562,
               21: 476, 22: 391, 23: 297, 24: 208, 25: 80}
        if (dic.has_key(25 - idx)):
            context = cairo.Context(image)
            context.set_source_surface(base)
            context.rectangle(dic[25-idx], 0, 1280, 720)
            context.fill()


class text:
    def __init__(self, start, phrases):
        self.startTime = start
        self.stopTime = start + 125
        self.phrases = phrases
        self.lanaguage = Languages.ENGLISH
        self.phrase = phrases[Languages.ENGLISH]

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        if idx > 100:
            alpha = (1. - (idx - 100) / (25.))
        else:
            alpha = 1
        context = cairo.Context(image)
        factor = self.phrase[1]
        context.translate(65, 300 - idx*(2 if self.lanaguage==Languages.SPANISH else 1))
        context.set_source_surface(self.phrase[0](int(idx * factor)))
        context.paint_with_alpha(alpha)


    def set_language(self, language):
        ':type language: languages'
        self.lanaguage = language
        if language == Languages.ENGLISH:
            self.phrase = self.phrases[Languages.ENGLISH]
        elif language == Languages.SPANISH:
            self.phrase = self.phrases[Languages.SPANISH]


class evolve(evolve_base):
    renderer = TextTRenderer()
    font = "Calibri Bold"
    text_english = [u"Still, our",u"movement",u"is not strong", u"enough to", u"bear fruit."]
    text_spanish = [u"Sin embargo,",u"hasta mayo del", u"2016, nuestro", u"\u00e1rbol no", u"ha sido lo",u"suficientemente", u"fuerte para",
                    u"brotar frutos.", u"Las ra\u00edzes a\u00fan", u"son d\u00e9biles."]

    phrase1 = {Languages.ENGLISH: [renderer.makeImage_runnable(text_english, font, 42, 60), 1.0],
               Languages.SPANISH: [renderer.makeImage_runnable(text_spanish, font, 42, 60),
                                   Helpers.getLetterRatio(text_english, text_spanish)]}

    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 125
        self.list = []
        self.list.append(labour(start))
        self.list.append(slider(start + 100))
        self.list.append(text(start, self.phrase1))