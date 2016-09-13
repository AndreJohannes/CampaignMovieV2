import cairo
import math
import random

from Tools.frontender import Languages


class RCRectengular:
    @staticmethod
    def draw(surface, rec, radius, width=2.5, color=(255, 255, 255)):
        context = cairo.Context(surface)
        context.arc(rec[0] + radius, rec[1] + radius, radius, 2 * (math.pi / 2), 3 * (math.pi / 2))
        context.arc(rec[2] - radius, rec[1] + radius, radius, 3 * (math.pi / 2), 4 * (math.pi / 2))
        context.arc(rec[2] - radius, rec[3] - radius, radius, 0 * (math.pi / 2), 1 * (math.pi / 2))
        context.arc(rec[0] + radius, rec[3] - radius, radius, 1 * (math.pi / 2), 2 * (math.pi / 2))
        context.close_path()
        context.set_source_rgb(color[0] / 255., color[1] / 255., color[2] / 255.)
        context.fill_preserve()
        context.set_source_rgb(0, 0, 0)
        context.set_line_width(width)
        context.stroke()


class MorphingTextBox:
    def __init__(self, image, pos_x, pos_y, radius, startTime, hover=False, shift=None):
        self.image = image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.startTime = startTime
        self.randomShift = random.randint(-10, 10) if shift is None else shift
        self.hover = hover

    def draw(self, frame, surface, color=(255, 255, 255)):
        if frame < self.startTime:
            return
        idx = frame - self.startTime
        y = int(self.pos_y + .2 * idx) if self.hover else self.pos_y - 2 * idx
        x = self.pos_x - 2 * self.randomShift * math.sqrt(idx)
        radius = int(max(self.radius - 2 * idx / 2., 5))
        hdx = min(int(self.radius + 8 * idx / 2.), (self.image.get_width() + radius) / 2)
        hdy = min(int(self.radius + 8 * idx / 4.), (self.image.get_height() + radius) / 2)
        RCRectengular.draw(surface, (x - hdx, y - hdy, x + hdx, y + hdy), radius, 2.5, color)
        context = cairo.Context(surface)
        context.translate(int(x) - hdx + radius, y - hdy + radius)
        scale_w = (2 * hdx - 2 * radius) / (1.0 * self.image.get_width())
        scale_h = (2 * hdy - 2 * radius) / (1.0 * self.image.get_height())
        if (scale_h == 0 or scale_w == 0):
            return
        context.scale(scale_w, scale_h)
        context.set_source_surface(self.image)
        context.paint_with_alpha(min(idx * 10 / 255., 1))
        # d.flush()
        # textbox = self.image.resize((2 * hdx - 2 * radius, 2 * hdy - 2 * radius), Image.ANTIALIAS)
        # textMask = Image.new("L", textbox.size, "black")
        # color = idx * 10
        # textMask.paste((color), (0, 0), textbox)
        # image.paste("black", (int(x) - hdx + radius, y - hdy + radius), textMask)


class TimedBubble:
    def __init__(self, pos_x, pos_y, radius, startTime, duration):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.startTime = startTime
        self.duration = duration
        self.stopTime = startTime + duration + 1

    def draw(self, frame, surface):
        if frame < self.startTime or frame >= self.stopTime:
            return
        context = cairo.Context(surface)  # type: cairo.Context
        context.arc(self.pos_x, self.pos_y, self.radius, 0, 2 * math.pi)
        context.set_line_width(2.5)
        idx = frame - self.startTime
        alpha = (1. * idx) / self.duration
        context.set_source_rgba(0, 0, 0, alpha)
        context.stroke()


class MovingBubble:
    def __init__(self, pos_x, pos_y, radius, startTime, duration, left=False, down=False):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.startTime = startTime
        self.stopTime = startTime + duration
        self.to_right = not left
        self.down = down

    def draw(self, frame, image):
        if frame < self.startTime:
            return
        if self.stopTime is not None and self.stopTime < frame:
            return
        idx = frame - self.startTime
        pos_x = self.pos_x + 5 * idx if self.to_right else self.pos_x - 5 * idx
        pos_y = self.pos_y - 1 * idx - 0.01 * idx * idx if self.down is False else self.pos_y + 3 * idx + 0.05 * idx * idx
        radius = self.radius + 0.5 * idx
        context = cairo.Context(image)
        context.arc(pos_x, pos_y, radius, 0, 2 * math.pi)
        color = min(255, int((255 * idx) / 10)) / 255.
        context.set_line_width(2.5)
        context.stroke()


class TranscendingBubble:
    def __init__(self, image, pos_x, pos_y, radius, startTime):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.startTime = startTime
        self.image = image

    def draw(self, frame, image):
        if (frame < self.startTime):
            return
        idx = frame - self.startTime
        radius = self.radius + 10 * idx + 0.1 * idx * idx
        context = cairo.Context(image)
        context.set_source_surface(self.image)
        context.arc(self.pos_x, self.pos_y, radius, 0, 2. * math.pi)
        context.clip()
        context.paint()
        context = cairo.Context(image)
        context.arc(self.pos_x, self.pos_y, radius, 0, 2. * math.pi)
        context.set_source_rgb(0, 0, 0)
        context.set_line_width(2.5)
        context.stroke()


class OneThought:
    def __init__(self, startTime, images, pos_x):
        self.lenguage = Languages.ENGLISH
        self.images = images
        self.bubble1 = TimedBubble(pos_x, 358, 10, startTime, 30)
        self.bubble2 = TimedBubble(pos_x, 318, 15, startTime + 10, 20)
        self.bubble3 = TimedBubble(pos_x, 268, 20, startTime + 20, 10)
        self.rectangualar = MorphingTextBox(images[Languages.ENGLISH], pos_x, 268, 20, startTime + 30)

    def draw(self, frame, image):
        self.bubble1.draw(frame, image)
        self.bubble2.draw(frame, image)
        self.bubble3.draw(frame, image)
        self.rectangualar.draw(frame, image, (248, 240, 118))

    def set_language(self, language):
        self.rectangualar.image = self.images[language]


class ThoughtfulTransition:
    def __init__(self, startTime, image, pos_x):
        self.bubble1 = TimedBubble(pos_x, 358, 10, startTime, 30)
        self.bubble2 = TimedBubble(pos_x, 318, 15, startTime + 10, 20)
        self.bubble3 = TimedBubble(pos_x, 268, 20, startTime + 20, 10)
        self.transcendingBubble = TranscendingBubble(image, pos_x, 268, 20,
                                                     startTime + 30)

    def draw(self, frame, image):
        self.bubble1.draw(frame, image)
        self.bubble2.draw(frame, image)
        self.bubble3.draw(frame, image)
        self.transcendingBubble.draw(frame, image)


class Line:
    def __init__(self, startTime, stopTime, startPoint, stopPoint):
        self.startTime = startTime
        self.stopTime = stopTime
        self.startPoint = startPoint
        self.stopPoint = stopPoint

    def draw(self, frame, image):
        if (frame < self.startTime):
            return
        idx = frame - self.startTime
        x = min(1.0 * (idx + 1) / (self.stopTime - self.startTime), 1)
        startPoint = self.startPoint
        stopPoint = ((1 - x) * startPoint[0] + x * self.stopPoint[0], (1 - x) * startPoint[1] + x * self.stopPoint[1])
        context = cairo.Context(image)
        context.move_to(startPoint[0], startPoint[1])
        context.line_to(stopPoint[0], stopPoint[1])
        context.set_source_rgb(0, 0, 0)
        context.set_line_width(2.5)
        context.stroke()
