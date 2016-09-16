import cairo
import math

import Tools.helpers as Helpers
import Tools.transitions as Transitions
from Tools.frontender import Languages, evolve_base
from Tools.phrases import TextTRenderer
from Tools.tools import Line


class still:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 450 + 60
        self.image = cairo.ImageSurface.create_from_png("./images/dreaming.png")

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        context = cairo.Context(image)
        context.set_source_surface(self.image)
        context.paint()


class text:
    def __init__(self, start, duration, phrases):
        self.startTime = start
        self.stopTime = start + duration
        self.phrases = phrases
        self.phrase = phrases[Languages.ENGLISH]

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        context = cairo.Context(image)
        factor = self.phrase[1]
        context.translate(750, 60)
        context.set_source_surface(self.phrase[0](int(idx * factor)))
        context.paint()

    def set_language(self, language):
        if language == Languages.ENGLISH:
            self.phrase = self.phrases[Languages.ENGLISH]
        elif language == Languages.SPANISH:
            self.phrase = self.phrases[Languages.SPANISH]


class apple:
    def __init__(self, start, stop, position):
        self.startTime = start
        self.stopTime = stop
        self.position = position
        self.image = cairo.ImageSurface.create_from_png("./images/apple.png")

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        sz = min(idx, 35)
        if sz == 0:
            return
        context = cairo.Context(image)
        context.translate(self.position[0] - sz / 2, self.position[1])
        scale_h = 1. * sz / self.image.get_height()
        scale_w = 1. * sz / self.image.get_width()
        context.scale(scale_w, scale_h)
        context.set_source_surface(self.image)
        context.paint()


class lupa:
    def __init__(self, start, stop, positionsAndPhrases):
        self.startTime = start
        self.stopTime = stop
        self.language = Languages.ENGLISH
        self.positionsAndPhrases = positionsAndPhrases
        self.lupa = cairo.ImageSurface.create_from_png("./images/lupa.png")
        # self.mask = Image.open("./images/mask.png").convert("L")
        self.base = cairo.ImageSurface.create_from_png("./images/dreaming.png")
        self.apple = cairo.ImageSurface.create_from_png("./images/apple.png")

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        [idx1, idx2] = divmod(idx, 40)
        k = math.pow(math.sin(math.pi / 2. * idx2 / 39.), 12 if idx1 != 0 else 1)
        if idx1 + 2 > len(self.positionsAndPhrases):
            x = self.positionsAndPhrases[int(idx1)][0][0]
            y = self.positionsAndPhrases[int(idx1)][0][1]
        else:
            x = int((1 - k) * self.positionsAndPhrases[int(idx1)][0][0] + k * (
                self.positionsAndPhrases[int(idx1 + 1)][0][0]))
            y = int((1 - k) * self.positionsAndPhrases[int(idx1)][0][1] + k * (
                self.positionsAndPhrases[int(idx1 + 1)][0][1]))
        context = cairo.Context(image)
        context.arc(x, y, 218, 0, 2 * math.pi)
        context.clip()
        context.translate(-4 * x, -4 * y)
        context.scale(5, 5)
        context.set_source_surface(self.base)
        context.paint()
        for positionAndPhrase in self.positionsAndPhrases:
            ax = positionAndPhrase[0][0]
            ay = positionAndPhrase[0][1]
            textMasks = positionAndPhrase[1]
            if textMasks != None:
                textMask = textMasks[self.language]
                pos = (-5 * (x - ax) + x, -5 * (y - ay) + y)
                context = cairo.Context(image)
                context.arc(x, y, 218, 0, 2 * math.pi)
                context.clip()
                context.save()
                context.translate(pos[0] - 350 / 2., pos[1] - 350 / 2.)
                context.scale(2, 2)
                context.set_source_surface(self.apple)
                context.paint()
                context.restore()
                context.translate(pos[0] - textMask.get_width() / 2., pos[1] - textMask.get_height() / 2. + 20)
                context.set_source_surface(textMask)
                context.paint()
        context = cairo.Context(image)
        context.translate(x - 254, y - 244)
        context.set_source_surface(self.lupa)
        context.paint()

    def set_language(self, language):
        self.language = language


