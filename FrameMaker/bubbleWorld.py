import cairo
import math

from Tools.frontender import evolve_base, Languages


class bubble:
    def __init__(self, start, fading, length):
        self.startTime = start
        self.stopTime = start + length
        pos_x = 190
        pos_y = 700
        radius = 10
        pen_size = 2.5
        self.bubbles = [[pos_x, pos_y, radius, pen_size]]
        for i in range(1, length):
            pos_x += 1.25 + radius / 10
            pos_y -= 0.67 + radius * radius / 500
            radius += 0.4
            if i >= fading:
                pen_size = max(0, 2.5 - (i - fading) / 30.)
            self.bubbles.append([pos_x, pos_y, radius, pen_size])

    def draw(self, frame, surface):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        pos_x = self.bubbles[frame - self.startTime][0]
        pos_y = self.bubbles[frame - self.startTime][1]
        radius = self.bubbles[frame - self.startTime][2]
        pen_size = self.bubbles[frame - self.startTime][3]
        context = cairo.Context(surface)
        context.set_source_rgb(0., 0., 0.)
        context.arc(pos_x, pos_y, radius, 0, 2 * math.pi)
        context.set_line_width(pen_size)
        context.stroke()
        # d = aggdraw.Draw(image)
        # p = aggdraw.Pen("black", pen_size)
        # d.ellipse((pos_x - radius, pos_y - radius, pos_x + radius, pos_y + radius), p)
        # d.flush()


class worldBubble:
    def __init__(self, start, length):
        self.startTime = start
        self.stopTime = start + length
        self.world = cairo.ImageSurface.create_from_png("./images/world.png")
        pos_x1 = 322.87
        pos_y1 = 640.1548
        radius1 = 27.199999999999964
        radius2 = 1.2
        pen_size = 2.5
        frac = 0
        self.bubbles = [[pos_x1, pos_y1, radius1 + radius2, pen_size]]
        for i in range(1, length):
            pos_x1 += 1.25 + radius1 / 10
            pos_y1 -= 0.67 + radius1 * radius1 / 500
            radius1 += 0.4
            radius2 += 1.2
            pos_x = (1 - frac) * pos_x1 + (frac) * 1280 / 2.
            pos_y = (1 - frac) * pos_y1 + (frac) * 720 / 2.
            radius = min(radius2 + radius1, 315);
            frac = min(1, i * i / (120. * 120.))
            self.bubbles.append([pos_x, pos_y, radius, pen_size + i / 30.])

    def draw(self, frame, surface):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        pos_x = self.bubbles[frame - self.startTime][0]
        pos_y = self.bubbles[frame - self.startTime][1]
        radius = self.bubbles[frame - self.startTime][2]
        pen_size = self.bubbles[frame - self.startTime][3]
        context = cairo.Context(surface)
        context.set_source_rgb(0., 0., 0.)
        context.arc(pos_x, pos_y, radius, 0, 2 * math.pi)
        context.set_line_width(pen_size)
        context.stroke()
        context.translate(int(pos_x - radius), int(pos_y - radius))
        scale_h = 2 * radius / self.world.get_height()
        scale_w = 2 * radius / self.world.get_width()
        context.scale(scale_w, scale_h)
        context.set_source_surface(self.world)
        context.paint_with_alpha(min((frame - self.startTime) * 2, 255) / 255.)


class flippingWorld:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 96
        self.world = cairo.ImageSurface.create_from_png("./images/world.png")

    def draw(self, frame, surface):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        radius_x = 315.
        radius_y = int(315 * (1 - math.sin(math.pi / 2. * ((frame - self.startTime) / 79.)))) if (
                                                                                                 frame - self.startTime) < 80 else 0
        offset_y = int(0.75 * (315 - radius_y))

        pos_x = 640
        pos_y = (360 + offset_y)
        context = cairo.Context(surface)
        context.set_source_rgb(0., 0., 0.)
        if radius_y != 0:
            context.scale(1, radius_y / radius_x)
            context.arc(pos_x, pos_y * radius_x / radius_y, radius_x, 0, 2 * math.pi)
            context.scale(1, radius_x / radius_y)
            context.set_line_width(8.46666)
            context.stroke()
            context.translate(int(pos_x - radius_x), int(pos_y - radius_y))
            scale_h = (2. * radius_y) / self.world.get_height()
            scale_w = (2. * radius_x) / self.world.get_width()
            context.scale(scale_w, scale_h)
            context.set_source_surface(self.world)
            context.paint()
        else:
            context.move_to(pos_x - radius_x, pos_y)
            context.line_to(pos_x + radius_x, pos_y)
            context.set_line_width(8.46666)
            context.stroke()


class Title:
    def __init__(self, start, length, position):
        self.startTime = start
        self.stopTime = start + length
        self.title = cairo.ImageSurface.create_from_png("./images/title/title.png")
        self.position = position

    def draw(self, frame, surface):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = frame - self.startTime
        if idx < 70:
            color = min(5 * idx, 255)
        else:
            color = max(255 - 5 * (idx - 70), 0)
        context = cairo.Context(surface)
        context.translate(self.position[0], self.position[1])
        context.set_source_surface(self.title)
        context.paint_with_alpha(color / 255.)

    def set_language(self, language):
        if language == Languages.ENGLISH:
            self.title = cairo.ImageSurface.create_from_png("./images/title/title.png")
            print("title set to: English")
        elif language == Languages.SPANISH:
            self.title = cairo.ImageSurface.create_from_png("./images/title/title_spanish.png")
            print("title set to: Spanish")


class Walkin:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 76

    def draw(self, frame, surface):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = int((frame - self.startTime) / 2)
        color = min((15 * idx), 256)
        pattern = cairo.SurfacePattern(cairo.ImageSurface.create_from_png("./sequences/walkin/frame{}.png".format(idx)))
        context = cairo.Context(surface)
        context.set_source(pattern)
        context.rectangle(0, 0, 1280, 720)
        context.paint_with_alpha(color / 255.)


class Wall:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 32

    def draw(self, frame, surface):
        if (frame < self.startTime or frame >= self.stopTime):
            return
        idx = int((frame - self.startTime) / 2)
        pattern = cairo.SurfacePattern(cairo.ImageSurface.create_from_png("./sequences/wall/frame{}.png".format(idx)))
        context = cairo.Context(surface)
        context.set_source(pattern)
        context.rectangle(0, 0, 1280, 720)
        context.paint()


class Bar:
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 32

    def draw(self, frame, surface):
        if (frame < self.startTime or frame >= self.stopTime):
            return
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
    def __init__(self, start):
        self.startTime = start
        self.stopTime = start + 406
        self.list = []
        self.list.append(bubble(start + 0, 120, 200))
        self.list.append(bubble(start + 25, 95, 200))
        self.list.append(bubble(start + 51, 69, 200))
        self.list.append(bubble(start + 77, 43, 43))
        self.list.append(bubble(start + 103, 17, 200))
        self.list.append(Title(start + 230, 120, (0, 0)))
        self.list.append(worldBubble(start + 120, 180))
        self.list.append(flippingWorld(start + 300))
        self.list.append(Walkin(start + 300))
        self.list.append(Wall(start + 376))
        self.list.append(Bar(start + 375))
