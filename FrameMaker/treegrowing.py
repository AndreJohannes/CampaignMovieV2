import cairo

import Tools.helpers as Helpers
import Tools.transitions as Transitions
from Tools.frontender import Languages, evolve_base
from Tools.phrases import TextTRenderer


class seednwater:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 72

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        context = cairo.Context(image)
        surface = cairo.ImageSurface.create_from_png(
            "./sequences/seednwater/frame{}.png".format(min(idx, 71)))
        context.set_source_surface(surface)
        context.paint()


class growing:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 241

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        idx = frame - self.startTime
        context = cairo.Context(image)
        surface = cairo.ImageSurface.create_from_png(
            "./sequences/tree/frame{}.png".format(min(int(5 / 3. * idx * (1. - 1 / 480. * idx)), 200)))
        context.set_source_surface(surface)
        context.paint()


class text:
    def __init__(self, start, duration, fading, phrases, scrolling_speed=1):
        self.startTime = start
        self.stopTime = start + duration + fading
        self.duration = duration
        self.fading = fading
        self.phrases = phrases
        self.phrase = phrases[Languages.ENGLISH]
        self.speed = scrolling_speed

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        context = cairo.Context(image)
        factor = self.phrase[1]
        context.translate(65, 300 - int(self.speed * idx))
        context.set_source_surface(self.phrase[0](int(idx * factor)))
        alpha = (1. - (idx - self.duration) / (self.fading - 1.)) if idx >= self.duration else 1
        context.paint_with_alpha(alpha)

    def set_language(self, language):
        ':type language: languages'
        if language == Languages.ENGLISH:
            self.phrase = self.phrases[Languages.ENGLISH]
        elif language == Languages.SPANISH:
            self.phrase = self.phrases[Languages.SPANISH]


class evolve(evolve_base):
    renderer = TextTRenderer()
    font = "Calibri Bold"
    text_english = [u"Where walls once existed, indigenous women",
                    u"unite around a strong, growing tree."]
    text_spanish = [u"En donde las paredes alguna vez existieron,",
                    u"las semillas se plantan y un \u00e1rbol crece."]

    phrase1 = {Languages.ENGLISH: [renderer.makeImage_runnable(text_english, font, 42, 60), 1.0],
               Languages.SPANISH: [renderer.makeImage_runnable(text_spanish, font, 42, 60),
                                   Helpers.getLetterRatio(text_english, text_spanish)]}

    text_english = [u"This tree", u"symbolizes", u"our work", u"to empower", u"sustainable", u"development."]
    text_spanish = [u"Este \u00e1rbol,", u"simboliza nuestro", u"trabajo y nuestra",
                    u"met\u00e1fora de", u"sustentabilidad.",
                    ]

    phrase2 = {Languages.ENGLISH: [renderer.makeImage_runnable(text_english, font, 42, 60), 1.0],
               Languages.SPANISH: [renderer.makeImage_runnable(text_spanish, font, 42, 60),
                                   Helpers.getLetterRatio(text_english, text_spanish)]}

    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 333
        self.list = []
        self.list.append(seednwater(start))
        self.list.append(growing(start + 72))
        self.list.append(text(start + 72, 70, 50, self.phrase1))
        self.list.append(text(start + 194, 70, 50, self.phrase2, scrolling_speed=2))
        self.list.append(
            Transitions.pageFlip(cairo.ImageSurface.create_from_png("./sequences/tree/frame200.png"),
                                 cairo.ImageSurface.create_from_png("./images/dreaming.png"),
                                 start + 313, 20))
