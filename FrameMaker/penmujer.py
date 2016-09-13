import cairo

import Tools.tools as Tools
from Tools.frontender import evolve_base, Languages
from Tools.phrases import TextTRenderer


class OneThought:
    def __init__(self, startTime, images, pos_x, left, down=False):
        self.images = images
        self.bubble = Tools.MovingBubble(pos_x, 163, 10, startTime, 20, left, down)
        pos_x += -100 if left else 100
        self.rectangualar = Tools.MorphingTextBox(images[Languages.ENGLISH], pos_x, 139 if down is False else 243, 20,
                                                  startTime + 20, True)

    def draw(self, frame, image):
        self.bubble.draw(frame, image)
        self.rectangualar.draw(frame, image)

    def set_language(self, language):
        """:type language: languages"""
        self.rectangualar.image = self.images[language]


class pensativo:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 130

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        im = cairo.ImageSurface.create_from_png("./sequences/pensombre/pensativo/image{}.png".format(min(idx, 69)))
        context = cairo.Context(image)
        context.set_source_surface(im)
        context.paint()


class rolling_tl:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 65

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        im = cairo.ImageSurface.create_from_png(
            "./sequences/pensombre/rollingeyes/topleft/image{}.png".format(min(idx, 5)))
        context = cairo.Context(image)
        context.set_source_surface(im)
        context.rectangle(0, 0, 800, 350)
        context.clip()
        context.paint()


class rolling_tlb:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 20

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        im = cairo.ImageSurface.create_from_png(
            "./sequences/pensombre/rollingeyes/topleft/image{}.png".format(max(5 - idx, 0)))
        context = cairo.Context(image)
        context.set_source_surface(im)
        context.rectangle(0, 0, 800, 350)
        context.clip()
        context.paint()


class slider:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 26

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return

        idx = frame - self.startTime
        base = cairo.ImageSurface.create_from_png(
            "./sequences/pensombre/slider/image" + "{:02d}".format(max(min(idx, 26), 0)) + ".png")
        context = cairo.Context(image)
        context.set_source_surface(base)
        context.paint()
        dic = {10: 1221, 11: 1196, 12: 1153, 13: 1096, 14: 1022, 15: 952, 16: 874, 17: 797, 18: 724, 19: 646, 20: 562,
               21: 476, 22: 391, 23: 297, 24: 208, 25: 80}
        if (dic.has_key(idx)):
            pass
            context = cairo.Context(image)
            base2 = cairo.ImageSurface.create_from_png("./images/base3.png")
            context.set_source_surface(base2)
            context.rectangle(dic[idx], 0, 1280, 720)
            context.fill()
            # mask = Image.new("L", (1280, 720), "white")
            # mask.paste("black", (0, 0, dic[idx], 720))
            # image.paste(base2, (0, 0), mask)


class evolve(evolve_base):
    font = "alphabetized cassette tapes"
    size = 36
    renderer = TextTRenderer()
    phrase1 = {Languages.ENGLISH: renderer.makeImage([u"If I could remove", u"blocks from the wall...?"], font, size),
               Languages.SPANISH: renderer.makeImage([u"\u00bfSi pudiera quitar los", u"ladrillos de la pared...?"],
                                                     font, size),
               Languages.GERMAN: renderer.makeImage(
                   [u"Wenn ich nur die Ziegel von", u"der Wand nehmen k\u00f6nnte...?"],
                   font, size)}
    phrase2 = {
        Languages.ENGLISH: renderer.makeImage([u"AND if the man on the", u"other side does the same..."], font,
                                              size),
        Languages.SPANISH: renderer.makeImage([u"Y si la persona del", u"otro lado hiciera lo mismo..."], font, size),
        Languages.GERMAN: renderer.makeImage([u"UND wenn die Person auf der", u"anderen Seite das gleiche tut...."],
                                             font, size)}
    phrase3 = {Languages.ENGLISH: renderer.makeImage([u"We can",u"all prosper!"], font, size),
               Languages.SPANISH: renderer.makeImage([u"\u00a1De hecho podemos", u"crecer sustentablemente!"], font,
                                                     size),
               Languages.GERMAN: renderer.makeImage(
                   [u"Koennen wir tats\u00e4chlich", u"etwas nachhaltiges erschaffen!"],
                   font, size)}

    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 156
        self.list = []
        self.list.append(pensativo(start))
        self.list.append(rolling_tl(start + 10))
        self.list.append(rolling_tlb(start + 75))
        self.list.append(slider(start + 130))
        self.list.append(OneThought(start + 0, self.phrase1, 500, True))
        self.list.append(OneThought(start + 30, self.phrase2, 877, False))
        self.list.append(OneThought(start + 60, self.phrase3, 500, True, True))
