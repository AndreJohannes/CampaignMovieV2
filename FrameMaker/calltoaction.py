import cairo
import math

import Tools.tools as Tools
import Tools.transitions as Transitions
from Tools.frontender import Languages, evolve_base
from Tools.phrases import TextTRenderer


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


class emoticon:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 200
        self.eye_left = cairo.ImageSurface.create_from_png("./images/eye_left.png")
        self.eye_right = cairo.ImageSurface.create_from_png("./images/eye_right.png")

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        im = cairo.ImageSurface.create_from_png("./sequences/emotions/frame{}.png".format(min(int(idx / 2) * 2, 24)))
        context = cairo.Context(image)
        context.set_source_surface(im)
        context.paint()
        # image.paste(im, (0, 0))
        self.draw_eye(idx, image)
        self.draw_smile(idx, image)

    def draw_eye(self, idx, image):
        eye_base = cairo.ImageSurface(cairo.FORMAT_ARGB32, 55, 63)
        # center = (17, 35)
        context = cairo.Context(eye_base)
        context.rectangle(0, 0, 55, 63)
        context.set_source_rgb(1, 1, 1)
        context.fill()
        if idx > 70:
            context.arc(55 / 2., 63 / 2., 13, 0, 2 * math.pi)
        else:
            context.arc(17, 35., 13, 0, 2 * math.pi)
        context.set_line_width(0)
        context.set_source_rgb(0., 0., 0.)
        context.fill()
        if idx > 70:
            lev = 44 * math.sin(max(0, 5 - (idx - 70)) / 3.)
        else:
            lev = 44 * math.sin(min(5, max(idx - 50, 0)) / 3.)
        context.arc(27.5, -90 + lev, 100, 0, 2 * math.pi)
        context.set_line_width(1)
        context.stroke_preserve()
        context.set_source_rgb(240. / 255., 240. / 255., 240. / 255.)
        context.fill()

        eye_left = cairo.ImageSurface(cairo.FORMAT_ARGB32, 55, 63)
        context = cairo.Context(eye_left)
        context.set_source_surface(eye_base)
        context.paint()
        context.set_source_surface(self.eye_left)
        context.paint()

        eye_right = eye_base
        context = cairo.Context(eye_right)
        context.set_source_surface(self.eye_right)
        context.paint()

        context = cairo.Context(image)
        context.translate(607, 256)
        context.set_source_surface(eye_right)
        context.paint()
        context.translate(747 - 607, 2)
        context.set_source_surface(eye_left)
        context.paint()

    def draw_smile(self, idx, image):
        if idx <= 70:
            return
        context = cairo.Context(image)
        context.rectangle(620, 435, 810 - 620, 485 - 435)
        context.clip()
        im = cairo.ImageSurface.create_from_png("./images/smile.png")
        context.set_source_surface(im)
        context.paint()


class animation3D:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 275 + 70

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        im = cairo.ImageSurface.create_from_png("./sequences/unite/frame{}.png".format(min(idx, 200)))
        context = cairo.Context(image)
        context.set_source_surface(im)
        context.paint()


class bubble:
    def __init__(self, pos_x, pos_y, radius, startTime):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.startTime = startTime

    def draw(self, frame, im):
        if frame < self.startTime:
            return
        idx = frame - self.startTime
        k = min(1, 0.2 * math.sqrt(idx))
        radius_x = (1 - k) * self.radius + k * 600
        radius_y = (1 - k) * self.radius + k * 320
        pos_x = (1 - k) * self.pos_x + k * 640
        pos_y = (1 - k) * self.pos_y + k * 360
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


class OneThought:
    def __init__(self, startTime, pos_x, left):
        self.bubble = Tools.MovingBubble(pos_x, 163, 10, startTime, 20, left)
        pos_x += -100 if left else 100
        self.rectangualar = bubble(pos_x, 139, 20, startTime + 20)

    def draw(self, frame, image):
        self.bubble.draw(frame, image)
        self.rectangualar.draw(frame, image)


