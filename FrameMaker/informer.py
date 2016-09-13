import cairo
import math

import Tools.helpers as Helpers
import Tools.transitions as Transitions
from Tools.frontender import evolve_base, Languages
from Tools.phrases import TextTRenderer
from Tools.tools import Line


class image:
    def __init__(self, start, duration, image):
        self.startTime = start
        self.stopTime = start + duration
        self.duration = duration
        self.image = image

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        context = cairo.Context(image)
        context.set_source_surface(self.image)
        context.paint()


class text:
    def __init__(self, start, duration, fading, phrases, pos_y=300, text_addons=None):
        self.startTime = start
        self.stopTime = start + duration + fading
        self.duration = duration
        self.fading = fading
        self.phrases = phrases
        self.phrase = phrases[Languages.ENGLISH]
        self.pos_y = pos_y
        self.text_addons = text_addons

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        context = cairo.Context(image)
        factor = self.phrase[1]
        context.translate(65, int(self.pos_y - 1.5 * idx * factor))

        text_surface = self.phrase[0](int(idx * factor))
        if self.text_addons is not None:
            for addon in self.text_addons:
                addon.draw(idx, text_surface)

        context.set_source_surface(text_surface)
        alpha = (1. - (idx - self.duration) / (self.fading - 1.)) if idx >= self.duration else 1
        context.paint_with_alpha(alpha)

    def set_language(self, language):
        if language == Languages.ENGLISH:
            self.phrase = self.phrases[Languages.ENGLISH]
        elif language == Languages.SPANISH:
            self.phrase = self.phrases[Languages.SPANISH]


class pullWall:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 360

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        context = cairo.Context(image)
        # surface = cairo.ImageSurface.create_from_png(
        #    "./sequences/pullWall/image{:03d}.png".format(max(0, min(135, int((idx - 120) / 2.)))))
        y = max(0, idx - 120)
        x = int(8 * (40 - math.sqrt(5 * (320 - y))))
        surface = cairo.ImageSurface.create_from_png(
            "./sequences/pullWall2/frame{}.png".format(x))
        context.set_source_surface(surface)
        idx = 0
        alpha = 1 - max(190 - 5 * max(0, idx - 120), 0) / 255.
        context.paint_with_alpha(alpha)


class handShake:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 390

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        context = cairo.Context(image)
        surface = cairo.ImageSurface.create_from_png(
            "./sequences/pullWall2/frame{}.png".format(160 + min(int((idx) / 2), 15)))
        context.set_source_surface(surface)
        idx = 1000
        alpha = 1 - min(5 * idx, 190) / 255.
        context.paint_with_alpha(alpha)


class gradient:
    def __init__(self, start):
        self.startTime = start
        # for idx in range(0, 200):
        #    draw.line((0, idx, 900, idx), fill=int(255 * max(0, idx - 150) / 50.))

    def draw(self, frame, image):
        if self.startTime > frame:
            return
        idx = frame - self.startTime
        color = min(5 * idx, 190)
        if idx > 200:
            color = max(0, 190 - 5 * (idx - 100))
        lg3 = cairo.LinearGradient(1280 / 2., 210.0, 1280 / 2., 600.0)
        lg3.add_color_stop_rgba(0.0, 1, 1, 1, color / 255.)
        lg3.add_color_stop_rgba(1.0, 1, 1, 1, 0)

        cr = cairo.Context(image)
        cr.rectangle(100.0, 210.0, 1000.0, 600.0)
        cr.set_source(lg3)
        cr.fill()

        # im = Image.new("L", (900, 200), color)
        # im.paste("black", (0, 0), self.mask)
        # image.paste("white", (100, 210), im)


