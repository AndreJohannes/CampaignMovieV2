import cairo

import Tools.tools as Tools
from Tools.frontender import Languages, evolve_base
from Tools.phrases import TextTRenderer


class flag:
    def __init__(self, startTime, stopTime, flag, pos_x, pos_y):
        self.image = flag
        self.startTime = startTime
        self.stopTime = stopTime + 1
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.counter = 0

    def draw(self, frame, image):
        if frame >= self.startTime and frame < self.stopTime:
            color = min(255, (frame - self.startTime) * 30) / 255.
            context = cairo.Context(image)
            context.translate(self.pos_x, self.pos_y)
            context.set_source_surface(self.image)
            context.paint_with_alpha(color)


class background:
    def __init__(self, start):
        self.startTime = start

    def draw(self, frame, surface):
        if (frame < self.startTime):
            return
        pattern = cairo.SurfacePattern(cairo.ImageSurface.create_from_png("./sequences/wall/frame{}.png".format(16)))
        context = cairo.Context(surface)
        context.set_source(pattern)
        context.rectangle(0, 0, 1280, 720)
        context.paint()
        radius_x = 315
        offset_y = int(0.75 * radius_x)
        pos_x = 640
        pos_y = (360 + offset_y)
        context = cairo.Context(surface)
        context.set_source_rgb(0., 0., 0.)
        context.move_to(pos_x - radius_x, pos_y)
        context.line_to(pos_x + radius_x, pos_y)
        context.set_line_width(8.46666)
        context.stroke()


class evolve(evolve_base):
    font = "alphabetized cassette tapes"
    size = 36
    renderer = TextTRenderer()
    phrase1 = {Languages.ENGLISH: renderer.makeImage([u"Build a wall?", u"     Really?"], font, size),
               Languages.SPANISH: renderer.makeImage([u"\u00bfConstruimos una pared?", u"     \u00bfEn serio?"], font,
                                                     size),
               Languages.GERMAN: renderer.makeImage([u"Wir errichten eine Mauer?", u"  Wirklich?"], font, size)}
    phrase2 = {Languages.ENGLISH: renderer.makeImage([u"What are people like", u"on the other side?"], font, size),
               Languages.SPANISH: renderer.makeImage([u"\u00bfComo es la gente", u"del otro lado?"], font, size),
               Languages.GERMAN: renderer.makeImage([u"Wie sind die Leute", u"auf der anderen Seite?"], font, size)}
    phrase3 = {Languages.ENGLISH: renderer.makeImage([u"American"], font, size),
               Languages.SPANISH: renderer.makeImage([u"Americano"], font, size),
               Languages.GERMAN: renderer.makeImage([u"Amerikaner"], font, size)}
    phrase4 = {Languages.ENGLISH: renderer.makeImage([u"Mexican"], font, size),
               Languages.SPANISH: renderer.makeImage([u"Mexicano"], font, size),
               Languages.GERMAN: renderer.makeImage([u"Mexikaner"], font, size)}
    phrase5 = {Languages.ENGLISH: renderer.makeImage([u"Latinos, Europeans", u"  or Asians"], font, size),
               Languages.SPANISH: renderer.makeImage([u"Latinos, Europeos", u"  o Asi\u00e1ticos"], font, size),
               Languages.GERMAN: renderer.makeImage([u"Latinos, Europ\u00e4er", u"oder Asiaten"], font, size)}
    phrase6 = {Languages.ENGLISH: renderer.makeImage([u"Are we so", u"different?"], font, size),
               Languages.SPANISH: renderer.makeImage([u"Somos tan", u"diferentes"], font, size),
               Languages.GERMAN: renderer.makeImage([u"Wir sind so", u"verschieden"], font, size)}

    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 270
        self.list = []
        self.list.append(background(start))
        self.list.append(Tools.OneThought(start + 0, self.phrase1, 350))
        self.list.append(Tools.OneThought(start + 30, self.phrase2, 900))
        self.list.append(Tools.OneThought(start + 60, self.phrase3, 350))
        self.list.append(Tools.OneThought(start + 90, self.phrase4, 900))
        self.list.append(Tools.OneThought(start + 120, self.phrase5, 350))
        self.list.append(Tools.OneThought(start + 150, self.phrase6, 900))

        self.list.append(
            flag(start + 100, start + 170, cairo.ImageSurface.create_from_png("./Flags/america.png"), 406, 346))
        self.list.append(
            flag(start + 130, start + 200, cairo.ImageSurface.create_from_png("./Flags/mexican.png"), 776, 346))
        self.list.append(
            flag(start + 150, start + 200, cairo.ImageSurface.create_from_png("./Flags/mexican.png"), 406, 346))
        self.list.append(
            flag(start + 170, start + 230, cairo.ImageSurface.create_from_png("./Flags/australia.png"), 406, 346))
        self.list.append(
            flag(start + 190, start + 260, cairo.ImageSurface.create_from_png("./Flags/spanish.png"), 406, 346))
        self.list.append(
            flag(start + 210, start + 300, cairo.ImageSurface.create_from_png("./Flags/china.png"), 406, 346))
        self.list.append(
            flag(start + 175, start + 245, cairo.ImageSurface.create_from_png("./Flags/british.png"), 776, 346))
        self.list.append(
            flag(start + 195, start + 275, cairo.ImageSurface.create_from_png("./Flags/ecuador.png"), 776, 346))
        self.list.append(
            flag(start + 215, start + 315, cairo.ImageSurface.create_from_png("./Flags/brazil.png"), 776, 346))
        self.list.append(
            Tools.ThoughtfulTransition(start + 180,
                                       cairo.ImageSurface.create_from_png("./sequences/pensombre/base.png"), 350))