class evolve(evolve_base):
    renderer = TextTRenderer()
    font = "Calibri"
    text_english = [u"In just 1.5 years, the ", u"Region's women and", u"PSYDEH have used citizen",
                    u"education training and", u"community organizing",
                    u"to dismantle walls and", u"plant seeds. Now they", u"work  to harvest the fruits."]
    text_spanish = [u"En solo un a\u00f1o y medio,", u"las mujeres ind\u00edgenas", u"de la Regi\u00f3n y PSYDEH",
                    u"han desmantelado las", u"paredes, plantado", u"semillas y sue\u00f1an con",
                    u"los frutos que brotar\u00e1n."]

    phrase1 = {Languages.ENGLISH: [renderer.makeImage_runnable(text_english, font, 34, 46), 1.0],
               Languages.SPANISH: [renderer.makeImage_runnable(text_spanish, font, 34, 46),
                                   Helpers.getLetterRatio(text_english, text_spanish)]}

    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 430 + 60
        self.list = []
        positions = [(600, 950), (400, 237), (600, 333), (396, 380), (568, 193), (529, 352), (663, 238),
                     (409, 304)]  # ,(723,372)]
        phrases = [None]

        phrases.append({Languages.ENGLISH: [u"Sustainable", u"economic", u"development"],
                        Languages.SPANISH: [u"Desarrollo", u"econ\u00f3mico", u"sustentable."]})
        phrases.append({Languages.ENGLISH: [u"Education", u"that", u"empowers"],
                        Languages.SPANISH: [u"Educaci\u00f3n", u"que", u"fortalece."]})
        phrases.append({Languages.ENGLISH: [u"Protected rights", u"and", u"justice"],
                        Languages.SPANISH: [u"Protecci\u00f3n de", u"derechos y justicia."]})
        phrases.append({Languages.ENGLISH: [u"Gender", u"equalty"],
                        Languages.SPANISH: [u"Relaciones saludables", u"entre mujeres", u"y hombres."]})
        phrases.append(
            {Languages.ENGLISH: [u"Responsible", u"government"], Languages.SPANISH: [u"Gobierno", u"responsable."]})
        phrases.append(
            {Languages.ENGLISH: [u"Protected", u"environment"], Languages.SPANISH: [u"Medio ambiente", u"protegido."]})
        phrases.append({Languages.ENGLISH: [u"Quality", u"health", u"care"],
                        Languages.SPANISH: [u"Sistema", u"de salud", u"de calidad."]})
        # phrases.append(["umbrella network","of","local NGOs"])
        self.list.append(still(start))
        self.list.append(text(start, 430 + 60, self.phrase1))

        self.list.append(Line(start + 79-20, start + 79 -20 + 7, (1098, 185 + 4), (1216, 185 + 4)))
        #self.list.append(Line(start + 86, start + 86 + 9, (752 - 3, 277 + 4), (930 + 3, 277 + 4)))
        #self.list.append(Line(start + 96, start + 96 + 8, (944 - 3, 277 + 4), (1083 + 3, 277 + 4)))
        self.list.append(Line(start + 86-20, start + 96 -20 + 8, (752 - 3, 231 + 4), (1083 + 3, 231 + 4)))

        #self.list.append(Line(start + 109, start + 109 + 8, (753 - 3, 323 + 4), (957 + 3, 323 + 4)))
        #self.list.append(Line(start + 118, start + 118 + 10, (970 - 3, 323 + 4), (1154 + 3, 323 + 4)))
        self.list.append(Line(start + 108-20, start + 118 -20+ 10, (753 - 3, 277 + 4), (1154 + 3, 277 + 4)))

        self.list.append(apple(start + 70, start + 410 + 60, positions[1]))  # could put the commands into a loop
        self.list.append(apple(start + 75, start + 410 + 60, positions[2]))
        self.list.append(apple(start + 80, start + 410 + 60, positions[3]))
        self.list.append(apple(start + 85, start + 410 + 60, positions[4]))
        self.list.append(apple(start + 90, start + 410 + 60, positions[5]))
        self.list.append(apple(start + 95, start + 410 + 60, positions[6]))
        # self.list.append(apple(start + 100, start + 450, positions[7] ))
        self.list.append(lupa(start + 110 + 60, start + 430 + 60, self.zipper(positions, phrases)))

        self.list.append(
            Transitions.pageFlip(cairo.ImageSurface.create_from_png("./sequences/stillworkin/frame0.png"),
                                 None, start + 410 + 60, 20, True))

    def zipper(self, a, b):
        retArray = []
        for pos, texts in zip(a, b):
            l_dict = {}
            if texts == None:
                retArray.append([pos, None])
            else:
                for language in Languages.list_of_languages:
                    l_dict[language] = self.renderer.makeImage_centered(texts[language], "sans", 20, 30,
                                                                        color=(1, 1, 1))
                retArray.append([pos, l_dict])
        return retArray
