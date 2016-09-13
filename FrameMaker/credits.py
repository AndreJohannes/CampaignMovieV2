import cairo

from Tools.frontender import evolve_base, Languages
from Tools.phrases import TextTRenderer


class still:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 200
        self.image = cairo.ImageSurface.create_from_png("./images/credits.png")

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        context = cairo.Context(image)
        context.set_source_surface(self.image)
        context.paint()

class text:
    def __init__(self, start, duration, phrases, position):
        self.startTime = start
        self.stopTime = start + duration
        self.duration = duration
        self.phrases = phrases
        self.phrase = phrases[Languages.ENGLISH]
        self.position = position

    #def draw(self, frame, image):
    #    if (frame < self.startTime or frame >= self.stopTime):
    #        return
    #    textMask = self.phrase(1000)
    #    image.paste("white", (640 - textMask.size[0] / 2, self.position), textMask)

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        context = cairo.Context(image)
        context.translate(640-self.phrase.get_width()/2., self.position)
        context.set_source_surface(self.phrase)
        context.paint()
        if idx==0:
            image.write_to_png("./images/credits_english.png")

    def set_language(self, language):
        if language == Languages.ENGLISH:
            self.phrase = self.phrases[Languages.ENGLISH]
        elif language == Languages.SPANISH:
            self.phrase = self.phrases[Languages.SPANISH]

class evolve(evolve_base):
    renderer = TextTRenderer()
    font = "Calibri"
    text_english = [u"CITIZENS ARE STRONGER TOGETHER!"]
    text_spanish = [u"CIUDADANOS PROPSERAN EN COLABORACI\u00d3N"]

    phrase1 = {Languages.ENGLISH: renderer.makeImage_centered(text_english, font, 34, 46, color=(1, 1, 1)),
               Languages.SPANISH: renderer.makeImage_centered(text_spanish, font, 34, 46, color=(1, 1, 1))}

    text_english = [u"Background song \"Learn to Live With What You're Not\" by Steve",
                    u"Combs has been slightly edited and available for public sharing and",
                    u"adaptation from freemusicarchive.org under an Adaptation License."]
    text_spanish = [u"Canci\u00f3n en el fondo \"Learn to Live With What You're Not\" por Steve Combs ha sido",
                    u"ligeramente editada y est\u00e1 disponible para compartirse p\u00fablicamente y adaptada por",
                    u"Freemusicarchive.org bajo una Licencia de adaptacion."]

    phrase2 = {Languages.ENGLISH: renderer.makeImage_centered(text_english, font, 18, 26, color=(1, 1, 1)),
               Languages.SPANISH: renderer.makeImage_centered(text_spanish, font, 18, 26, color=(1, 1, 1))}

    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 200
        self.list = []
        self.list.append(still(start))
        self.list.append(text(start, 200, self.phrase1, 460))
        self.list.append(text(start, 200, self.phrase2, 620))
