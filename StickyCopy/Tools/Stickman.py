import math
from enum import Enum

from PIL import ImageDraw2


class Part(Enum):
    POSITION = 1
    TORSO = 2
    UPPER_LEG_1 = 3
    LOWER_LEG_1 = 4
    UPPER_LEG_2 = 5
    LOWER_LEG_2 = 6
    UPPER_ARM_1 = 7
    LOWER_ARM_1 = 8
    UPPER_ARM_2 = 9
    LOWER_ARM_2 = 10
    HEAD = 11


class Stickman:
    def __init__(self):
        self.length_torso = 60
        self.length_leg = 50
        self.length_arm = 40
        self.radius_head = 35 / 2.
        self.orientation = {}
        self.position = {}
        for part in Part:
            self.orientation[part] = 0
        self.position[Part.POSITION] = (500, 500)

    def set_position(self, x, y):
        self.position[Part.POSITION] = (x, y)

    def inc_position(self, dx, dy):
        self.orientation[Part.POSITION] = (
            self.orientation[Part.POSITION][0] + dx, self.orientation[Part.POSITION][1] + dy)

    def inc_angle(self, part: Part, d_rad):
        self.orientation[part] += d_rad

    def set_angle(self, part: Part, rad):
        self.orientation[part] = rad

    def get_angle(self, part: Part):
        return self.orientation[part]

    def get_data(self) -> dict:
        return self.orientation.copy()

    def set_data(self, data):
        self.orientation = data

    def get_position(self, part: Part):
        return self.position[part]

    def draw(self, image):
        self._calculate_points()
        canvas = ImageDraw2.Draw(image)
        pen = ImageDraw2.Pen("blue", width=7, opacity=125)
        pen2 = ImageDraw2.Pen("red", width=7, opacity=125)
        brush = ImageDraw2.Brush("blue", 125)
        pos_1 = self.position[Part.POSITION]
        pos_2 = self.position[Part.TORSO]
        canvas.line(pos_1 + pos_2, pen)
        pos_1 = self.position[Part.POSITION]
        pos_2 = self.position[Part.UPPER_LEG_1]
        canvas.line(pos_1 + pos_2, pen2)
        pos_1 = self.position[Part.UPPER_LEG_1]
        pos_2 = self.position[Part.LOWER_LEG_1]
        canvas.line(pos_1 + pos_2, pen2)
        pos_1 = self.position[Part.POSITION]
        pos_2 = self.position[Part.UPPER_LEG_2]
        canvas.line(pos_1 + pos_2, pen)
        pos_1 = self.position[Part.UPPER_LEG_2]
        pos_2 = self.position[Part.LOWER_LEG_2]
        canvas.line(pos_1 + pos_2, pen)
        pos_1 = self.position[Part.TORSO]
        pos_2 = self.position[Part.UPPER_ARM_1]
        canvas.line(pos_1 + pos_2, pen2)
        pos_1 = self.position[Part.UPPER_ARM_1]
        pos_2 = self.position[Part.LOWER_ARM_1]
        canvas.line(pos_1 + pos_2, pen2)
        pos_1 = self.position[Part.TORSO]
        pos_2 = self.position[Part.UPPER_ARM_2]
        canvas.line(pos_1 + pos_2, pen)
        pos_1 = self.position[Part.UPPER_ARM_2]
        pos_2 = self.position[Part.LOWER_ARM_2]
        canvas.line(pos_1 + pos_2, pen)
        for part in Part:
            pos = self.position[part]
            if part == Part.HEAD:
                r = self.radius_head
                brush = ImageDraw2.Brush("blue", 125)
                canvas.ellipse((pos[0] - r, pos[1] - r, pos[0] + r, pos[1] + r), pen, brush)
            else:
                brush = ImageDraw2.Brush("red", 125)
                canvas.ellipse((pos[0] - 3.5, pos[1] - 3.5, pos[0] + 3.5, pos[1] + 3.5), None, brush)
        canvas.flush()

    def _calculate_points(self):
        anchor = self.position[Part.POSITION]
        rad = self.orientation[Part.TORSO]
        self.position[Part.TORSO] = (
            anchor[0] + self.length_torso * math.sin(rad), anchor[1] - self.length_torso * math.cos(rad))

        anchor = self.position[Part.POSITION]
        rad = self.orientation[Part.UPPER_LEG_1]
        self.position[Part.UPPER_LEG_1] = (
            anchor[0] + self.length_leg * math.sin(rad), anchor[1] - self.length_leg * math.cos(rad))

        anchor = self.position[Part.UPPER_LEG_1]
        rad = self.orientation[Part.LOWER_LEG_1]
        self.position[Part.LOWER_LEG_1] = (
            anchor[0] + self.length_leg * math.sin(rad), anchor[1] - self.length_leg * math.cos(rad))

        anchor = self.position[Part.POSITION]
        rad = self.orientation[Part.UPPER_LEG_2]
        self.position[Part.UPPER_LEG_2] = (
            anchor[0] + self.length_leg * math.sin(rad), anchor[1] - self.length_leg * math.cos(rad))

        anchor = self.position[Part.UPPER_LEG_2]
        rad = self.orientation[Part.LOWER_LEG_2]
        self.position[Part.LOWER_LEG_2] = (
            anchor[0] + self.length_leg * math.sin(rad), anchor[1] - self.length_leg * math.cos(rad))

        anchor = self.position[Part.TORSO]
        rad = self.orientation[Part.HEAD]
        self.position[Part.HEAD] = (
            anchor[0] + self.radius_head * math.sin(rad), anchor[1] - self.radius_head * math.cos(rad))

        anchor = self.position[Part.TORSO]
        rad = self.orientation[Part.UPPER_ARM_1]
        self.position[Part.UPPER_ARM_1] = (
            anchor[0] + self.length_arm * math.sin(rad), anchor[1] - self.length_arm * math.cos(rad))

        anchor = self.position[Part.UPPER_ARM_1]
        rad = self.orientation[Part.LOWER_ARM_1]
        self.position[Part.LOWER_ARM_1] = (
            anchor[0] + self.length_arm * math.sin(rad), anchor[1] - self.length_arm * math.cos(rad))

        anchor = self.position[Part.TORSO]
        rad = self.orientation[Part.UPPER_ARM_2]
        self.position[Part.UPPER_ARM_2] = (
            anchor[0] + self.length_arm * math.sin(rad), anchor[1] - self.length_arm * math.cos(rad))

        anchor = self.position[Part.UPPER_ARM_2]
        rad = self.orientation[Part.LOWER_ARM_2]
        self.position[Part.LOWER_ARM_2] = (
            anchor[0] + self.length_arm * math.sin(rad), anchor[1] - self.length_arm * math.cos(rad))