class leaf:
    def __init__(self, startTime, boomTime, pos_y, image):
        self.pos_y = pos_y
        self.startTime = startTime
        self.boomTime = boomTime
        self.image = image

    def draw(self, frame, image):
        if frame < self.startTime:
            return
        context = cairo.Context(image)
        if frame < self.boomTime:
            s_x = 80 / (1.0 * self.image.get_width())
            s_y = 80 / (1.0 * self.image.get_height())
            context.translate(150, self.pos_y)
            context.scale(s_x, s_y)
            context.mask_surface(self.image)
            context.set_source_rgb(0, 0, 0)
            context.fill()
        elif frame <= self.boomTime + 5:
            idx = frame - self.boomTime
            s_x = (80 + 50 * idx) / (1.0 * self.image.get_width())
            s_y = (80 + 50 * idx) / (1.0 * self.image.get_height())
            context.translate(150 - 25 * idx, self.pos_y - 25 * idx)
            context.scale(s_x, s_y)
            context.set_source_surface(self.image)
            context.paint()
        else:
            s_x = (80 + 50) / (1.0 * self.image.get_width())
            s_y = (80 + 50) / (1.0 * self.image.get_height())
            context.translate(150 - 25, self.pos_y - 25)
            context.scale(s_x, s_y)
            context.set_source_surface(self.image)
            context.paint()


class text:
    def __init__(self, start, duration, fading, phrases, position):
        self.startTime = start
        self.stopTime = start + duration + fading
        self.duration = duration
        self.fading = fading
        self.phrases = phrases
        self.phrase = phrases[Languages.ENGLISH]
        self.position = position

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        if idx > self.duration:
            alpha = (1. - (idx - self.duration) / (self.fading - 1.))
        else:
            alpha = 1

        context = cairo.Context(image)
        context.translate(640 - self.phrase(idx).get_width() / 2, self.position[1])
        context.set_source_surface(self.phrase(int(idx)))
        context.paint_with_alpha(alpha)

    def set_language(self, language):
        ':type language: languages'
        if language == Languages.ENGLISH:
            self.phrase = self.phrases[Languages.ENGLISH]
        elif language == Languages.SPANISH:
            self.phrase = self.phrases[Languages.SPANISH]


class leafText:
    def __init__(self, start, fading, phrases, position):
        self.startTime = start
        self.stopTime = start + fading + 25
        self.fading = fading
        self.phrases = phrases
        self.phrase = phrases[Languages.ENGLISH]
        self.position = position

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        if idx <= self.fading:
            color = int(255 / 5. * idx) / 255.
        else:
            color = int(255 - 255 / (25 - 1.) * (idx - self.fading)) / 255.
        context = cairo.Context(image)
        context.translate(self.position[0], self.position[1])
        context.set_source_surface(self.phrase)
        context.paint_with_alpha(color)

    def set_language(self, language):
        ':type language: languages'
        if language == Languages.ENGLISH:
            self.phrase = self.phrases[Languages.ENGLISH]
        elif language == Languages.SPANISH:
            self.phrase = self.phrases[Languages.SPANISH]


class zoom:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 100
        self.startRect = [0, 0, 1280, 720]
        self.endRect = [723, 255, 823, 323]

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        t = min(idx / 99., 1)
        rect = (int((1 - t) * self.startRect[0] + t * self.endRect[0]),
                int((1 - t) * self.startRect[1] + t * self.endRect[1]),
                int((1 - t) * self.startRect[2] + t * self.endRect[2]),
                int((1 - t) * self.startRect[3] + t * self.endRect[3]))

        s_x = 1280. / (rect[2] - rect[0])
        s_y = 720. / (rect[3] - rect[1])
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720)
        context = cairo.Context(surface)
        context.scale(s_x, s_y)
        context.translate(-rect[0], -rect[1])
        context.set_source_surface(image)
        context.paint()
        context = cairo.Context(image)
        context.set_source_surface(surface)
        context.paint()


class stickman:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 270

    def draw(self, frame, image):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        context = cairo.Context(image)
        img = cairo.ImageSurface.create_from_png("./sequences/call/frame{}.png".format(max(0,min(165-idx+80, 165))))
        context.set_source_surface(img)
        context.paint()
        if idx == 0:
            image.write_to_png("./images/bgCallForAction.png")


