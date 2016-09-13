import cairo

import Tools.helpers as Helpers
import Tools.transitions as Transitions
from Tools.frontender import evolve_base, Languages
from Tools.phrases import TextTRenderer


class transition:
    def __init__(self, start):
        self.start = start
        self.transition = Transitions.blender(None, cairo.ImageSurface.create_from_png("./images/credits_english.png"),
                                              self.start, 40)

    def draw(self, frame, image):
        if frame < self.start:
            return
        self.transition.draw(frame, image)

    def set_language(self, language):
        ':type language: languages'
        if language == Languages.ENGLISH:
            self.transition = Transitions.blender(None, cairo.ImageSurface.create_from_png("./images/credits_english.png"),
                                                  self.start, 40)
        elif language == Languages.SPANISH:
            self.transition = Transitions.blender(None,
                                                  cairo.ImageSurface.create_from_png("./images/credits_spanish.png"),
                                                  self.start, 40)


class still:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 265
        self.image = cairo.ImageSurface.create_from_png("./images/final.png")

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        context = cairo.Context(image)
        context.set_source_surface(self.image)
        context.paint()


class color_text:
    def __init__(self, start, duration, phrases, position):
        self.startTime = start
        self.stopTime = start + duration
        self.duration = duration
        self.phrases = phrases
        self.phrase = phrases[Languages.ENGLISH]
        self.position = position
        self.pos_org = position

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        context = cairo.Context(image)
        context.translate(self.position[0], self.position[1])
        context.set_source_surface(self.phrase[0](idx))
        context.paint()

    def set_language(self, language):
        ':type language: languages'
        if language == Languages.ENGLISH:
            self.phrase = self.phrases[Languages.ENGLISH]
            self.position = self.pos_org
        elif language == Languages.SPANISH:
            self.phrase = self.phrases[Languages.SPANISH]
            self.position = (self.pos_org[0] + 210, self.pos_org[1])


class text:
    def __init__(self, start, duration, phrases, position):
        self.startTime = start
        self.stopTime = start + duration
        self.duration = duration
        self.phrases = phrases
        self.phrase = phrases[Languages.ENGLISH]
        self.position = position

    def draw(self, frame, image):
        if frame < self.startTime or frame >= self.stopTime:
            return
        idx = frame - self.startTime
        factor = self.phrase[1]
        context = cairo.Context(image)
        context.translate(self.position[0], self.position[1])
        context.set_source_surface(self.phrase[0](int(idx * factor)))
        context.paint()

    def set_language(self, language):
        ':type language: languages'
        if language == Languages.ENGLISH:
            self.phrase = self.phrases[Languages.ENGLISH]
        elif language == Languages.SPANISH:
            self.phrase = self.phrases[Languages.SPANISH]


class evolve(evolve_base):
    renderer = TextTRenderer()
    font = "Calibri"
    text_english = [u"PSYDEH and Global Citizens:", u"Joining indigenous women in",
                    u"building self-reliant communities."]
    text_spanish = [u"PSYDEH y Ciudadanos del Mundo:", u"Derrumbando paredes y plantando arboles",
                    u"junto con nuestros socios ind\u00EDgenas en M\u00e9xico."]
    phrase1 = {Languages.ENGLISH: [renderer.makeImage_runnable(text_english, font, 34, 50), 1.0],
               Languages.SPANISH: [renderer.makeImage_runnable(text_spanish, font, 34, 50),
                                   Helpers.getLetterRatio(text_english, text_spanish)]}
    text_english = [u"Visit PSYDEH's website for more", u"information: "]
    text_spanish = [u"Para m\u00e1s informaci\u00f3n visita la", u"p\u00e1gina web de PSYDEH: "]
    phrase2 = {Languages.ENGLISH: [renderer.makeImage_runnable(text_english, font, 34, 50), 1.0],
               Languages.SPANISH: [renderer.makeImage_runnable(text_spanish, font, 34, 50),
                                   Helpers.getLetterRatio(text_english, text_spanish)]}

    font = "Calibri Bold"
    text_english = [u"Invest in our fruits of change campaign."]
    text_spanish = [u"www.psydeh.com"]
    phrase3 = {Languages.ENGLISH: [
        renderer.makeImage_runnable(text_english, font, 40, 55, color=(80 / 255., 147 / 255., 205 / 255.)), 1.0],
        Languages.SPANISH: [
            renderer.makeImage_runnable(text_spanish, font, 34, 50, color=(80 / 255., 147 / 255., 205 / 255.)),
            Helpers.getLetterRatio(text_english, text_spanish)]}

    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 280
        self.list = []
        self.list.append(still(start))
        self.list.append(text(start, 265, self.phrase1, (310, 50)))
        #self.list.append(text(start + 92, 195, self.phrase2, (310, 600)))
        self.list.append(
            color_text(start + 92 + 0*44, 195, self.phrase3, (310 -100+ 0*252, 600 +25+ 0*50)))
        self.list.append(transition(start + 240))
