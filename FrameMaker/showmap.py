import cairo

import Tools.helpers as Helpers
import Tools.transitions as Transitions
from Tools.frontender import evolve_base, Languages
from Tools.phrases import TextTRenderer


class zoom:
    def __init__(self, start, phrases):
        self.startTime = start
        self.stopTime = start + 170
        self.phrases = phrases
        self.phrase = phrases[Languages.ENGLISH]

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        context = cairo.Context(image)
        surface = cairo.ImageSurface.create_from_png(
            "./sequences/map/image{}.png".format(min(int(1.7*idx), 169)))
        context.set_source_surface(surface)
        context.paint()
        context = cairo.Context(image)
        factor = self.phrase[1]
        context.translate(50, 265)
        context.set_source_surface(self.phrase[0](int(idx * factor)))
        alpha = (1 - (idx - 100) / 69.) if idx >= 100 else 1
        context.paint_with_alpha(alpha)

    def set_language(self, language):
        self.phrase = self.phrases[language]


class zoom2:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 120

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        context = cairo.Context(image)
        surface = cairo.ImageSurface.create_from_png(
            "./sequences/map/image{}.png".format(min(idx + 390, 459)))
        context.set_source_surface(surface)
        context.paint()


class regions:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 150
        self.blenders = []
        hidalgo = cairo.ImageSurface.create_from_png("./images/map/hidalgo.png")
        mezquital = cairo.ImageSurface.create_from_png("./images/map/mezquital.png")
        huasteca = cairo.ImageSurface.create_from_png("./images/map/huasteca.png")
        otomi = cairo.ImageSurface.create_from_png("./images/map/otomi.png")
        self.blenders.append(Transitions.blender(hidalgo, mezquital, start, 25))
        self.blenders.append(Transitions.blender(mezquital, huasteca, start + 25, 25))
        self.blenders.append(Transitions.blender(huasteca, otomi, start + 50, 25))

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        for blender in self.blenders:
            blender.draw(frame, image)


class areas:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 160
        self.blenders = []
        otomi = cairo.ImageSurface.create_from_png("./images/map/otomi_close.png")
        acaxochitlan = cairo.ImageSurface.create_from_png("./images/map/acaxochitlan.png")
        tenango = cairo.ImageSurface.create_from_png("./images/map/tenango.png")
        bartolo = cairo.ImageSurface.create_from_png("./images/map/bartolo.png")
        huehuetla = cairo.ImageSurface.create_from_png("./images/map/huehuetla.png")
        self.blenders.append(Transitions.blender(otomi, acaxochitlan, start, 40))
        self.blenders.append(Transitions.blender(acaxochitlan, tenango, start + 40, 40))
        self.blenders.append(Transitions.blender(tenango, bartolo, start + 80, 40))
        self.blenders.append(Transitions.blender(bartolo, huehuetla, start + 120, 40))

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        for blender in self.blenders:
            blender.draw(frame, image)


class text2:
    def __init__(self, start, phrases):
        self.startTime = start
        self.stopTime = start + 140
        self.phrases = phrases
        self.phrase = phrases[Languages.ENGLISH]

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        context = cairo.Context(image)
        factor = self.phrase[1]
        context.translate(50, 200)
        context.set_source_surface(self.phrase[0](int(idx * factor)))
        alpha = (1 - (idx - 110) / 20.) if idx >= 110 else 1
        context.paint_with_alpha(alpha)

    def set_language(self, language):
        ':type language: languages'
        self.phrase = self.phrases[language]


class evolve(evolve_base):
    renderer = TextTRenderer()
    font = "Calibri Bold"
    # aggdraw.Font("white", "./fonts/calibrib.ttf", 56)
    text_english = [u"Hidalgo is a small state in central Mexico where",
                    u"its indigenous citizens live in three regions:"]
    text_spanish = [u"Hidalgo es un peque\u00f1o, rocoso y bello estado en",
                    u"M\u00e9xico central donde su poblacion indigena vive",
                    u"en tres regiones en las cuales el desarrollo humano",
                    u"se encuentra cerca de los m\u00e1s bajos del mundo:"]
    text_german = [u"Hidalgo ist ein kleiner, zerkl\u00fcfteter und pittoresker",
                   u"Bundesstatt im Herzen Mexikos in dem seine",
                   u"einheimische Bevoelkerung in drei Region lebt in",
                   u"denen die humane Entwicklung mit am niedrigsten",
                   u"in der Welt ist:"]

    phrase1 = {Languages.ENGLISH: [renderer.makeImage_runnable(text_english, font, 42, 60), 1.0],
               Languages.SPANISH: [renderer.makeImage_runnable(text_spanish, font, 42, 60),
                                   Helpers.getLetterRatio(text_english, text_spanish)],
               Languages.GERMAN: [renderer.makeImage_runnable(text_german, font, 42, 60),
                                  Helpers.getLetterRatio(text_english, text_german)]}

    text_english = [u"In this first stage of PSYDEH's work, ",
                    u"we focus on the Otom\u00ed-Tepehua region and",
                    u"its four majority indigenous areas:"]
    text_spanish = [u"En la regi\u00f3n Otom\u00ed-Tepehua hay cuatro \u00e1reas",
                    u"mayoritariamente ind\u00edgenas:"]
    text_german = [u"In der Region Otomi-Tepehua befinden sich 4",
                   u"mehrheitlich indigene Gebiete:"]

    phrase2 = {Languages.ENGLISH: [renderer.makeImage_runnable(text_english, font, 42, 60), 1.0],
               Languages.SPANISH: [renderer.makeImage_runnable(text_spanish, font, 42, 60),
                                   Helpers.getLetterRatio(text_english, text_spanish)],
               Languages.GERMAN: [renderer.makeImage_runnable(text_german, font, 42, 60),
                                  Helpers.getLetterRatio(text_english, text_german)]}

    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 355+160+40
        self.list = [zoom(start, self.phrase1)]
        self.list.append(regions(start + 170))
        self.list.append(zoom2(start + 245))
        self.list.append(areas(start + 355))
        self.list.append(text2(start + 245, self.phrase2))
        self.list.append(
            Transitions.blender(cairo.ImageSurface.create_from_png("./images/map/huehuetla.png"),
                                Helpers.open_image("./sequences/pullWall2/frame0.png", 190),
                                start + 355+160, 40))