class evolve(evolve_base):
    renderer = TextTRenderer()
    font = "Calibri Bold"
    text_english = [u"Despite living in isolated communities separated ",
                    u"by \"walls\", dividing community from community",
                    u"and the Region from the world, indigenous",
                    u"people work for different.",
                    u"             ",
                    u"These walls include:",
                    u"             ",
                    u"-The majority of the Region's people earn less", u"  than $85usd per month.", u"             ",
                    u"-Less than 1% of homes possess a computer.", "             ",
                    # u"Communities rarely collaborate, municipalities", u"even less.", u"             ",
                    u"-Women average three grades of schooling",
                    u"  and 9 out of 10 confront violence in", u"  their communities."]

    text_spanish = [u"La gente ind\u00edgena est\u00e1 separada.",
                    u"Se dividen comunidad de comunidad,",
                    u"municipio de municipio y la Regi\u00f3n del", u"mundo.", u"             ",
                    u"La mayor\u00eda de la gente de la regi\u00f3n", u"gana menos de $96 d\u00f3lares al mes.",
                    "             ",
                    u"Menos de 1% de los hogares posee", u"una computadora.", "             ",
                    # u"Las comunidades raramente colaboran entre", u"ellas, los municipios todav\u00eda menos.",
                    # "             ",
                    u"Las mujeres promedian solo tres", u"a\u00f1os de escolaridad."]

    phrase1 = {Languages.ENGLISH: [renderer.makeImage_runnable(text_english, font, 42, 60), 1.],
               Languages.SPANISH: [renderer.makeImage_runnable(text_spanish, font, 42, 60),
                                   Helpers.getLetterRatio(text_english, text_spanish)]}

    text_english = [u"Since 2014, an Umbrella network of 500+ Nahua,",
                    u"Otom\u00ed and Tepehua indigenous women from",
                    u"35+ communities partner with the Mexican NGO",
                    u"PSYDEH and build their own bottom-up movement.",
                    u"          ",
                    u"Their goal?",
                    u"          ",
                    u"Plant innovative \"seeds\" to advance", u"their own self-reliant communities through",
                    u"          ",
                    u"          Citizen Leader Education",
                    u"          ",
                    u"          Community Organizing"]

    text_spanish = [u"Desde 2013, las poblaciones Nahua, Otom\u00ed y",
                    u"Tepehua desaf\u00edan las paredes y construyen su",
                    u"propio movimiento social desde la base", u"piramidal con respecto a sus derechos humanos.",
                    "             ",
                    u"En colaboraci\u00f3n con la ONG mexicana PSYDEH,",
                    u"en 2014 y 2015, una red de m\u00e1s de 500 mujeres",
                    u"ind\u00edgenas de m\u00e1s de 35 comunidades plantaron",
                    u"semillas de innovaci\u00f3n para su propio futuro", u"sustentable."]

    phrase2 = {Languages.ENGLISH: [renderer.makeImage_runnable(text_english, font, 42, 60), 1.],
               Languages.SPANISH: [renderer.makeImage_runnable(text_spanish, font, 42, 60),
                                   Helpers.getLetterRatio(text_english, text_spanish)]}

    text_english = [u"These seeds: ", "             ",
                    u"   - Identify shared problems", "             ",
                    u"   - Reach clarity on solutions", "             ",
                    u"   - Adopt leader disciplines to implement", u"      solutions", "             ",
                    u"   - Exercise rights & laws on which solutions", u"      are based", "             ",
                    u"   - Assert personal & communal autonomy"]

    text_spanish = [u"Estas semillas significan aprender acerca de: ", "             ",
                    u"   - Problemas en com\u00fan", "             ",
                    u"   - Claridad en soluciones", "             ",
                    u"   - M\u00e9todos de liderazgo para implementar", u"    soluciones", "             ",
                    u"   - Derechos y leyes en los que se basan las", u"     soluciones", "             ",
                    u"   - Autonom\u00eda personal y colectiva"]

    phrase3 = {Languages.ENGLISH: [renderer.makeImage_runnable(text_english, font, 42, 60), 1.],
               Languages.SPANISH: [renderer.makeImage_runnable(text_spanish, font, 42, 60),
                                   Helpers.getLetterRatio(text_english, text_spanish)]}

    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 1170 + 50+40
        self.list = []
        self.list.append(image(start, 450, Helpers.open_image("./sequences/pullWall2/frame0.png", 190)))
        self.list.append(text(start, 400+40, 50, self.phrase1))
        self.list.append(pullWall(start + 450))
        # self.list.append(gradient(start + 450 + 120))
        text_lines = [Line(304, 304+24, (600-468-3, 700-58+3), (696+3, 700-58+3))]
        text_lines.append(Line(304+44, 304+44+20, (600-468-3, 700-58+3+120), (696-35+3, 700-58+3+120)))

        self.list.append(text(start + 450+40, 350, 50, self.phrase2, pos_y=400, text_addons=text_lines))
        self.list.append(handShake(start + 810+40))
        self.list.append(text(start + 810 + 50+40, 290, 50, self.phrase3))
        self.list.append(Transitions.horizontalFlip(Helpers.open_image("./sequences/pullWall2/frame175.png", 190),
                                                    cairo.ImageSurface.create_from_png(
                                                        "./sequences/seednwater/frame0.png"),
                                                    start + 1150 + 50+40, 20))