class evolve(evolve_base):
    renderer = TextTRenderer()
    font = "Calibri"
    # font = aggdraw.Font("white", "./fonts/calibri.ttf", 4)

    text_english = [u"Help indigenous women to drive their own",
                    u"bottom-up sustainable development.",
                    "             ",
                    u"Team up with PSYDEH to ",
                    u"support our first ever Crowdfunding campaign."]
    text_spanish = [u"Ay\u00fadanos a impulsar el desarrollo sustentable desde", u"la ra\u00edz.", "             ",
                    u"Hagamos equipo con estas mujeres ind\u00edgenas y PSYDEH",
                    u"apoyando nuestra primera campa\u00f1a de Crowdfunding."]

    phrase1 = {Languages.ENGLISH: renderer.makeImage_centered_runnable(text_english, font, 35, 60),
               Languages.SPANISH: renderer.makeImage_centered_runnable(text_spanish, font, 35, 60)}

    text_english = [u"Our campaign goal is $25,000usd.",
                    "     ",
                    u"This money will produce, at minimum, 3 outcomes."]
    text_spanish = [u"Nuestra meta de recaudaci\u00f3n es de $15,000 d\u00f3lares.",
                    "     ",
                    u"Esta cantidad generar\u00e1 3 proyectos."]

    phrase2 = {Languages.ENGLISH: renderer.makeImage_centered_runnable(text_english, font, 35, 60),
               Languages.SPANISH: renderer.makeImage_centered_runnable(text_spanish, font, 35, 60)}

    text_english = [u"\u25cf Five new community-improvement projects",u"    produced by women-led organizations."]
    text_spanish = [u"Cinco proyectos nuevos por las cinco", u"organizaciones de la Red \"paraguas\" de las",
                    u"mujeres ind\u00edgenas."]

    font = "Calibri Bold"
    phrase3 = {Languages.ENGLISH: renderer.makeImage(text_english, font, 35),
               Languages.SPANISH: renderer.makeImage(text_spanish, font, 35)}

    text_english = [u"\u25cf Leadership training program for",u"    the Network's women members."]
    text_spanish = [u"Programa de entrenamiento e incubaci\u00f3n",
                    u"de la Cooperativa Regional de las Artesanas", u"Ind\u00edgenas"]

    phrase4 = {Languages.ENGLISH: renderer.makeImage(text_english, font, 35),
               Languages.SPANISH: renderer.makeImage(text_spanish, font, 35)}

    text_english = [u"\u25cf A Public Forum where women present their",u"    development agenda to new government", u"    leaders."]
    text_spanish = [u"Programa de Entrenamiento Narrativo para", u"las mujeres l\u00edderes de la Red \"paraguas\""]

    phrase5 = {Languages.ENGLISH: renderer.makeImage(text_english, font, 35),
               Languages.SPANISH: renderer.makeImage(text_spanish, font, 35)}

    text_english = [u"\u25cfA Public Forum", u"Forum of Indigenous Citizens."]
    text_spanish = [u"Programa de Entrenamiento Narrativo para", u"las mujeres l\u00edderes de la Red \"paraguas\""]

    phrase6 = {Languages.ENGLISH: renderer.makeImage(text_english, font, 35),
               Languages.SPANISH: renderer.makeImage(text_spanish, font, 35)}

    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 690
        self.list = []
        self.list.append(still(start))
        self.list.append(emoticon(start + 230))
        self.list.append(animation3D(start + 430))
        self.list.append(zoom(start + 330))
        self.list.append(
            Transitions.blender(None, cairo.ImageSurface.create_from_png("./images/penmujer_smiling.png"), start + 670,
                                20))
        self.list.append(OneThought(start, 500, True))
        self.list.append(
            Transitions.blender(None, cairo.ImageSurface.create_from_png("./images/bgCallForAction.png"), start + 420,
                                10))
        self.list.append(text(start + 50, 190, 50, self.phrase1, (110, 240)))
        self.list.append(text(start + 290, 90, 50, self.phrase2, (250, 280)))

        self.list.append(stickman(start + 430))

        # self.list.append(leaf(start + 430, start + 440, 200, cairo.ImageSurface.create_from_png("./images/leaf1.png")))
        self.list.append(leafText(start + 595, 75, self.phrase3, (300-40, 200)))
        # self.list.append(leaf(start + 430, start + 510, 300, cairo.ImageSurface.create_from_png("./images/leaf2.png")))
        self.list.append(leafText(start + 515, 75+80, self.phrase4, (300-40, 300)))
        # self.list.append(leaf(start + 430, start + 590, 400, cairo.ImageSurface.create_from_png("./images/leaf3.png")))
        self.list.append(leafText(start + 445, 75+150, self.phrase5, (300-40, 400)))
        # self.list.append(leaf(start + 430, start + 660, 450, cairo.ImageSurface.create_from_png("./images/leaf4.png")))
        # self.list.append(leafText(start + 665, 75, self.phrase6, (300, 450)))
